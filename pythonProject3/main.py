import socket
import numpy as np
import json

def generate_random_matrix(rows, cols):
    return np.random.randint(1, 10, size=(rows, cols)).tolist()

def receive_data_from_server(client_socket):
    # Receive the size of the incoming data
    size_bytes = client_socket.recv(4)
    size = int.from_bytes(size_bytes, byteorder='big')

    # Receive the data in chunks
    data_chunks = []
    while size > 0:
        chunk = client_socket.recv(min(size, 8192))
        if not chunk:
            break
        data_chunks.append(chunk)
        size -= len(chunk)

    # Combine the chunks (binary data) without decoding
    received_data = b''.join(data_chunks)
    return received_data

def send_data_to_server(host, port, size1, size2, matrix1, matrix2):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        # Prepare data to send to the server
        data = {'size1': size1, 'size2': size2, 'matrix1': matrix1, 'matrix2': matrix2}
        json_data = json.dumps(data).encode('utf-8')

        # Send the size of the data first
        client_socket.send(len(json_data).to_bytes(4, byteorder='big'))

        # Send the data in chunks
        for i in range(0, len(json_data), 8192):
            client_socket.send(json_data[i:i+8192])

        # Receive the result from the server
        received_data = receive_data_from_server(client_socket)

        # Deserialize the binary data without decoding as UTF-8
        result_data = json.loads(received_data)

        # Check for errors
        if 'error' in result_data:
            print(f"Error from server: {result_data['error']}")
        else:
            print("\nInput Matrix1:")
            print(np.array(matrix1))
            print("\nInput Matrix2:")
            print(np.array(matrix2))
            print("\nResult from server:")
            print(np.array(result_data['result']))

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345

    # Generate random matrix sizes and elements
    size1 = (np.random.randint(1000, 1500), np.random.randint(1000, 1500))
    size2 = (size1[1], np.random.randint(1000, 1500))

    matrix1 = generate_random_matrix(size1[0], size1[1])
    matrix2 = generate_random_matrix(size2[0], size2[1])

    # Print the input matrices and the result matrix
    print("Input Matrix1:")
    print(np.array(matrix1))
    print("\nInput Matrix2:")
    print(np.array(matrix2))

    # Send data to the server
    send_data_to_server(host, port, size1, size2, matrix1, matrix2)
