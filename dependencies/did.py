import didkit

# Generate a new DID (Decentralized Identifier)
def generate_did():
    try:
        # Generate a new DID using didkit
        did_document = didkit.generate_ed25519_key()

        # Extract the DID from the DID document
        did = did_document

        return did, did_document
    except Exception as e:
        print("Error generating DID:", e)
        return None, None

# Resolve a DID to get its associated DID document
def resolve_did(did):
    try:
        # Resolve the DID using didkit
        did_document = didkit.resolve_did(input_metadata='{}',did=did)

        return did_document
    except Exception as e:
        print("Error resolving DID:", e)
        return None

# Main function
if __name__ == "__main__":
    # Generate a new DID
    new_did, new_did_document = generate_did()
    if new_did:
        print("Generated DID:", new_did)
        print("==DID Document:", new_did_document)

        # Resolve the generated DID
        resolved_did_document = resolve_did(new_did)
        if resolved_did_document:
            print("Resolved DID Document:", resolved_did_document)
