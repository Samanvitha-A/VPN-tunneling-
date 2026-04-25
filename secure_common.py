# secure_common.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes, hmac, padding
import os

AES_KEY = os.urandom(32)  # 256-bit key
HMAC_KEY = os.urandom(32)

def encrypt_message(message: bytes):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    h = hmac.HMAC(HMAC_KEY, hashes.SHA256())
    h.update(iv + ciphertext)
    tag = h.finalize()
    return iv + ciphertext + tag

def decrypt_message(data: bytes):
    iv = data[:16]
    ciphertext = data[16:-32]
    tag = data[-32:]
    h = hmac.HMAC(HMAC_KEY, hashes.SHA256())
    h.update(iv + ciphertext)
    h.verify(tag)
    cipher = Cipher(algorithms.AES(AES_KEY), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded_plaintext) + unpadder.finalize()
