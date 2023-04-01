# to develop a peer-to-peer file transfer application, comprising one manager and multiple peers github
import socket

import socket
import threading

class Manager:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.peers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.ip_address, self.port))
        self.server_socket.listen()

    def start(self):
        print(f'Started server at {self.ip_address}:{self.port}')
        while True:
            conn, addr = self.server_socket.accept()
            peer = Peer(addr[0], addr[1])
            self.peers.append(peer)
            print(f'Connected to {addr[0]}:{addr[1]}')
            threading.Thread(target=self.handle_client, args=(conn, peer)).start()

    def handle_client(self, conn, peer):
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                if message == 'get_peers':
                    peer_list = [p.ip_address + ':' + str(p.port) for p in self.peers]
                    peer_list_string = ','.join(peer_list)
                    conn.sendall(peer_list_string.encode())
                elif message.startswith('send_file'):
                    file_path, dest_ip, dest_port = message.split(':')[1:]
                    if dest_ip and dest_port:
                        for p in self.peers:
                            if p.ip_address == dest_ip and p.port == int(dest_port):
                                peer.send_file(file_path, p)
                                conn.sendall(b'File sent')
                                break
                    else:
                        for p in self.peers:
                            if p != peer:
                                p.receive_file(file_path)
                        conn.sendall(b'File sent')
                elif message == 'disconnect':
                    self.peers.remove(peer)
                    print(f'Disconnected from {peer.ip_address}:{peer.port}')
                    break
                else:
                    conn.sendall(b'Invalid command')

class Peer:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

    def receive_file(self, file_path):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.ip_address, self.port))
            s.listen()
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode()
                if data.startswith('send_file:'):
                    sender_file_path = data.split(':')[1]
                    with open(file_path, 'wb') as f:
                        while True:
                            data = conn.recv(1024)
                            if not data:
                                break
                            f.write(data)
                elif data.startswith('request_file:'):
                    sender_file_path = data.split(':')[1]
                    with open(sender_file_path, 'rb') as f:
                        while True:
                            data = f.read(1024)
                            if not data:
                                break
                            conn.sendall(data)

    def send_file(self, file_path, dest_peer):
       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.ip_address, self.port))
            s.sendall(('send_file:' + file_path).encode())
            with open(file_path, 'wb') as f:
                while True:
                    data = s.recv(1024)
                    if not data:
                        break
                    f.write(data)
                    s.sendall(data)

if __name__ == '__main__':
    manager = Manager('127.0.0.1', 5000)
    manager.start()
