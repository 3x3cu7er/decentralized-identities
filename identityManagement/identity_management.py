import re
import logging
from cryptography.fernet import Fernet
from datetime import datetime, timedelta

class IdentityManagement:
    def __init__(self):
        self.identities = {}
        self.crypto_key = Fernet.generate_key()
        self.cipher = Fernet(self.crypto_key)
        self.shared_data = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        logger = logging.getLogger("IdentityManagementLogger")
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler = logging.FileHandler("identity_management.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def register_identity(self, ethereum_address, name, email):
        if ethereum_address not in self.identities:
            self.identities[ethereum_address] = {'name': name, 'email': self._encrypt(email), 'verified': False}
            self.logger.info(f"Identity registered: Address - {ethereum_address}, Name - {name}, Email - {email}")

    def share_data(self, owner_address, receiver_address, data):
        if owner_address in self.identities and receiver_address in self.identities:
            if self._is_owner(owner_address) or self._is_admin(owner_address):
                if receiver_address not in self.shared_data:
                    self.shared_data[receiver_address] = []

                expiry_date = datetime.now() + timedelta(days=30)
                self.shared_data[receiver_address].append({'owner_address': owner_address, 'data': data, 'expiry_date': expiry_date})
                self.logger.info(f"Data shared: Owner - {owner_address}, Receiver - {receiver_address}, Data - {data}")

    def access_shared_data(self, address):
        current_time = datetime.now()
        if address in self.shared_data:
            return [item for item in self.shared_data[address] if item['expiry_date'] > current_time]
        return []

    def revoke_shared_data(self, owner_address, receiver_address):
        if receiver_address in self.shared_data:
            self.shared_data[receiver_address] = [item for item in self.shared_data[receiver_address] if item['owner_address'] != owner_address]
            self.logger.info(f"Data revoked: Owner - {owner_address}, Receiver - {receiver_address}")

    def _is_valid_address(self, address):
        return isinstance(address, str) and re.match('^0x[a-fA-F0-9]{40}$', address)

    def _encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def _decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def _is_owner(self, owner_address):
        return owner_address in self.identities and not self.identities[owner_address]['verified']

    def _is_admin(self, address):
        return address in self.identities and self.identities[address]['verified'] and self.identities[address]['name'] == 'Admin'
