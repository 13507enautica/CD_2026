#Credits for the socket implementation:
#https://medium.com/@andrescoronel1209/building-a-socket-json-based-communication-protocol-using-python-f9233c38d2f4

import os
import socket
import struct
import json
from flask import Flask, redirect, request, render_template, jsonify, url_for, session
from werkzeug.security import generate_password_hash
import logging
import re
import requests
from datetime import datetime

SERVER_HOST = "database"
SERVER_PORT = int(os.getenv("SERVER_PORT"))
DATABASE_PORT = int(os.getenv("DATABASE_PORT"))

app = Flask(__name__)
app.secret_key = 'bolachinha'  # Necessária para usar sessões
app.url_map.strict_slashes = False
app.config['JSON_AS_ASCII'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

app.base_directory = "static"
app.scripts_directory = "private"
DATABASE_FILE = os.path.join("private", "dados.json")

def listFiles(directory, extension):
    try:
        if not extension.startswith('.'):
            extension = f".{extension}"

        ficheiros = [
            {"nome": f}
            for f in os.listdir(directory)
            if os.path.isfile(os.path.join(directory, f)) and f.endswith(extension)
        ]

        return ficheiros

    except Exception as e:
        return json.dumps({"error": str(e)}, indent=4)


# Configuração de logging
logging.basicConfig(level=logging.DEBUG)

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


@app.route('/')
def home():
    return render_template('index.html')  # Página principal


@app.route('/login')
def login():
    return render_template('login.html')  # Página de login


@app.route('/register')
def register():
    return render_template('register.html')  # Página de registro


@app.route('/procura')
def procura():
    return render_template('procura.html')  # Página de registro


@app.route('/main')
def main():
    if 'user' not in session:
        return redirect(url_for('login'))  # Redirecionar se não estiver logado
    return render_template('main.html', user=session['user'])


@app.route('/register-boat')
def register_boat():
    # Verifica se o usuário está autenticado
    if 'user' not in session:
        return redirect(url_for('login'))

    # Renderiza a página de registro de embarcações
    return render_template('naviosreg.html', user=session['user'])


@app.route('/doRegister', methods=['POST'])
def doRegister():
    logging.debug("Route /doRegister called...")

    fullname = request.form.get('fullname')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    if not fullname or not email or not password or not confirm_password:
        return render_template("register.html", error="Todos os campos são obrigatórios!")

    if password != confirm_password:
        return render_template("register.html", error="As senhas não coincidem!")

    email_pattern = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$")
    if not email_pattern.match(email):
        return render_template("register.html", error="Por favor, insira um email válido!")

    if len(password) < 8:
        return render_template("register.html", error="A senha deve ter pelo menos 8 caracteres!")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        # Send a JSON request
        requestj = {
            "action": "/checkUser",
            "data": {
                "username": "alice",
                "email": "alice@example.com"
            }
        }
        send_json(client, requestj)

        # Receive and print the JSON response
        response = recv_json(client)
        print(f"Server response: {response}")

        if response["exists"]:
            return render_template("register.html", error="O email já está registrado!")

        new_user = {
            "fullname": fullname,
            "email": email,
            "password": generate_password_hash(password)
        }

        requestj = {
            "action": "/register",
            "data": new_user
        }
        send_json(client, requestj)

        response = recv_json(client)

    if (response["status"] != "ok"):
        return render_template("register.html", error="Ocorreu um erro ao registar o utilizador!")

    return render_template("login.html", success="Registro bem-sucedido! Faça login para continuar.")


@app.route('/doLogin', methods=['POST'])
def doLogin():
    logging.debug("Route /doLogin called...")

    email = request.form.get('email')
    password = request.form.get('password')

    email_pattern = re.compile(r"^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$")
    if not email_pattern.match(email):
        return render_template("login.html", error="Por favor, insira um email válido!")

    if len(password) < 8:
        return render_template("login.html", error="A senha deve ter pelo menos 8 caracteres!")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        requestj = {"action": "/login",
                    "data": {"email": email, "password": password}}

        send_json(client, requestj)

        response = recv_json(client)

    if "status" not in response.keys():
        user = response["user"]
        print(user)
        session['user'] = {"email": user['email'], "fullname": user['fullname'], "id": user['id']}
        logging.debug("Login bem-sucedido.")
        return render_template('main.html', user=session['user'])

    return render_template("login.html", error="O email ou a senha estão incorretos!")

@app.route('/logout')
def logout():
    session.pop('user', None)
    logging.debug("Usuário deslogado.")
    return redirect('/login')

@app.route('/book-stay')
def book_stay():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_id = session['user']['id']

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        requestj = {
            "action": "/getUserBoats",
            "data": {"user_id": user_id}
        }

        send_json(client, requestj)

        user_boats = recv_json(client)["boats"]

        requestj = {
            "action": "/getUserPorts"
        }

        send_json(client, requestj)

        available_ports = recv_json(client)["ports"]

    if not user_boats:
        return render_template('main.html', error="Você não possui barcos disponíveis. Cadastre um para continuar.",
                               user=session['user'])
    if not available_ports:
        return render_template('main.html', error="Não há portos disponíveis no momento.", user=session['user'])

    return render_template('estadiareg.html', user=session['user'], user_boats=user_boats, boat_ports=available_ports)


@app.route('/searchBoat', methods=['GET'])
def search_boat():
    email = request.args.get('email', '').strip()
    if not email:
        return jsonify({"error": "E-mail não fornecido!"}), 400

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        requestj = {"action": "/searchBoat",
                    "data": {"email": email}}

        send_json(client, requestj)

        boats = recv_json(client)["boats"]

    if not boats:
        return render_template('results.html', message=f"Nenhum barco encontrado para o e-mail: {email}")

    return render_template('results.html', boats=boats)


@app.route('/searchStay', methods=['GET'])
def search_stay():
    logging.basicConfig(level=logging.DEBUG)

    # Obter a data da estadia
    stay_date = request.args.get('stay_date', '').strip()
    logging.debug(f"Data fornecida pelo usuário: {stay_date}")

    if not stay_date:
        return jsonify({"error": "Data não fornecida!"}), 400

    try:
        stay_date = datetime.strptime(stay_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"error": "Data inválida! Formato esperado: YYYY-MM-DD."}), 400

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        requestj = {"action": "/searchStay",
                    "data": {"stay_date": str(stay_date)}}

        send_json(client, requestj)

        stays = recv_json(client)["stays"]

    if not stays:
        return render_template('results.html', message=f"Nenhuma estadia encontrada para a data: {stay_date}")

    return render_template('results.html', stays=stays)


