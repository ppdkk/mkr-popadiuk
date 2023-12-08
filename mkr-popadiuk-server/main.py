import socket
import numpy as np
import json
import threading

def matrix_multiply(matrix1, matrix2):
    result = np.dot(matrix1, matrix2)
    return result.tolist()

def receive_data(client_socket):
    # Receive the size of the incoming data
    size_bytes = client_socket.recv(4)
    size = int.from_bytes(size_bytes, byteorder='big')

    data_chunks = []
    while size > 0:
        chunk = client_socket.recv(min(size, 8192))
        if not chunk:
            break
        data_chunks.append(chunk)
        size -= len(chunk)

    # Combine the chunks and decode the JSON data
    received_data = json.loads(b''.join(data_chunks).decode('utf-8'))
    return received_data

def send_response(client_socket, response_data):
    try:
        # Prepare the response data
        json_data = json.dumps(response_data).encode('utf-8')

        # Send the size of the data first
        client_socket.send(len(json_data).to_bytes(4, byteorder='big'))

        # Send the data
        for i in range(0, len(json_data), 8192):
            client_socket.send(json_data[i:i+8192])

    except ConnectionResetError:
        print("Connection closed by the client.")
    finally:
        # Close the client socket
        client_socket.close()

def handle_client(client_socket):
    try:
        # Receive data from the client
        received_data = receive_data(client_socket)

        # Extract matrix dimensions and elements
        size1, size2, matrix1, matrix2 = (
            received_data['size1'],
            received_data['size2'],
            received_data['matrix1'],
            received_data['matrix2']
        )

        # Check if matrices can be multiplied
        if size1[1] != size2[0]:
            raise ValueError("Matrix size mismatch. Cannot perform multiplication.")

        # Perform matrix multiplication
        result_matrix = matrix_multiply(np.array(matrix1), np.array(matrix2))

        # Print the input matrices and the result matrix
        print("Matrix1:")
        print(np.array(matrix1))
        print("\nMatrix2:")
        print(np.array(matrix2))
        print("\nResult Matrix:")
        print(np.array(result_matrix))

        # Send the result back to the client
        response_data = {'result': result_matrix}
        send_response(client_socket, response_data)

    except Exception as e:
        # Handle errors and send an error response to the client
        error_message = str(e)
        response_data = {'error': error_message}
        send_response(client_socket, response_data)

    finally:
        # Close the client socket
        client_socket.close()

def start_server():
    host = '127.0.0.1'
    port = 12345

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Accepted connection from {addr}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
