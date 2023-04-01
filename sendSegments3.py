import socket
import threading

# Define the buffer size for receiving data
BUFFER_SIZE = 1024
def send_segment(conn, file_path, segment_index, segment_size):
    # Open the file and seek to the start of the segment
    with open(file_path, 'rb') as f:
        f.seek(segment_index * segment_size)

        # Read the segment data from the file and send it to the requesting peer
        segment_data = f.read(segment_size)
        while segment_data:
            conn.send(segment_data)
            segment_data = f.read(segment_size)

    print(f"Segment {segment_index} sent.")

def serve_file_segment(file_path, segment_index, segment_size, port=8000):
    # Create a server socket and listen for connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('localhost', port))
        s.listen()

        print(f"Server listening on port {port}...")

        # Accept a connection from a peer and send the specified segment
        conn, addr = s.accept()

        print(f"Accepted connection from {addr[0]}:{addr[1]}")

        # Send the specified segment to the requesting peer
        send_segment(conn, file_path, segment_index, segment_size)

        # Close the connection
        #conn.close()

        print(f"Connection to {addr[0]}:{addr[1]} closed.")
if __name__ == '__main__':
    # Define the file path, segment index, and segment size
    file_path = 'file.txt'
    segment_index = 2
    segment_size = 2375

    # Serve the specified segment to a peer on port 8000
    serve_file_segment(file_path, segment_index, segment_size, port=8002)