@app.route('/doRegisterBoat', methods=['POST'])
def doRegisterBoat():
    logging.debug("Route /doRegisterBoat called...")

    # Verificando se o usuário está logado
    if 'user' not in session:
        return {"error": "Usuário não autenticado"}, 401

    if 'boat-image' not in request.files:
        logging.debug("Ficheiro nao existente!")
        return {"error": "Ficheiro nao existente!"}, 400

    file = request.files['boat-image']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.

    if file.filename == '':
        logging.debug("Ficheiro nao foi selecionado!")
        return {"error": "Ficheiro nao foi selecionado!"}, 400

    filename = file.filename
    logging.debug(filename)

    file.save(os.path.join("static/Images", filename))

    # Obtendo dados da embarcação do formulário
    boat_name = request.form.get('boat-name', '').strip()
    boat_type = request.form.get('boat-type', '').strip()
    registration_number = request.form.get('registration-number', '').strip()
    year_built = request.form.get('year-built', '').strip()
    length = request.form.get('length', '').strip()
    boat_image = filename

    # Validações dos campos
    if not all([boat_name, boat_type, registration_number, year_built, length, boat_image]):
        return {"error": "Todos os campos são obrigatórios!"}, 400

    try:
        year_built = int(year_built)
        if year_built < 1900 or year_built > 2025:
            return {"error": "Por favor, insira um ano válido (entre 1900 e 2025)."}, 400
    except ValueError:
        return {"error": "Ano de construção inválido!"}, 400

    try:
        length = float(length)
        if length <= 0:
            return {"error": "O comprimento deve ser maior que 0."}, 400
    except ValueError:
        return {"error": "Comprimento inválido!"}, 400

    # Recuperando ID do usuário da sessão
    user_id = session['user']['id']

    # Criando registro da embarcação
    new_boat = {
        "available": 1,
        "owner_email": session['user']['email'],
        "name": boat_name,
        "type": boat_type,
        "registration_number": registration_number,
        "owner_name": session['user']['fullname'],
        "year_built": year_built,
        "length": length,
        "boat_image": boat_image,
        "user_id": user_id
    }

    # Adicionando à base de dados
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        requestj = {"action": "/registerBoat",
                    "data": new_boat}

        send_json(client, requestj)

    logging.debug(f"Boat registered successfully: {new_boat}")
    return redirect('/register-boat')


