import socket
import struct


def receive_message(client_socket):
    # Receive the length of the message
    length_header = client_socket.recv(4)
    if not length_header:
        return None

    # Unpack the length from binary to integer
    message_length = struct.unpack("!I", length_header)[0]

    # Receive the actual message
    data = client_socket.recv(message_length)
    return data.decode()


def send_message(client_socket, message):
    # Pack the length of the message as binary
    length_header = struct.pack("!I", len(message))

    # Send the length header
    client_socket.sendall(length_header)

    # Send the actual message
    client_socket.sendall(message.encode())


# Server setup
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('127.0.0.1', 6116)
server_socket.bind(server_address)
server_socket.listen(5)
print('Waiting for the connection...')

while True:
    client_socket, client_address = server_socket.accept()
    print('Client has joined')

    # Receive and print 100 messages
    for _ in range(100):
        received_message = receive_message(client_socket)
        if received_message:
            print(f"Received: {received_message}")

        # Respond with a different message
        send_message(client_socket, f"Server says: Thanks for the message {_}")

    # Close the connection
    client_socket.close()
