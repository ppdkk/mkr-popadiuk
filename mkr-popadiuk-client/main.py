import socket
import numpy as np
import json

def generate_random_matrix(rows, cols):
    return np.random.randint(1, 10, size=(rows, cols)).tolist()

def receive_data_from_server(client_socket):
    size_bytes = client_socket.recv(4)
    size = int.from_bytes(size_bytes, byteorder='big')
    data_chunks = []
    while size > 0:
        chunk = client_socket.recv(min(size, 8192))
        if not chunk:
            break
        data_chunks.append(chunk)
        size -= len(chunk)
    received_data = b''.join(data_chunks)
    return received_data

def send_data_to_server(host, port, size1, size2, matrix1, matrix2):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

    
        data = {'size1': size1, 'size2': size2, 'matrix1': matrix1, 'matrix2': matrix2}
        json_data = json.dumps(data).encode('utf-8')

        # Передаєм розміри і дані
        client_socket.send(len(json_data).to_bytes(4, byteorder='big'))

        for i in range(0, len(json_data), 8192):
            client_socket.send(json_data[i:i+8192])

        # отримання результату
        received_data = receive_data_from_server(client_socket)

        # декодування
        result_data = json.loads(received_data)

        # перевірка на помилки
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
        client_socket.close()

if __name__ == "__main__":
    host = '127.0.0.1'
    port = 12345

    # генерація матриць та розмірів
    size1 = (np.random.randint(1000, 1500), np.random.randint(1000, 1500))
    size2 = (size1[1], np.random.randint(1000, 1500))

    matrix1 = generate_random_matrix(size1[0], size1[1])
    matrix2 = generate_random_matrix(size2[0], size2[1])

    # вивід матриць
    print("Input Matrix1:")
    print(np.array(matrix1))
    print("\nInput Matrix2:")
    print(np.array(matrix2))

    # надсилання даних
    send_data_to_server(host, port, size1, size2, matrix1, matrix2)
