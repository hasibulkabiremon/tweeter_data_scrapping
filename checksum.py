import hashlib

def generate_checksum(text: str):
    hash_object = hashlib.md5(text.encode())
    return hash_object.hexdigest()
