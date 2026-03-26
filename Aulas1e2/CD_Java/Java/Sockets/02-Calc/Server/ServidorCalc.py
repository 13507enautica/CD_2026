# ServidorCalc.py

#https://docs.python.org/3/library/struct.html

import sys, getopt
import socket
import json
from threading import Thread
import struct
from Complexo import Complexo

DefaultPort = 12349

DebugMessages = False

"""
    Ler um valor inteiro (4 bytes) no formato Litle Endian (processadores Intel)
"""
def readIntV1(connection) :
    val = 0
    iter = 0
    while iter < 4 :
        aux = connection.recv( 1 )[0]
        val = (aux << (iter*8)) | val
        iter = iter + 1

    return val

"""
    Ler um valor inteiro (4 bytes) no formato Big Endian / Network (processadores Motorola / Java) - v1
"""
def readIntV2(connection) :
    val = 0
    iter = 3
    while iter >= 0 :
        aux = connection.recv( 1 )[0]
        val = (aux << (iter*8)) | val
        iter = iter - 1

    return val

"""
    Ler um valor inteiro (4 bytes) no formato Big Endian / Network (processadores Motorola / Java) - v2
"""
def readIntV3(connection) :
    return struct.unpack( "!i", connection.recv( 4 ) )[0]

"""
    Ler um valor inteiro (4 bytes)
"""
def readInt(connection) :
    #return readIntV1(connection)
    return readIntV2(connection)
    #return readIntV3(connection)

"""
    Escrever um valor inteiro no formato nativo.
    
    Corresponde ao hardware onde o servidor se está a executar 
"""
def writeIntV1(connection, value) :
    connection.sendall( struct.pack( '@i', value ) )

"""
    Escrever um valor inteiro no formato Litle Endian (processadores Intel)
"""
def writeIntV2(connection, value) :
    mask = 0x000000ff
    iter = 0
    while iter < 4 :
        aux = ( value & ( mask << (iter*8) ) ) >> ( iter * 8 )

        if ( DebugMessages==True ) :
            print( "Sending {}".format( aux ) )

        connection.sendall( struct.pack( 'b', aux ) )
        iter = iter + 1

"""
    Escrever um valor inteiro no formato Big Endian (processadores Motorola)
"""
def writeIntV3(connection, value) :
    mask = 0xff000000
    iter = 3
    while iter >= 0 :
        aux = (value & ( mask >> ( 3-iter) * 8 ) ) >> ( iter * 8 )

        if ( DebugMessages==True ) :
            print( "Sending {}".format( aux ) )
        
        connection.sendall( struct.pack( 'b', aux ) )
        iter = iter - 1 

"""
    Escrever um valor inteiro (4 bytes) do formato local para network (Big Endian) 
"""
def writeIntV4(connection, value) :
    aux = struct.pack( "!i", value )

    if ( DebugMessages==True ) :
        print( "Sending {}".format( aux ) )

    connection.sendall( aux )

"""
    Escrever um valor inteiro
"""
def writeInt(connection, value) :
    #writeIntV1(connection, value)
    #writeIntV2(connection, value)
    writeIntV3(connection, value)
    #writeIntV4(connection, value)

def readByte(connection) :
    return connection.recv( 1 ).decode( "utf-8" )

def readJSON(connection):
    data = connection.recv(1024).decode("utf-8")
    return json.loads(data)

def ServidorDedicado(cliConnection, cliAddress):
    print( "Starting thread to handle data from {}".format(cliAddress) )

    global DebugMessages

    with cliConnection:
        while True :
            try :
                data = readJSON(cliConnection)

                oper = data["oper"]
                c1 = Complexo(data["real"][0], data["imaginary"][0])
                c2 = Complexo(data["real"][1], data["imaginary"][1])

                match oper : 
                    case '+' :
                        res = c1.addTo(c2)
                    case '-' :
                        res = c1.subtractTo(c2)
                    case '*' :
                        res = c1.multiplyBy(c2)
                    case _:
                        cliConnection.sendall( "Invalid operation" ).encode("utf-8")
                        break

                if ( DebugMessages==True ) :
                    print( "Going to send: {}".format( str(res) ) )

                cliConnection.sendall(str(res).encode("utf-8"))
            except socket.error as sockEx :
                print( "Socket error!\nDetails:\n{}".format( sockEx ) )
                break

            except struct.error as strEx :
                print( "Unpack error!\nDetails:\n{}".format( strEx ) )
                break
            
            except IndexError as idxEx :
                print( "No more data to read!\nDetails:\n{}".format( idxEx ) )
                break

            except Exception as genEx :
                print( "Generic error!\nDetails:\n{}".format( genEx ) )
                break
        
        cliConnection.close()

        print( "Thread to handle data from {} is ending".format(cliAddress) )

def usage() :
    print( "ServidorCalc.py [--port <server port number>]" )

def startServer(portNumber) :
    print( "Starting Calc server on port {}".format(portNumber) )

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind( ( "localhost" , portNumber ) )
        while True :
            s.listen()
            conn, addr = s.accept()
            
            print( "New connection ({})".format( addr ) )

            tt = Thread( target=ServidorDedicado, args=(conn, addr,) )
            tt.start()

def parseArguments(argv) :
    print( "Parsing arguments..." )

    try:
        opts, args = getopt.getopt(argv, "h", [ "debug", "help", "port=" ])
    except getopt.GetoptError as err:
        # print help information and exit:
        print( err )
        sys.exit( 2 )

    hostPort = DefaultPort

    for opt, arg in opts:
        if opt in ( "-h", "--help" ) :
            usage()
            sys.exit()
        
        if opt in ( "--port" ) :
            hostPort = int(arg)
        
        if opt in ( "--debug" ) :
            print( "Debug messages active." )
            global DebugMessages
            DebugMessages = True
    
    startServer( hostPort )

if __name__ == "__main__":
    parseArguments( sys.argv[1:] )
