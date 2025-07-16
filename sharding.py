import hashlib

def get_triad_id(address: str, num_triads: int) -> int:
    """
    Assigns a smart contract or account address to a specific Triad ID.

    Args:
        address: The address of the smart contract or account.
        num_triads: The total number of Triads.

    Returns:
        The Triad ID.
    """
    hash_object = hashlib.sha256(address.encode())
    hash_digest = hash_object.hexdigest()
    hash_int = int(hash_digest, 16)
    return hash_int % num_triads
