# utils.py

import ipfshttpclient
from django.conf import settings

def upload_to_ipfs(file_path):
    # Connect to the IPFS daemon using the configured API URL
    client = ipfshttpclient.connect(settings.IPFS_STORAGE_API_URL)

    # Upload the file to IPFS
    result = client.add(file_path)

    # Close the connection to the IPFS daemon
    client.close()

    # Return the IPFS hash of the uploaded file
    return result['Hash']

def get_from_ipfs(ipfs_hash, destination_path):
    # Connect to the IPFS daemon using the configured API URL
    client = ipfshttpclient.connect(settings.IPFS_STORAGE_API_URL)

    # Download the file from IPFS
    client.get(ipfs_hash, destination=destination_path)

    # Close the connection to the IPFS daemon
    client.close()
