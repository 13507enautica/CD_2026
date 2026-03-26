# ServidorHello.py

# POR FAZER: ALTERAR PARA TRABALHAR COM SERVIDOR CONCORRENTE. SÓ PRECISO DE ALTERAR UM DOS EXEMPLOS

import sys, getopt
import socket
import threading
from _thread import start_new_thread

DefaultPort = 12345

lock = threading.Lock()

def startServer(portNumber) :
    print( "Starting Hello server on port {}".format(portNumber) )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind( ("localhost", portNumber) )
        while True :
            s.listen()
            conn, addr = s.accept()
            lock.acquire()
            print( "New connection ({})".format( addr ) )
            start_new_thread(iniciarUtilizador,(conn,))


def iniciarUtilizador(conn):
    while True:
        response = "Hello "
        data = conn.recv(1024)

        if not data:
            print("Fim de conexão")
            lock.release()
            break

        response += data.decode("utf-8")
        conn.sendall( bytes( response, "utf-8" ) )
    conn.close()

def usage() :
    print( "ServidorHello.py [--port <server port number>]" )

def parseArguments(argv) :
    print( "Parsing arguments..." )

    try:
        opts, args = getopt.getopt(argv,"h",["help", "port="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print( err )
        sys.exit( 2 )

    for opt, arg in opts:
        if opt in ( "-h", "--help" ) :
            usage()
            sys.exit()
        
        if opt in ( "-p", "--port" ) :
            startServer( int(arg) )
            sys.exit()
    
    startServer( DefaultPort )

if __name__ == "__main__":
    parseArguments( sys.argv[1:] )