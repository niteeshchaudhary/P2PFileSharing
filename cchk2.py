# echo-client.py

import socket
import random
import threading
import os
import time
import sys

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 5000 # The port used by the server
inp=""
files_available=[]
folder=""

def handle_input():
    global inp, files_available,folder
    while True:
        inp=input("Enter the message:(DISCONNECT, REQFILE, ADDFOLDER,CHEKFILE) ")
        if inp == "DISCONNECT":
            break
        elif inp=="REQFILE":
            fname=input("Enter the filename: ")
            inp=inp+" "+fname
            filerequest_thread = threading.Thread(target=handle_input)
            filerequest_thread.start()
        elif inp=="ADDFOLDER":
            fname=input("Enter the folder Location in your system: ")
            folder=fname
        elif inp=="CHECKFILE":
            fname=input("Enter file name:")
            print(check_file(fname))            
        
def handle_files():
    global files_available,folder,inp
    while True:
        if folder != "":
            files_available=os.listdir(folder)
        if inp == "DISCONNECT":
            break
        time.sleep(30) 


def check_file(file):
    handle_files()
    if file in files_available:
        return os.path.getsize(folder+"/"+file)
    return -1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    send_port = random.randint(1024, 65535)
    s.sendall(("CONNECT "+str(send_port)).encode())
    client_thread = threading.Thread(target=handle_input)
    client_thread.setDaemon(True)
    client_thread.start()
    filesync_thread = threading.Thread(target=handle_files)
    filesync_thread.setDaemon(True)
    filesync_thread.start()
    while True:
        a=0
        data = s.recv(1024).decode()
        if(data=="PING"):
            s.sendall("PONG".encode())
        elif not data:
            pass
        else:
            pass
            #inp=input("Enter the message:(DISCONNECT, REQFILE,) ")
        if inp!="":
            if(inp=="DISCONNECT"):
                s.sendall(inp.encode())
                break
        
        # data = s.recv(1024)
        # print(f"Received {data!r}")