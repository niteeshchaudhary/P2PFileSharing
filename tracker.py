import socket
import threading
import time

# Define the host and port for the manager server
HOST = 'localhost'
PORT = 5000

# Define the maximum number of clients the manager server can handle
MAX_CLIENTS = 10

# List to keep track of active clients
ACTIVE_CLIENTS = {}
maping = {}

def flfunc(key):
    global ACTIVE_CLIENTS
    #print(key)
    return ACTIVE_CLIENTS[key]!=""

# Function to handle client connections
def handle_client(conn, addr):
    global ACTIVE_CLIENTS
    gservport=""
    # Add the client to the list of active clients
    while True:
        try:
            #conn.settimeout(15)
        # Receive data from the client
            data = conn.recv(1024).decode()
            dtl=data.split()
            # If the client has disconnected, remove them from the active client list and break the loop
            if dtl[0]=="CONNECT":
                maping[addr]=dtl[1]
                gservport=dtl[1]
                ACTIVE_CLIENTS[dtl[1]]=conn
                print(f"New connection from {addr}.Serves at {dtl[1]}. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")
                
            elif dtl[0]=="DISCONNECT":
                print("yes")
                gservport=maping[addr]
                ACTIVE_CLIENTS[gservport]=""
                print(f"disconnected from {addr} closed.No Service at {gservport} Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")
                conn.close()
                break
            
            for servport,client in ACTIVE_CLIENTS.items():
                if client != conn and client!="":
                    try:
                        client.sendall(f"Active clients: {list(filter(flfunc, ACTIVE_CLIENTS.keys()))}".encode())
                    except:
                        ACTIVE_CLIENTS[servport]=""
                        print(f"Connection from {client.getpeername()} closed. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")
            time.sleep(5)
        except:
            if gservport!="" and ACTIVE_CLIENTS[gservport]==conn:
                ACTIVE_CLIENTS[gservport]=""
                print(f"Connection from {addr} closed. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")
                conn.close()
                break
            
    # Broadcast the updated active client list to all connected clients
    for servport,client in ACTIVE_CLIENTS.items():
            if client != conn and client!="":
                try:
                    client.sendall(f"Active clients: {list(filter(flfunc, ACTIVE_CLIENTS.keys()))}".encode())
                except:
                    ACTIVE_CLIENTS[servport]=""
                    print(f"Connection from {client.getpeername()} closed. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")

    print(f"Connection from {addr} closed. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")
    # Close the connection

# Function to periodically check for available clients
def check_clients():
    global ACTIVE_CLIENTS

    while True:
        time.sleep(20)

        # Check each active client to see if they are still connected
        for servport,client in ACTIVE_CLIENTS.items():
            try:
                if client!="":
                    client.sendall("PING".encode())
            except:
                # If the client is not responding, remove them from the active client list and print a message
                ACTIVE_CLIENTS[servport]=""
                print(f"Connection from {client.getpeername()} closed. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")

        # Broadcast the updated active client list to all connected clients
        for servport,client in ACTIVE_CLIENTS.items():
            try:
                if client!="":
                    client.sendall(f"Active clients: {list(filter(flfunc, ACTIVE_CLIENTS.keys()))}".encode())
            except:
                # If the client is not responding, remove them from the active client list and print a message
                if ACTIVE_CLIENTS[servport]!="":
                    ACTIVE_CLIENTS[servport]=""
                    print(f"Connection from {client.getpeername()} closed. Total active clients: {len(list(filter(flfunc, ACTIVE_CLIENTS.keys())))}")

# Main function to start the manager server
def main():
    # Create the server socket and bind it to the host and port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))

    # Start listening for incoming connections
    server_socket.listen(MAX_CLIENTS)
    print(f"Manager server started on {HOST}:{PORT}")

    # Start a separate thread to periodically check for available clients
    check_thread = threading.Thread(target=check_clients)
    check_thread.start()

    # Main loop to handle incoming connections
    
    while True:
        # Accept an incoming connection
        conn, addr = server_socket.accept()

        # Start a new thread to handle the connection
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

    # Close the server socket when the program ends
    server_socket.close()

if __name__ == "__main__":
    main()
