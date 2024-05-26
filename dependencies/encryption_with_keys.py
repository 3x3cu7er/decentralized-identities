from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def generate_key_pair():
    """
    Generates a new RSA key pair.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_data(public_key, data):
    """
    Encrypts data using the given public key.
    """
    encrypted_data = public_key.encrypt(
        data.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_data

def decrypt_data(private_key, encrypted_data):
    """
    Decrypts data using the given private key.
    """
    decrypted_data = private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_data.decode()
# Generate key pair for User A
private_key_userA, public_key_userA = generate_key_pair()

# # User A sends their public key to User B via email
# print("Email content for User B:")
# print("Subject: Public Key for Encryption")
# print("Body:")
# public_key_pem_userA = public_key_userA.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# ).decode()
# print(public_key_pem_userA)

# # User B receives User A's public key via email and generates their own key pair
# # Assume User B reads the email and extracts User A's public key from it
# received_public_key_userA = serialization.load_pem_public_key(
#     public_key_pem_userA.encode(),
#     backend=default_backend()
# )

# # Generate key pair for User B
# private_key_userB, public_key_userB = generate_key_pair()

# # User B sends their public key to User A via email
# print("\nEmail content for User A:")
# print("Subject: Public Key for Encryption")
# print("Body:")
# public_key_pem_userB = public_key_userB.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# ).decode()
# print(public_key_pem_userB)

# # User A receives User B's public key via email and extracts it
# received_public_key_userB = serialization.load_pem_public_key(
#     public_key_pem_userB.encode(),
#     backend=default_backend()
# )

# Data to be encrypted by User A and sent to User B
data_to_encrypt = "Hello, User B! This is a message from User A."

# # Encrypt the data with User B's public key
# encrypted_data = encrypt_data(received_public_key_userB, data_to_encrypt)
# print("\nEncrypted data to be sent to User B:", encrypted_data)

# User B decrypts the data using their private key
# decrypted_data = decrypt_data(private_key_userB, encrypted_data)
# print("Decrypted data by User B:", decrypted_data)

# # Data to be encrypted by User B and sent to User A
# data_to_encrypt = "Hi, User A! This is a response from User B."

# # Encrypt the data with User A's public key
# encrypted_data = encrypt_data(received_public_key_userA, data_to_encrypt)
# print("\nEncrypted data to be sent to User A:", encrypted_data)

# # User A decrypts the data using their private key
# decrypted_data = decrypt_data(private_key_userA, encrypted_data)
# print("Decrypted data by User A:", decrypted_data)


