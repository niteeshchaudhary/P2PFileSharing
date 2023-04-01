import socket

# def getActiveConnection():
#     # Number of active connections
    
    

# connect to socket
server_socket =socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port=8080
timeout = 1 
server_address=('localhost', port)
print('starting up on %s port %s' % server_address)
server_socket.bind(server_address)
# Listen for incoming connections
server_socket.listen(10)

while True:
    # Wait for a connection
    
    print( 'waiting for a connection')
    connection, client_address = server_socket.accept()
    try:
        print( 'connection from', client_address)

        # Receive the data in small chunks and retransmit it
        while True:
            #server_socket.settimeout(timeout)
            data = connection.recv(16).decode()
            print( 'received "%s"' % data)
            if data:
                print( 'sending data back to the client')
                connection.sendall(data.encode())
            else:
                print( 'no more data from', client_address)
                break
            
    finally:
        # Clean up the connection
        connection.close()

    
