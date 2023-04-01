import socket

'''client socket'''
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect the socket to the port where the server is listening
server_address = ('localhost', 5000)
print('connecting to %s port %s' % server_address)
client_socket.connect(server_address)

try:
    
    # Send data
    message = 'This is NKC'
    print( 'sending "%s"' % message)
    client_socket.sendall(message.encode())

    # Look for the response
    amount_received = 0
    amount_expected = len(message)
    
    while amount_received < amount_expected:
        data = client_socket.recv(16).decode()
        amount_received += len(data)
        print('received "%s"' % data)

finally:
    print ('closing socket')
    client_socket.close()