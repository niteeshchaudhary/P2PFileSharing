import socket
import threading
import os

# Define the buffer size for receiving data
BUFFER_SIZE = 1024

def fetch_segment(peer_ip,file_download, peer_port, start_byte, end_byte, segment_data):
    # Create a TCP socket for connecting to the peer
    peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the peer's IP address and port
    peer_socket.connect((peer_ip, peer_port))

    # Send a request for the specified segment of the file
    request = f"GET {file_download} {start_byte} {end_byte}"
    peer_socket.send(request.encode())

    # Receive the segment data from the peer
    segment_data_part = b''
    while len(segment_data_part) < end_byte - start_byte:
        try:
            data = peer_socket.recv(BUFFER_SIZE)
            if not data:
                break
            segment_data_part += data
        except Exception as e:
            print("Error" + str(e))
            break
    segment_data[start_byte]=segment_data_part
    # Close the socket
    #peer_socket.close()
    return segment_data_part

def fetch_file(segments,file_download, save_path):
    # Initialize a dictionary to store the segment data
    segment_data = {}

    # Create a list of threads to fetch each segment from a different peer
    threads = []
    for i, (peer_ip, peer_port, start_byte, end_byte) in enumerate(segments):
        # Create a new thread to fetch the segment from the peer
        thread = threading.Thread(target=fetch_segment, args=(peer_ip,file_download, peer_port, start_byte, end_byte, segment_data))
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Write the fetched file segments to disk
    with open(save_path, 'wb') as f:
        for i in range(len(segments)):
            f.write(segment_data[segments[i][2]])

# Example usage:
# Define the file segments to fetch from multiple peers
file_path = 'file.txt'
download_path = 'receive_file.txt'
file_size = os.path.getsize(file_path)
segments = [
    ('localhost', 8000, 0, 2374),
    ('localhost', 8001, 2375, 4749),
    ('localhost', 8002, 4750, 7124),
    ('localhost', 8003, 7125, 9499)
]

# Fetch the file segments from multiple peers in parallel
fetch_file(segments,file_path,download_path)
