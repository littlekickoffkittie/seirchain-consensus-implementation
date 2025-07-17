import hashlib
from .key_pair import KeyPair

def simple_vrf(key_pair: KeyPair, input_data: bytes) -> tuple[bytes, bytes]:
    """
    A simplified Verifiable Random Function (VRF) implementation.

    This is NOT a cryptographically secure VRF, but it simulates the core
    functionality: generating a random-looking output (hash) and a proof
    that the output was generated with a specific private key.

    In a real implementation, this would use complex elliptic curve cryptography.
    Here, we use a signature as the proof.

    Args:
        key_pair: The KeyPair of the entity generating the VRF.
        input_data: The public input seed for the VRF (e.g., previous block hash).

    Returns:
        A tuple containing:
        - random_output (bytes): A 32-byte pseudorandom value.
        - proof (bytes): A proof that the output was generated correctly.
    """
    # 1. Create a "proof" by signing the input data.
    # This proves the keyholder generated this VRF output for this specific input.
    proof = key_pair.sign(input_data)

    # 2. Generate the random output by hashing the proof.
    # Hashing the signature makes the output unpredictable without the private key.
    random_output = hashlib.sha256(proof).digest()

    return random_output, proof

def simple_vrf_verify(public_key: bytes, input_data: bytes, random_output: bytes, proof: bytes) -> bool:
    """
    Verifies a simplified VRF output.

    Args:
        public_key: The public key of the VRF generator.
        input_data: The public input seed.
        random_output: The random output to verify.
        proof: The proof generated alongside the output.

    Returns:
        True if the verification is successful, False otherwise.
    """
    # 1. Verify the proof (signature) against the public key and input data.
    if not KeyPair.verify(public_key, proof, input_data):
        return False

    # 2. Re-generate the random output and check if it matches.
    # This ensures the provided random_output is the one derived from the valid proof.
    expected_output = hashlib.sha256(proof).digest()

    return random_output == expected_output
