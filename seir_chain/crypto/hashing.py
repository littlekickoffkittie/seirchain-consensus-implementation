import hashlib

def sha256_hash(data: bytes) -> bytes:
    """
    Computes the SHA-256 hash of the given data.

    Args:
        data: The input data as bytes.

    Returns:
        The 32-byte SHA-256 hash.
    """
    return hashlib.sha256(data).digest()

def merkle_root(items: list[bytes]) -> bytes:
    """
    Calculates the Merkle root for a list of byte strings.
    Handles empty, odd, and even numbers of items.
    """
    if not items:
        return sha256_hash(b'')

    if len(items) == 1:
        return sha256_hash(items[0])

    # Create the next level of the tree
    next_level = []
    for i in range(0, len(items), 2):
        left = items[i]
        # If there's an odd number of items, duplicate the last one
        right = items[i+1] if i+1 < len(items) else left
        combined_hash = sha256_hash(left + right)
        next_level.append(combined_hash)

    return merkle_root(next_level)
