import time
import json
from seir_chain.crypto.hashing import sha256_hash
from seir_chain.crypto.key_pair import KeyPair

class Transaction:
    """
    Represents a single transaction in the SeirChain network.
    """
    def __init__(self, from_address: str, to_address: str, amount: int, fee: int, nonce: int, signature: bytes = None, public_key: bytes = None):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.fee = fee
        self.nonce = nonce
        self.timestamp = int(time.time())
        self.signature = signature
        self.public_key = public_key

    def to_dict(self, with_signature=True) -> dict:
        """Returns a dictionary representation of the transaction."""
        data = {
            "from_address": self.from_address,
            "to_address": self.to_address,
            "amount": self.amount,
            "fee": self.fee,
            "nonce": self.nonce,
            "timestamp": self.timestamp,
        }
        if with_signature:
            data["public_key"] = self.public_key.hex() if self.public_key else None
            data["signature"] = self.signature.hex() if self.signature else None
        return data

    def payload(self) -> bytes:
        """
        Creates the payload of the transaction that needs to be signed.
        The signature itself and the public key are excluded from the payload.
        """
        # Using a sorted JSON string ensures a consistent hash
        payload_str = json.dumps(self.to_dict(with_signature=False), sort_keys=True)
        return payload_str.encode('utf-8')

    def sign(self, key_pair: KeyPair):
        """
        Signs the transaction with the sender's private key.
        The signature is stored in the transaction object.
        """
        if key_pair.get_address() != self.from_address:
            raise ValueError("Cannot sign transaction for another address.")

        self.public_key = key_pair.public_key
        self.signature = key_pair.sign(self.payload())

    def is_valid(self) -> bool:
        """
        Verifies the transaction's signature.
        """
        if self.from_address == "COINBASE": # Genesis or reward transactions
            return True
        if not self.signature or not self.public_key:
            return False

        # Verify the public key matches the from_address
        temp_key_pair = KeyPair() # Create a dummy keypair to access get_address
        # This is a bit inefficient, but avoids storing the address in the keypair
        # A better way might be to derive the address directly from the public key
        # without creating a KeyPair object. For now, this works.
        # Let's create a static method in KeyPair for this.
        # (This is a placeholder for a direct address calculation from public key)
        # Re-generating address from public key to ensure it matches from_address
        # Note: We need to import hashlib for this to work. Let's add it.
        import hashlib
        hasher = hashlib.sha256(self.public_key)
        addr_from_pubkey = 'WAC' + hasher.digest()[-20:].hex()
        if addr_from_pubkey != self.from_address:
             return False

        return KeyPair.verify(self.public_key, self.signature, self.payload())

    def get_hash(self) -> bytes:
        """
        Computes the hash of the entire transaction, including the signature.
        This hash serves as the unique identifier for the transaction.
        """
        tx_str = json.dumps(self.to_dict(with_signature=True), sort_keys=True)
        return sha256_hash(tx_str.encode('utf-8'))
