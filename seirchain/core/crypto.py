import hashlib
import os
from ecdsa import SigningKey, NIST256p

def generate_key_pair():
    """Generates a new ECDSA key pair."""
    private_key = SigningKey.generate(curve=NIST256p)
    public_key = private_key.get_verifying_key()
    return private_key, public_key

def hash_data(data):
    """Hashes data using SHA-256."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    return hashlib.sha256(data).hexdigest()
