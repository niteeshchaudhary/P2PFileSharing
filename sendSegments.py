import socket
import threading
import os
# Define the buffer size for receiving data
BUFFER_SIZE = 1024
def send_segment(conn, file_path, segment_start, segment_end):
    # Open the file and seek to the start of the segment
    with open(file_path, 'rb') as f:
        f.seek(segment_start)

        # Read the segment data from the file and send it to the requesting peer
        segment_size=segment_end-segment_start
        segment_data = f.read(segment_size)
        while segment_data:
            conn.send(segment_data)
            segment_data = f.read(segment_size)

    print(f"Segment start: {segment_start} sent.")
    
def handle_client(conn, addr):
    
    try:
        data=conn.recv(1024).decode()
        print(data)
        if data.startswith("GET"):
            print("GET request received")
            file_path=data.split()[1]
            print(file_path)
            file_size=os.path.getsize(file_path)
            print(file_size)
            segment_start=int(data.split()[2])
            print(segment_start)
            segment_end=int(data.split()[3])
            print(segment_end)
            send_segment(conn, file_path, segment_start,segment_end)
            conn.close()
            print(f"Connection to {addr[0]}:{addr[1]} closed.")
            
    except socket.timeout:
        print('Request timed out')
        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Send the specified segment to the requesting peer
        #send_segment(conn, file_path, segment_start,segment_end)

        # Close the connection
        # conn.close()

        print(f"Connection to {addr[0]}:{addr[1]} closed.")

def serve_file_segment(port=8000):
    # Create a server socket and listen for connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen(10)

        print(f"Server listening on port {port}...")

        # Accept a connection from a peer and send the specified segment
        while True:
            conn, addr = s.accept()
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.start()
               

if __name__ == '__main__':
    # Define the file path, segment index, and segment size
    #file_path = 'file.txt'
    # segment_index = 0
    # segment_size = 2375
    # file_size = os.path.getsize(file_path)
    # print(file_size)
    # Serve the specified segment to a peer on port 8000
    serve_file_segment(port=8000)