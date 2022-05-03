import socket
import os
from thread import *

ServerSocket = socket.socket()
#host = 'sbsy.co.in'
host = socket.gethostname()
#host="103.128.97.81" 
#host=""
port = 5000
ThreadCount = 0
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))
f=open("datafile.txt","a")
f.write(str("server bind")+"\n")
f.close()
print('Waitiing for a Connection..')
ServerSocket.listen(5)

print("server running *********************************************\n",host,port)


def threaded_client(connection):
    #connection.send(str.encode('Welcome to the Server\n'))
    while True:
        f=open("datafile.txt","a")
        data = connection.recv(2048)
        #data="client data aayega "
        f.write(str(data)+"\n")
        f.close()
        print(data)
        reply = 'Server Says: ' + data.decode('utf-8')
        if not data:
            break
        connection.sendall(str.encode(reply))
        connection.sendall(str.encode("heloooo client"))
    connection.close()

while True:
    Client, address = ServerSocket.accept()
    print('Connected to: ' + address[0] + ':' + str(address[1]))
    f=open("datafile.txt","a")
    f.write(str(Client)+"\n")
    f.write(str(address)+"\n")
    f.close()
    start_new_thread(threaded_client, (Client, ))
    ThreadCount += 1
    print('Thread Number: ' + str(ThreadCount))
    f=open("datafile.txt","a")
    f.write(str("new_client found ")+"\n")
    f.close()
    
    
ServerSocket.close()
