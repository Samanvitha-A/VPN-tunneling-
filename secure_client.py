import socket
from cryptography.fernet import Fernet
import hashlib

# Load shared key from file
with open("secret.key", "rb") as key_file:
    key = key_file.read()

fernet = Fernet(key)

HOST = '127.0.0.1'
PORT = 65433  # Must match server port

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("[CLIENT] Connected to the server.")

while True:
    message = input("Enter message (or 'exit' to quit): ")
    if message.lower() == "exit":
        break

    sha_hash = hashlib.sha256(message.encode()).hexdigest()
    print(f"[CLIENT] SHA256 hash: {sha_hash}")

    encrypted_message = fernet.encrypt(message.encode())
    print(f"[CLIENT] Encrypted data: {encrypted_message}")

    client_socket.sendall(encrypted_message)

    encrypted_response = client_socket.recv(1024)
    decrypted_response = fernet.decrypt(encrypted_response).decode()
    print(f"[CLIENT] Server says: {decrypted_response}")

client_socket.close()
