import hashlib

class ErasureCode:
    """
    A placeholder for an erasure coding library.
    In a real implementation, this would use a library like zfec or reedsolo.
    """
    def __init__(self, k, m):
        self.k = k # Number of original chunks
        self.m = m # Number of total chunks (original + parity)

    def encode(self, data):
        """
        Encodes data into k + m chunks.
        """
        # This is a simplified simulation. A real implementation would generate
        # parity chunks that can be used for reconstruction.
        chunk_size = (len(data) + self.k - 1) // self.k
        original_chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

        # Simulate parity chunks by hashing the original chunks
        parity_chunks = [hashlib.sha256(chunk).digest() for chunk in original_chunks]

        return original_chunks + parity_chunks[:self.m - self.k]

    def decode(self, chunks):
        """
        Decodes the original data from a subset of the chunks.
        """
        # This is a simplified simulation. A real implementation would use the
        # parity chunks to reconstruct missing original chunks.
        # We assume that at least k chunks are present.
        original_chunks = chunks[:self.k]
        return b"".join(original_chunks)

class CodedMerkleTree:
    def __init__(self, data, k, m):
        self.encoder = ErasureCode(k, m)
        self.encoded_chunks = self.encoder.encode(data)
        self.tree = self._build_tree()

    def _hash_pair(self, left, right):
        return hashlib.sha256(left + right).hexdigest()

    def _build_tree(self):
        nodes = [hashlib.sha256(chunk).hexdigest() for chunk in self.encoded_chunks]
        tree = [nodes]

        while len(nodes) > 1:
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1]) # Duplicate the last node if odd

            new_level = []
            for i in range(0, len(nodes), 2):
                new_level.append(self._hash_pair(nodes[i].encode(), nodes[i+1].encode()))
            nodes = new_level
            tree.append(nodes)

        return tree

    def get_root(self):
        return self.tree[-1][0] if self.tree else None

    def get_proof(self, chunk_index):
        # Proof generation for a Merkle tree (omitted for brevity, but would be standard)
        pass

    def reconstruct_data(self, available_chunks):
        """
        Reconstructs the original data from a subset of the encoded chunks.
        """
        return self.encoder.decode(available_chunks)

if __name__ == '__main__':
    original_data = b"This is some important data that needs to be resilient to loss."
    k = 4 # 4 original chunks
    m = 8 # 8 total chunks (4 original + 4 parity)

    # Create a Coded Merkle Tree
    cmt = CodedMerkleTree(original_data, k, m)
    print(f"Merkle Root: {cmt.get_root()}")

    # Simulate data loss by only having a subset of the chunks available
    # We need at least k chunks to reconstruct the data
    available_chunks = cmt.encoded_chunks[:k]

    # Reconstruct the data from the available chunks
    reconstructed_data = cmt.reconstruct_data(available_chunks)
    print(f"\nOriginal data:      {original_data}")
    print(f"Reconstructed data: {reconstructed_data}")
    print(f"Is reconstruction successful? {original_data == reconstructed_data}")
