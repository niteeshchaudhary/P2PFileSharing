import socket
import threading
import time
import os

class Peer:
    def __init__(self, manager_ip, manager_port, listen_port, files_directory):
        self.manager_ip = manager_ip
        self.manager_port = manager_port
        self.listen_port = listen_port
        self.files_directory = files_directory

        self.active_peers = []
        self.shareable_files = []

        # Create a UDP socket to communicate with the manager
        self.manager_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Create a TCP socket to listen for incoming file transfer requests
        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.bind(('0.0.0.0', self.listen_port))
        self.listener_socket.listen()

        # Start the thread that listens for incoming file transfer requests
        self.file_transfer_thread = threading.Thread(target=self.check_for_file_transfer_requests)
        self.file_transfer_thread.start()

        # Ping the manager to get the list of active peers and shareable files
        self.ping_manager()
        
    def connect_to_manager(self):
        # create a socket object
        self.manager_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # get the IP address of the manager and connect to it
        manager_address = (self.manager_ip, self.manager_port)
        self.manager_socket.connect(manager_address)

        # send the peer's listening port to the manager
        message = f"JOIN {self.listen_port}"
        self.manager_socket.sendall(message.encode())

        # receive the list of active peers from the manager
        response = self.manager_socket.recv(4096).decode()
        active_peers = json.loads(response)

        # update the list of active peers
        self.active_peers = active_peers
        
    
    def send_message(self, message, address):
        """
        Send a message to a given address.
        """
        try:
            # Convert the message to bytes and send it to the given address.
            self.socket.sendto(message.encode(), address)
        except Exception as e:
            print(f"Error sending message to {address}: {e}")
    
    
    def broadcast_message(self, message):
        """
        Broadcasts a message to all connected peers.

        Args:
            message (str): The message to be broadcasted.
        """
        for address in self.active_peers:
            self.send_message(message, address)
            
    
    def get_active_peers(self):
        """
        Query the manager for a list of active peers and return the list.

        Returns:
            A list of tuples containing the IP address and port number of active peers.
        """
        message = {'type': 'query_peers'}
        response = self.send_message(message, (self.manager_ip, self.manager_port))

        if response is not None and response.get('type') == 'peer_list':
            peer_list = response.get('peer_list')
            return [(peer.get('ip_address'), peer.get('port')) for peer in peer_list]
        else:
            return []


    def get_shareable_files(self):
        """Get a list of files in the shared directory that can be shared with other peers."""
        shareable_files = []
        for file_name in os.listdir(self.files_directory):
            file_path = os.path.join(self.files_directory, file_name)
            # Check if the file is not a directory and is not already being shared
            if os.path.isfile(file_path) and file_name not in self.shared_files:
                shareable_files.append(file_name)
        return shareable_files
    
    def broadcast_file(self, file_name, file_path):
        file_size = os.path.getsize(file_path)
        message = f"FILE|{self.peer_ip}:{self.listen_port}|{file_name}|{file_size}"
        self.broadcast_message(message)

        with open(file_path, "rb") as file:
            while True:
                chunk = file.read(self.chunk_size)
                if not chunk:
                    break
                self.broadcast_message(chunk)
                
    
    def request_file(self, file_name):
        # Check if the requested file is already in the files directory
        if os.path.isfile(os.path.join(self.files_directory, file_name)):
            print(f"{file_name} already exists in {self.files_directory}")
            return

        # Check for active peers
        active_peers = self.get_active_peers()

        # Select a random active peer to request the file from
        if active_peers:
            peer_address = random.choice(active_peers)
            message = f"REQUEST_FILE {file_name}"
            self.send_message(message, peer_address)
            print(f"Requested {file_name} from {peer_address}")
        else:
            print("No active peers available to request the file from.")


    def run(self):
        # Connect to the manager and register with it
        self.connect_to_manager()
        self.register_with_manager()

        # Continuously check for incoming connections, messages, user input, and available files
        while True:
            self.check_for_incoming_connections()
            self.check_for_incoming_messages()
            self.check_for_user_input()
            self.check_for_available_peers()
            self.check_for_available_files()
            time.sleep(1)  # Sleep for 1 second before checking again
            
    
    def check_for_user_input(self):
        while True:
            user_input = input()

            if user_input == "list peers":
                active_peers = self.get_active_peers()
                print(f"Active Peers: {active_peers}")

            elif user_input == "list files":
                shareable_files = self.get_shareable_files()
                print(f"Shareable Files: {shareable_files}")

            elif user_input.startswith("request"):
                file_name = user_input.split(" ")[1]
                self.request_file(file_name)

            elif user_input.startswith("broadcast"):
                file_path = user_input.split(" ")[1]
                file_name = os.path.basename(file_path)
                self.broadcast_file(file_name, file_path)

            elif user_input == "help":
                print("Available Commands:")
                print("list peers - Lists active peers")
                print("list files - Lists shareable files")
                print("request <file_name> - Requests a file from available peers")
                print("broadcast <file_path> - Broadcasts a file to all connected peers")
                print("help - Shows available commands")

            else:
                print("Invalid command, type 'help' to see available commands")
        
    def check_for_incoming_connections(self):
        while True:
            try:
                # Wait for incoming connections
                conn, addr = self.listener.accept()
                
                # Add new connection to connections list
                self.connections.append(conn)
                
                print(f"Incoming connection from {addr}")
            except OSError:
                # Listener was closed, exit thread
                return
    
    def check_for_incoming_messages(self):
        while True:
            # Check if there are any messages in the message queue
            if not self.message_queue.empty():
                message, sender_address = self.message_queue.get()
                self.handle_message(message, sender_address)
            else:
                time.sleep(0.1)

    def check_for_available_peers(self):
        """
        This function is used to periodically check for available peers and add them to the self.peers dictionary
        """
        while True:
            try:
                # Get list of active peers from the manager
                response = self.send_message("GET_PEERS", (self.manager_ip, self.manager_port))
                active_peers = json.loads(response.decode())

                # Add active peers to peer list
                for peer in active_peers:
                    if peer not in self.peers.keys() and peer != self.listen_address:
                        self.peers[peer] = None

            except Exception as e:
                print(f"Error checking for available peers: {e}")

            # Wait for some time before checking again
            time.sleep(10)

    def check_for_available_files(self):
        # Get list of files in the shared directory
        files = os.listdir(self.files_directory)
        shareable_files = self.get_shareable_files()
        
        # Check for new files that are shareable
        new_files = [f for f in files if f not in self.shared_files and f in shareable_files]
        for file_name in new_files:
            file_path = os.path.join(self.files_directory, file_name)
            self.shared_files[file_name] = file_path
            self.broadcast_file(file_name, file_path)
            
        # Check for files that are no longer shareable
        for file_name in list(self.shared_files.keys()):
            if file_name not in files or file_name not in shareable_files:
                del self.shared_files[file_name]
                message = f"UNSHARE {file_name}"
                self.broadcast_message(message)










if __name__ == "__main__":
    # Initialize a new Peer object
    peer = Peer(manager_ip="127.0.0.1", manager_port=5000, listen_port=6000, files_directory="shared_files")

    # Connect to the Manager
    peer.connect_to_manager()

    # Start the main loop
    peer.run()