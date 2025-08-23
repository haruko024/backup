import datetime
import random

# Random shift for encryption
r = random.randint(1, 1000)

def encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    print(f"🔐 Shift used: {shift}")
    return result

def decrypt(text, shift):
    return encrypt(text, -shift)

def log_action(action, text, result, shift):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if action == "ENCRYPT":
        logfile = "encrypt_log.txt"
    else:
        logfile = "decrypt_log.txt"

    with open(logfile, "a") as log:
        log.write(f"[{timestamp}] {action} | Shift: {shift} | Input: {text} | Output: {result}\n")

if __name__ == "__main__":
    print("=== Falcon Encryption Tool ===")
    print("1. Encrypt a message")
    print("2. Decrypt a message")

    choice = input("Select option (1/2): ").strip()

    if choice == "1":
        msg = input("Enter text to encrypt: ")
        encrypted = encrypt(msg, r)
        print("🔐 Encrypted:", encrypted)
        log_action("ENCRYPT", msg, encrypted, r)

    elif choice == "2":
        shift = int(input("Enter shift number: "))  # convert to int
        msg = input("Enter text to decrypt: ")
        decrypted = decrypt(msg, shift)
        print("✅ Decrypted:", decrypted)
        log_action("DECRYPT", msg, decrypted, shift)

    else:
        print("Invalid choice!")
