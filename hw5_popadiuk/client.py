import socket
import struct


def receive_message(server_socket):
    # Receive the length of the message
    length_header = server_socket.recv(4)
    if not length_header:
        return None

    # Unpack the length from binary to integer
    message_length = struct.unpack("!I", length_header)[0]

    # Receive the actual message
    data = server_socket.recv(message_length)
    return data.decode()


def send_message(server_socket, message):
    # Pack the length of the message as binary
    length_header = struct.pack("!I", len(message))

    # Send the length header
    server_socket.sendall(length_header)

    # Send the actual message
    server_socket.sendall(message.encode())


# Client setup
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 6116)
client_socket.connect(server_address)

# Send and receive 100 messages
for i in range(100):
    send_message(client_socket, f"Hello, Server {i}")
    received_message = receive_message(client_socket)
    if received_message:
        print(f"Received: {received_message}")

# Close the connection
client_socket.close()
