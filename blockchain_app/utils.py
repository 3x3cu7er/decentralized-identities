# utils.py

from django.core.mail import send_mail
from django.urls import reverse

def send_verification_email(email, token):
    verification_link = reverse('verify_account', kwargs={'token': token})
    verification_url = f'http://yourdomain.com{verification_link}'  # Replace 'yourdomain.com' with your actual domain
    message = f'Click the link to verify your account: {verification_url}'
    send_mail('Verify Your Account', message, 'from@example.com', [email])


from cryptography.fernet import Fernet

# Generate a secret key for encryption
def generate_key():
    return Fernet.generate_key()

# Initialize the Fernet cipher with the provided key
def initialize_cipher(key):
    return Fernet(key)

# Encrypt data using the initialized cipher
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# def encrypt_data(data, key):
#     cipher = AES.new(key, AES.MODE_CBC)
#     ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
#     iv = base64.b64encode(cipher.iv).decode('utf-8')
#     ct = base64.b64encode(ct_bytes).decode('utf-8')
#     return iv, ct
def encrypt_data(data, key):
    # Convert data to bytes
    if isinstance(data, str):
        data = data.encode('utf-8')  # Assuming UTF-8 encoding, change if necessary

    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data, AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt_data(iv, ct, key):
    cipher = AES.new(key, AES.MODE_CBC, base64.b64decode(iv))
    pt = unpad(cipher.decrypt(base64.b64decode(ct)), AES.block_size)
    return pt.decode('utf-8')

# Example usage:
key = get_random_bytes(16)  # Generate a random 128-bit key
# data_to_encrypt = "Hello,  World!, encrypted data mmmmmmmmmmmmmmmmmmmmmmmmmmmmmfdfddffd"
# iv, ciphertext = encrypt_data(data_to_encrypt, key)
# print("Encrypted data:", ciphertext)

# decrypted_data = decrypt_data(iv, ciphertext, key)
# print("Decrypted data:", decrypted_data)
# print(iv)
