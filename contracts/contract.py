import re
import logging
from cryptography.fernet import Fernet

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

    def register_identity(self):
        while True:
            owner_address = input("Enter owner Ethereum address (starting with '0x'): ").strip()
            if self._is_valid_address(owner_address):
                break
            else:
                print("Invalid Ethereum address format. Please try again.")

        name = input("Enter name: ").strip()
        email = input("Enter email address: ").strip()
        if not self._is_valid_email(email):
            print("Invalid email address format.")
            return

        if owner_address not in self.identities:
            self.identities[owner_address] = {'name': name, 'email': self._encrypt(email), 'verified': False}
            print(f"Identity for {name} registered successfully.")
            self.logger.info(f"Identity registered: Address - {owner_address}, Name - {name}, Email - {email}")
        else:
            print("Identity already registered.")

    def share_data(self):
        while True:
            owner_address = input("Enter owner Ethereum address (starting with '0x'): ").strip()
            if self._is_valid_address(owner_address):
                break
            else:
                print("Invalid Ethereum address format. Please try again.")

        while True:
            receiver_address = input("Enter receiver Ethereum address (starting with '0x'): ").strip()
            if self._is_valid_address(receiver_address):
                break
            else:
                print("Invalid Ethereum address format. Please try again.")

        data = input("Enter data to share: ").strip()

        if owner_address in self.identities and receiver_address in self.identities:
            if self._is_owner(owner_address) or self._is_admin(owner_address):
                if receiver_address not in self.shared_data:
                    self.shared_data[receiver_address] = []

                self.shared_data[receiver_address].append({'owner_address': owner_address, 'data': data})
                print(f"Data shared successfully with {receiver_address}.")
                self.logger.info(f"Data shared: Owner - {owner_address}, Receiver - {receiver_address}, Data - {data}")
            else:
                print("Not authorized to share data.")
        else:
            print("One or both addresses not found.")

    def access_shared_data(self, address):
        if address in self.shared_data:
            print(f"Shared data for {address}:")
            for shared_item in self.shared_data[address]:
                print(f"Owner: {shared_item['owner_address']}, Data: {shared_item['data']}")
                self.logger.info(f"Accessed shared data: Address - {address}, Owner - {shared_item['owner_address']}, Data - {shared_item['data']}")
        else:
            print("No shared data found for this address.")
            self.logger.warning(f"No shared data found: Address - {address}")

    def _is_valid_address(self, address):
        return isinstance(address, str) and re.match('^0x[a-fA-F0-9]{40}$', address)

    def _is_valid_email(self, email):
        return isinstance(email, str) and re.match('[^@]+@[^@]+\.[^@]+', email)

    def _encrypt(self, data):
        return self.cipher.encrypt(data.encode()).decode()

    def _decrypt(self, encrypted_data):
        return self.cipher.decrypt(encrypted_data.encode()).decode()

    def _is_owner(self, owner_address):
        return owner_address in self.identities and not self.identities[owner_address]['verified']

    def _is_admin(self, address):
        return address in self.identities and self.identities[address]['verified'] and self.identities[address]['name'] == 'Admin'
    



    def is_owner(self, owner_address):
        return owner_address in self.identities and not self.identities[owner_address]['verified']

    def is_admin(self, address):
        return address == 'admin'






    def _encrypt_email(self, email):
        # Dummy encryption for demonstration purposes
        return email[::-1]  # Reverse the email string as an example of encryption

    def _decrypt_email(self, encrypted_email):
        # Dummy decryption for demonstration purposes
        return encrypted_email[::-1]  # Reverse the encrypted email string to decrypt





    def _is_valid_email(self, email):
        return isinstance(email, str) and re.match('[^@]+@[^@]+\.[^@]+', email)



    def update_identity(self):
        owner_address = input("Enter owner Ethereum address to update identity: ").strip()
        if not self._is_valid_address(owner_address):
            print("Invalid Ethereum address format.")
            return

        if owner_address in self.identities:
            if self._is_owner(owner_address):
                name = input("Enter updated name: ").strip()
                email = input("Enter updated email address: ").strip()
                if not self._is_valid_email(email):
                    print("Invalid email address format.")
                    return

                self.identities[owner_address]['name'] = name
                self.identities[owner_address]['email'] = self._encrypt(email)
                print("Identity updated successfully.")
            else:
                print("Not authorized to update identity.")
        else:
            print("Identity not found.")

    def verify_identity(self):
        owner_address = input("Enter owner Ethereum address to verify: ").strip()
        if not self._is_valid_address(owner_address):
            print("Invalid Ethereum address format.")
            return

        verifier_address = input("Enter verifier Ethereum address: ").strip()
        if not self._is_valid_address(verifier_address):
            print("Invalid Ethereum address format.")
            return

        if owner_address in self.identities:
            if self._is_owner(owner_address) or self._is_admin(verifier_address):
                if not self.identities[owner_address]['verified']:
                    self.identities[owner_address]['verified'] = True
                    print("Identity verified successfully.")
                else:
                    print("Identity is already verified.")
            else:
                print("Not authorized to verify identity.")
        else:
            print("Identity not found.")
    
        
    
    # Existing methods for managing identities (register, update, verify, revoke, grant admin privileges, list identities)

    
    def revoke_identity(self):
        owner_address = input("Enter owner Ethereum address to revoke: ").strip()
        if not self._is_valid_address(owner_address):
            print("Invalid Ethereum address format.")
            return

        revoker_address = input("Enter revoker Ethereum address: ").strip()
        if not self._is_valid_address(revoker_address):
            print("Invalid Ethereum address format.")
            return

        if owner_address in self.identities:
            if self._is_owner(owner_address) or self._is_admin(revoker_address):
                del self.identities[owner_address]
                print("Identity revoked successfully.")
            else:
                print("Not authorized to revoke identity.")
        else:
            print("Identity not found.")

    def grant_admin_privileges(self):
        admin_address = input("Enter Ethereum address to grant admin privileges: ").strip()
        if not self._is_valid_address(admin_address):
            print("Invalid Ethereum address format.")
            return

        if admin_address not in self.identities:
            self.identities[admin_address] = {'name': 'Admin', 'email': '', 'verified': True}
            print("Admin privileges granted successfully.")
        else:
            print("Admin already exists.")

    def list_identities(self):
        print("Registered Identities:")
        for address, identity in self.identities.items():
            print(f"Address: {address}, Name: {identity['name']}, Email: {self._decrypt(identity['email'])}, Verified: {identity['verified']}")




