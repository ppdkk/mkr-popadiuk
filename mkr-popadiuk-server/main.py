import socket
import numpy as np
import json
import threading

def matrix_multiply(matrix1, matrix2):
    result = np.dot(matrix1, matrix2)
    return result.tolist()

def receive_data(client_socket):
    # отримання розмірів та матриць
    size_bytes = client_socket.recv(4)
    size = int.from_bytes(size_bytes, byteorder='big')

    data_chunks = []
    while size > 0:
        chunk = client_socket.recv(min(size, 8192))
        if not chunk:
            break
        data_chunks.append(chunk)
        size -= len(chunk)

    # декодування JSON 
    received_data = json.loads(b''.join(data_chunks).decode('utf-8'))
    return received_data

def send_response(client_socket, response_data):
    try:
        json_data = json.dumps(response_data).encode('utf-8')

        # розмір даних
        client_socket.send(len(json_data).to_bytes(4, byteorder='big'))

        # надсилання
        for i in range(0, len(json_data), 8192):
            client_socket.send(json_data[i:i+8192])

    except ConnectionResetError:
        print("Connection closed by the client.")
    finally:
        #  закриваєм сокет
        client_socket.close()

def handle_client(client_socket):
    try:
        # отримання даних від клієнта
        received_data = receive_data(client_socket)

        size1, size2, matrix1, matrix2 = (
            received_data['size1'],
            received_data['size2'],
            received_data['matrix1'],
            received_data['matrix2']
        )

        # перевірка чи можливе множення
        if size1[1] != size2[0]:
            raise ValueError("Matrix size mismatch. Cannot perform multiplication.")

        # множення
        result_matrix = matrix_multiply(np.array(matrix1), np.array(matrix2))

        # Print the input matrices and the result matrix
        print("Matrix1:")
        print(np.array(matrix1))
        print("\nMatrix2:")
        print(np.array(matrix2))
        print("\nResult Matrix:")
        print(np.array(result_matrix))

        # надсилаєм рези
        response_data = {'result': result_matrix}
        send_response(client_socket, response_data)

    except Exception as e:
        # надсилаємо текст помилки
        error_message = str(e)
        response_data = {'error': error_message}
        send_response(client_socket, response_data)

    finally:
        # закриваємо сокет
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
        client_thread = threading.Thread(target=handle_client, args=(client_socket,)) #поток для клієнта
        client_thread.start()

if __name__ == "__main__":
    start_server()
