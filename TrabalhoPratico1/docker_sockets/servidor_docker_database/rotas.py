from flask import Flask, jsonify, request
import os
import json
from werkzeug.security import check_password_hash
from datetime import datetime

server_port = int(os.getenv("SERVER_PORT"))
app = Flask(__name__)
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
@app.route('/')
def ping_online():
    return jsonify({"status": "ok"}), 200

@app.route('/checkUser/<username>')
def check_user(username):
    data = load_db()
    return jsonify({"exists": any(user['email'] == username for user in data['users'])})
@app.route('/register', methods=['POST'])
def register():
    try:
        db = load_db()
        data = request.get_json()
        data["id"] = len(db["users"])+1

        db['users'].append(data)
        save_db(db)

        return jsonify({"status": "ok"}), 200
    except:
        return jsonify({"status": "error"}), 400

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    db = load_db()

    user = next((u for u in db['users'] if u['email'] == data["email"] and check_password_hash(u["password"], data["password"])), None)

    if not user:
        return jsonify({"status": "error"}), 400
    else:
        return jsonify({"user": user}), 200

@app.route("/getUserBoats", methods=['POST'])
def getBoats():
    data = request.get_json()
    db = load_db()

    try:
        return jsonify({"boats": [boat for boat in db['boats'] if boat['user_id'] == data["user_id"] and boat['available']]}), 200
    except:
        return jsonify({"status": "error"}), 400

@app.route("/getUserPorts")
def getPorts():
    db = load_db()

    try:
        return jsonify({"ports": [port for port in db['ports'] if port['available']]}), 200
    except:
        return jsonify({"status": "error"}), 400

@app.route("/searchBoat", methods=['POST'])
def searchBoat():
    data = request.get_json()
    db = load_db()

    try:
        return jsonify({"boats": [boat for boat in db["boats"] if boat['owner_email'] == data["email"]]}), 200
    except:
        return jsonify({"status": "error"}), 400

@app.route("/searchStay", methods=['POST'])
def searchStay():
    data = request.get_json()
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
            return jsonify({"status": "error"}), 400

    return jsonify({"stays": stays}), 200

@app.route("/registerBoat", methods=['POST'])
def registerBoat():
    data = request.get_json()
    db = load_db()

    data["id"] = len(db["boats"])+1

    try:
        db["boats"].append(data)
        save_db(db)

        return jsonify({"status": "ok"}), 200
    except:
        return jsonify({"status": "error"}), 400

@app.route("/bookStay", methods=['POST'])
def bookStay():
    data = request.get_json()
    db = load_db()

    data["id"] = len(db["stays"])+1

    db["stays"].append(data)
    save_db(db)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=server_port)