# # Create an instance of the IdentityManagement class
# contract = IdentityManagement()

# # Register an identity
# contract.register_identity()

# # Prompt user for action
# while True:
#     print("\nChoose an action:")
#     print("1. Register Identity")
#     print("2. Share Data")
#     print("3. Access Shared Data")
#     print("4. Update Identity")
#     print("5. Verify Identity")
#     print("6. Revoke Identity")
#     print("7. Grant Admin Privileges")
#     print("8. List Identities")
#     print("9. Exit")

#     choice = input("Enter your choice (1-9): ")
#     if choice == "1":
#         contract.register_identity()
#     elif choice == "2":
#         contract.share_data()
#     elif choice == "3":
#         owner_address = input("Enter owner Ethereum address to access shared data: ").strip()
#         if contract._is_valid_address(owner_address):
#             contract.access_shared_data(owner_address)
#         else:
#             print("Invalid Ethereum address format.")
#     elif choice == "4":
#         print("Exiting program.")
#         break
#     elif choice == "4":
#         contract.update_identity()
#     elif choice == "5":
#         contract.verify_identity()
#     elif choice == "6":
#         contract.revoke_identity()
#     elif choice == "7":
#         contract.grant_admin_privileges()
#     elif choice == "8":
#         contract.list_identities()
#     elif choice == "9":
#         print("Exiting program.")
#         break
#     else:
#         print("Invalid choice. Please enter a number between 1 and 6.")











    
