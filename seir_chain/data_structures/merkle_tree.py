from seir_chain.crypto.hashing import sha256_hash, merkle_root

class MerkleTree:
    """
    A class-based wrapper for the Merkle root calculation.
    While the core logic is in crypto.hashing.merkle_root, this class
    provides an object-oriented interface and a placeholder for future
    enhancements like proof generation.
    """
    def __init__(self, items: list[bytes]):
        """
        Initializes the Merkle tree.

        Args:
            items: A list of byte strings to build the tree from.
                   These are typically transaction hashes.
        """
        if not isinstance(items, list):
            raise TypeError("MerkleTree requires a list of byte strings.")

        self.items = items
        self.root = self._calculate_root()

    def _calculate_root(self) -> bytes:
        """
        Calculates the Merkle root for the given items.
        """
        if not self.items:
            return sha256_hash(b'')

        # The merkle_root function expects hashes, not raw data.
        # In our design, Triad passes transaction hashes to it.
        return merkle_root(self.items)

    def get_root(self) -> bytes:
        """Returns the calculated Merkle root."""
        return self.root

    def get_proof(self, index: int):
        """
        (Not Implemented) Generates a Merkle proof for an item at a given index.
        This would be required for light clients (SPV).
        """
        print("Warning: Merkle proof generation is not yet implemented.")
        # A real implementation would traverse the tree structure to find sibling hashes.
        return []

    @staticmethod
    def verify_proof(root: bytes, item: bytes, proof: list):
        """
        (Not Implemented) Verifies a Merkle proof.
        """
        print("Warning: Merkle proof verification is not yet implemented.")
        # A real implementation would hash the item with the proof hashes
        # sequentially to see if the final hash matches the root.
        return False
