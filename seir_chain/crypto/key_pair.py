import ecdsa
import hashlib
import os

class KeyPair:
    """
    Manages cryptographic key pairs for signing and verification.
    Uses ECDSA over the SECP256k1 curve, same as Bitcoin and Ethereum.
    """
    def __init__(self, private_key_bytes=None):
        """
        Initializes a KeyPair. If private_key is provided, it loads it.
        Otherwise, it generates a new private key.
        """
        if private_key_bytes:
            self.signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
        else:
            # Using os.urandom for cryptographically secure randomness
            self.signing_key = ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1, entropy=os.urandom)

        self.verifying_key = self.signing_key.get_verifying_key()

    @property
    def private_key(self) -> bytes:
        """Returns the private key as bytes."""
        return self.signing_key.to_string()

    @property
    def public_key(self) -> bytes:
        """Returns the public key in its compressed form."""
        return self.verifying_key.to_string("compressed")

    def sign(self, message: bytes) -> bytes:
        """
        Signs a message with the private key.

        Args:
            message: The message to sign, as bytes.

        Returns:
            The signature as bytes.
        """
        return self.signing_key.sign(message, hashfunc=hashlib.sha256)

    @staticmethod
    def verify(public_key: bytes, signature: bytes, message: bytes) -> bool:
        """
        Verifies a signature with the corresponding public key.

        Args:
            public_key: The public key to use for verification.
            signature: The signature to verify.
            message: The original message.

        Returns:
            True if the signature is valid, False otherwise.
        """
        try:
            vk = ecdsa.VerifyingKey.from_string(public_key, curve=ecdsa.SECP256k1)
            return vk.verify(signature, message, hashfunc=hashlib.sha256)
        except (ecdsa.BadSignatureError, ValueError):
            return False

    def get_address(self) -> str:
        """
        Generates a WAC-style address from the public key.
        This is similar to how Ethereum addresses are generated.
        """
        # Keccak-256 is often used, but we'll use SHA-256 for simplicity here.
        pub_key_hash = hashlib.sha256(self.public_key).digest()
        # Take the last 20 bytes of the hash
        return 'WAC' + pub_key_hash[-20:].hex()
