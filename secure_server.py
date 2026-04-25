import socket
from cryptography.fernet import Fernet
import hashlib

# Generate or load a shared key
key = Fernet.generate_key()
fernet = Fernet(key)

# Save key so client can read it
with open("secret.key", "wb") as key_file:
    key_file.write(key)

HOST = '127.0.0.1'
PORT = 65433  # You can change if needed

# Create TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)
print("[SERVER] Listening for incoming connection...")

conn, addr = server_socket.accept()
print(f"[SERVER] Connected by {addr}")

while True:
    encrypted_data = conn.recv(1024)
    if not encrypted_data:
        break

    decrypted_data = fernet.decrypt(encrypted_data).decode()
    sha_hash = hashlib.sha256(decrypted_data.encode()).hexdigest()

    print(f"[SERVER] Received (decrypted): {decrypted_data}")
    print(f"[SERVER] Integrity SHA256: {sha_hash}")

    response = f"Server received: {decrypted_data}"
    encrypted_response = fernet.encrypt(response.encode())
    conn.sendall(encrypted_response)

conn.close()
server_socket.close()
