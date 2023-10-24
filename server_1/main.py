import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 6116)
server_socket.bind(server_address)

server_socket.listen(5)
print('waiting for the connection...')
while True:
    client_socket, client_address = server_socket.accept()
    print('Client has joined')
    data = client_socket.recv(1024)
    if data:
        print(f"Received: {data.decode()}")
    message = "Hello, Client"
    client_socket.send(message.encode())