@app.route('/doBookStay', methods=['POST'])
def doBookStay():
    logging.debug("Route /doBookStay called...")

    # Verificando se o usuário está logado
    if 'user' not in session:
        return {"error": "Usuário não autenticado"}, 401

    # Obtendo os dados do formulário
    stay_boat = request.form.get('stay-boat', '').strip()
    stay_desc = request.form.get('stay-desc', '').strip()
    stay_passagers = request.form.get('stay-passagers', '').strip()
    stay_loadsize = request.form.get('stay-loadsize', '').strip()
    stay_port = request.form.get('stay-port', '').strip()
    stay_date1 = request.form.get('stay-date1', '').strip()
    stay_date2 = request.form.get('stay-date2', '').strip()
    latitude = request.form.get('latitude', '').strip()
    longitude = request.form.get('longitude', '').strip()

    # Validações dos campos obrigatórios
    if not all([stay_boat, stay_desc, stay_passagers, stay_port, stay_date1, stay_date2, latitude, longitude]):
        return {"error": "Todos os campos são obrigatórios!"}, 400

    try:
        stay_passagers = int(stay_passagers)
        if stay_passagers < 0 or stay_passagers > 9999:
            return {"error": "Número de passageiros inválido! Deve estar entre 0 e 9999."}, 400
    except ValueError:
        return {"error": "Número de passageiros inválido!"}, 400

    # Validação para tamanho de carga (pode ser 0 ou maior)
    if stay_loadsize:
        try:
            stay_loadsize = float(stay_loadsize)
            if stay_loadsize < 0:  # Não pode ser negativo
                return {"error": "O tamanho da carga não pode ser negativo."}, 400
        except ValueError:
            return {"error": "Tamanho de carga inválido!"}, 400
    else:
        stay_loadsize = 0  # Caso não seja fornecido, define como 0

    try:
        latitude = latitude
        longitude = longitude
    except ValueError:
        return {"error": "Latitude ou longitude inválida!"}, 400

    # Recuperando ID do usuário da sessão
    user_id = session['user']['id']

    # Criando registro da estadia
    new_stay = {
        "boat_id": int(stay_boat),
        "description": stay_desc,
        "passengers": stay_passagers,
        "load_size": stay_loadsize,
        "port_id": int(stay_port),
        "arrival_time": stay_date1,
        "departure_time": stay_date2,
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "user_id": user_id
    }

    # Adicionando à base de dados
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((SERVER_HOST, DATABASE_PORT))

        requestj = {"action": "/bookStay",
                    "data": new_stay}

        send_json(client, requestj)

    logging.debug(f"Stay booked successfully: {new_stay}")
    return redirect('/book-stay')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=SERVER_PORT)