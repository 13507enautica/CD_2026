import json
import socket
from Complexo import Complexo

def sendJSON(c1, c2, oper):
    return json.dumps({"real": [c1.getReal(), c2.getReal()], "imaginary": [c1.getImaginary(), c2.getImaginary()], "oper": oper}).encode("utf-8")

if __name__ == "__main__":
    DefaultAddress = "localhost"
    DefaultPort = 12349

    c1 = Complexo(2)
    c2 = Complexo(3)

    oper = '*'

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((DefaultAddress, DefaultPort))

        message = sendJSON(c1, c2, oper)

        s.sendall(message)

        response = s.recv(1024).decode("utf-8")
        print(f"Result: {response}")
