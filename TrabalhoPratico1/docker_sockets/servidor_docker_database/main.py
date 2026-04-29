#Credits for the socket implementation:
#https://medium.com/@andrescoronel1209/building-a-socket-json-based-communication-protocol-using-python-f9233c38d2f4

import json
import socket
import os
import struct
import threading
from werkzeug.security import check_password_hash
from datetime import datetime

SERVER_HOST = "0.0.0.0"
SERVER_PORT = int(os.getenv("SERVER_PORT"))

def init_db():
    with open("db.json", "w", encoding="utf-8") as db:
        data = {"users": [], "boats": [], "ports": [], "stays": []}
        json.dump(data, db, indent=4, ensure_ascii=False)


def load_db():
    if "db.json" not in os.listdir():
        init_db()

    with open("db.json", "r", encoding="utf-8") as db:
        data = json.load(db)

    return data

def save_db(data):
    with open("db.json", "w", encoding="utf-8") as db:
        json.dump(data, db, indent=4, ensure_ascii=False)

def send_json(sock: socket.socket, data: dict) -> None:
    """Serialize data to JSON and send with a 4-byte length prefix."""
    payload = json.dumps(data).encode("utf-8")
    # Pack the length as a 4-byte big-endian unsigned integer
    header = struct.pack(">I", len(payload))
    sock.sendall(header + payload)


def recv_json(sock: socket.socket) -> dict:
    """Receive a length-prefixed JSON message from the socket."""
    # Read exactly 4 bytes for the length header
    raw_len = recvn(sock, 4)
    if not raw_len:
        raise ConnectionError("Connection closed while reading header")

    msg_len = struct.unpack(">I", raw_len)[0]

    # Read exactly msg_len bytes for the payload
    raw_payload = recvn(sock, msg_len)
    if not raw_payload:
        raise ConnectionError("Connection closed while reading payload")

    return json.loads(raw_payload.decode("utf-8"))


def recvn(sock: socket.socket, n: int) -> bytes:
    """Read exactly n bytes from the socket."""
    buf = b""
    while len(buf) < n:
        chunk = sock.recv(n - len(buf))
        if not chunk:
            return b""
        buf += chunk
    return buf

def handle_client(conn: socket.socket, addr: tuple) -> None:
    print(f"Client connected: {addr}")
    with conn:
        while True:
            try:
                msg = recv_json(conn)
                print(f"Received from {addr}: {msg}")

                match msg["action"]:
                    case "/checkUser":
                        data = load_db()
                        username = msg["data"]["username"]
                        response = {"exists": any(user['email'] == username for user in data['users'])}
                    case "/register":
                        try:
                            db = load_db()
                            data = msg["data"]
                            data["id"] = len(db["users"]) + 1

                            db['users'].append(data)
                            save_db(db)

                            response = {"status": "ok"}
                        except:
                            response = {"status": "error"}
                    case "/login":
                        data = msg["data"]
                        db = load_db()

                        user = next((u for u in db['users'] if
                                     u['email'] == data["email"] and check_password_hash(u["password"], data["password"])),
                                    None)

                        if not user:
                            response = {"status": "error"}
                        else:
                            response = {"user": user}
                    case "/getUserBoats":
                        data = msg["data"]
                        db = load_db()

                        try:
                            response = {"boats": [boat for boat in db['boats'] if
                                                      boat['user_id'] == data["user_id"] and boat['available']]}
                        except:
                            response = {"status": "error"}
                    case "/getUserPorts":
                        db = load_db()

                        try:
                            response = {"ports": [port for port in db['ports'] if port['available']]}
                        except:
                            response = {"status": "error"}
                    case "/searchBoat":
                        data = msg["data"]
                        db = load_db()

                        try:
                            response = {"boats": [boat for boat in db["boats"] if boat['owner_email'] == data["email"]]}
                        except:
                            response = {"status": "error"}
                    case "/searchStay":
                        data = msg["data"]
                        db = load_db()
                        stays = []
                        stay_date = datetime.strptime(data["stay_date"], "%Y-%m-%d").date()
                        print(stay_date)

                        for stay in db["stays"]:
                            try:
                                arrival_date = datetime.strptime(stay['arrival_time'], "%Y-%m-%dT%H:%M").date()
                                departure_date = datetime.strptime(stay['departure_time'], "%Y-%m-%dT%H:%M").date()

                                # Corrigir datas invertidas
                                if arrival_date > departure_date:
                                    arrival_date, departure_date = departure_date, arrival_date

                                # Verificar se a data fornecida está dentro do intervalo
                                if arrival_date <= stay_date <= departure_date:
                                    stays.append(stay)
                            except Exception as e:
                                response = {"status": "error"}

                        response = {"stays": stays}
                    case "/registerBoat":
                        data = msg["data"]
                        db = load_db()

                        data["id"] = len(db["boats"]) + 1

                        try:
                            db["boats"].append(data)
                            save_db(db)

                            response = {"status": "ok"}
                        except:
                            response = {"status": "error"}
                    case "/bookStay":
                        data = msg["data"]
                        db = load_db()

                        data["id"] = len(db["stays"]) + 1

                        db["stays"].append(data)
                        save_db(db)

                send_json(conn, response)

            except (ConnectionError, json.JSONDecodeError) as e:
                print(f"Client {addr} error: {e}")
                break

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((SERVER_HOST, SERVER_PORT))
        srv.listen(10)
        print(f"JSON server on {SERVER_PORT}")

        while True:
            conn, addr = srv.accept()
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()