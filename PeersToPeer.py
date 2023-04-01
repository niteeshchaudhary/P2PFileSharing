import socket
import threading
import time
import os

import socket
import random

# Define the buffer size for receiving data
BUFFER_SIZE = 2048

def send_file(file_path, ip_address, send_port):
    # Create a TCP socket for sending data
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the receiver's IP address and port
    send_socket.connect((ip_address, send_port))

    # Open the file to be sent and read its contents
    with open(file_path, 'rb') as f:
        file_data = f.read()

    # Send the file data over the socket
    send_socket.sendall(file_data)
    send_socket.sendall("end".encode())

    # Close the socket
    send_socket.close()

def receive_file(save_path, recv_port):
    # Create a TCP socket for receiving data
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a random available port
    recv_socket.bind(('localhost', recv_port))

    # Listen for incoming connections
    recv_socket.listen()

    # Accept the incoming connection
    conn, addr = recv_socket.accept()

    # Receive the file data from the sender
    file_data = b''
    flag=0
    while True:
        data = conn.recv(BUFFER_SIZE)
        if data.decode()=="end":
            break
        elif not data:
            flag=1
            break
        file_data += data

    # Write the received file data to disk
    if(flag==1):
        pass
    else:
        with open(save_path, 'wb') as f:
            f.write(file_data)

    # Close the connection and socket
    conn.close()
    recv_socket.close()

# Generate random ports for the sender and receiver
send_port = random.randint(1024, 65535)
recv_port = random.randint(1024, 65535)

while True:
    msg=input("Enter the message: ")
# Example usage:
# Send the file from sender to receiver
    if msg=="send":
        msg=int(input(f"available ports are {send_port} and {recv_port}"))
        send_file('file.txt', 'localhost', msg)
    elif msg=="receive":
# Receive the file from sender
        print(f"available ports are {send_port} and {recv_port}")
        receive_file('received_file.txt', recv_port)
    else:
        break


#   def sync_file_folder(self):
#     """
#     Keep file_share dictionary in sync with files that are actually there in folder.
#     """
#     actual_file_list = os.listdir('folder')
#     stored_file_list = list(self.file_share)
#     new_files = list(set(actual_file_list) - set(stored_file_list))
#     old_files = list(set(stored_file_list) - set(actual_file_list))
#     for new_file in new_files:
#       self.file_share[new_file] = True
#     for old_file in old_files:
#       del self.file_share[old_file]

#   def check_file(self, filename):
#     """
#     iterate over file-folder and check if the filename is available.
#     Availability is also dependent on whether its share variable and global share variable are both set.
#     """
#     self.sync_file_folder()
#     for file in os.listdir('folder'):
#       share = self.file_share.get(file, None)
#       if fnmatch.fnmatch(file, filename):
#         return share and self.global_share
#     return False