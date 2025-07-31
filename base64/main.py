import base64

def encode_base64(data: str) -> str:
    encoded_bytes = base64.b64encode(data.encode('utf-8'))
    return encoded_bytes.decode('utf-8')

def decode_base64(encoded_data: str) -> str:
    try:
        decoded_bytes = base64.b64decode(encoded_data.encode('utf-8'))
        return decoded_bytes.decode('utf-8')
    except Exception as e:
        return f"Decoding failed: {e}"

def main():
    print("Choose an option:")
    print("1. Encode to Base64")
    print("2. Decode from Base64")
    choice = input("Enter 1 or 2: ")

    if choice == '1':
        data = input("Enter string to encode: ")
        encoded = encode_base64(data)
        print(f"Encoded Base64: {encoded}")
    elif choice == '2':
        encoded_data = input("Enter Base64 string to decode: ")
        decoded = decode_base64(encoded_data)
        print(f"Decoded string: {decoded}")
    else:
        print("Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()
