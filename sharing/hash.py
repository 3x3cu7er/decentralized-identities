import hashlib

def cal_file_hash(File):
    sha256 = hashlib.sha256()

# This code is made to handle large file. Hash part by part instaed of loading the whole file in ram and hash it once.
    for byte_block in iter(lambda: File.read(4096), b""):
            sha256.update(byte_block)

    return sha256.hexdigest()
    
