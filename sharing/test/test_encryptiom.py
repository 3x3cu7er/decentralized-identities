import tempfile
import os
from django.test import TestCase
from sharing.encryption import generate_key, encrypt_file, decrypt_file

class CryptoUtilsTest(TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)


        with open(self.temp_file.name, 'wb') as file:
            file.write(b'Test content for encryption')


    def test_encrypt_and_decrypt_file(self):

        # Generate a key for encryption:
        key = generate_key()

        # Encrypt the temporary file
        encrypt_file(self.temp_file.name, key)

        with open(self.temp_file.name, 'rb') as file:
            self.assertNotEqual(file.read(), b'')

        # Decrypt the encrypted file
        decrypt_file(self.temp_file.name, key)

        # Verify that the content is restored after decryption
        with open(self.temp_file.name, 'rb') as file:
            self.assertEqual(file.read(), b'Test content for encryption')

        def tearDown(self):
            os.remove(self.temp_file.name)

