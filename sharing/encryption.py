from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_file(file_path, key):

    # Read the content: (read)
    with open(file_path, 'rb') as file:
        plaintext = file.read()

    # Encrypt plain text:
    fernet = Fernet(key)
    ciphertext = fernet.encrypt(plaintext)

    # Write the encrypted content: (rewrite)
    with open(file_path, 'wb') as encrypted_file:
        encrypted_file.write(ciphertext)


def decrypt_file(file_path, key):

    # read the cipher text:
    with open(file_path, 'rb') as file:
        ciphertext = file.read()

    # decrypt using the same key:
    fernet = Fernet(key)
    plaintext = fernet.decrypt(ciphertext)

    # write the plain text
    with open(file_path, 'wb') as decrypted_file:
        decrypted_file.write(plaintext)

