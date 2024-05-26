import hashlib
import json
from datetime import datetime

class DIDRegistry:
    def __init__(self):
        self.dids = {}

    def register_did(self, user, did):
        if user in self.dids:
            raise Exception("DID already registered for this user")
        self.dids[user] = did

    def get_did(self, user):
        return self.dids.get(user, None)

class CredentialRegistry:
    def __init__(self):
        self.credentials = {}

    def issue_credential(self, did, credential_data):
        credential_id = hashlib.sha256(json.dumps(credential_data).encode()).hexdigest()
        self.credentials[credential_id] = {
            'did': did,
            'credential_data': credential_data,
            'issued_at': datetime.utcnow().isoformat()
        }
        return credential_id

    def verify_credential(self, credential_id):
        return self.credentials.get(credential_id, None)

did_registry = DIDRegistry()
credential_registry = CredentialRegistry()
