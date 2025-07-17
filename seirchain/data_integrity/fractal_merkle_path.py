import hashlib

def hash_pair(left, right):
    return hashlib.sha256(left.encode('utf-8') + right.encode('utf-8')).hexdigest()

class SimpleMerkleTree:
    def __init__(self, items):
        self.leaves = [hashlib.sha256(item.encode('utf-8')).hexdigest() for item in items]
        self.tree = self._build_tree()

    def _build_tree(self):
        nodes = list(self.leaves)
        if not nodes:
            return []

        tree = [nodes]
        while len(nodes) > 1:
            if len(nodes) % 2 != 0:
                nodes.append(nodes[-1])

            new_level = []
            for i in range(0, len(nodes), 2):
                new_level.append(hash_pair(nodes[i], nodes[i+1]))
            nodes = new_level
            tree.append(nodes)
        return tree

    def get_root(self):
        return self.tree[-1][0] if self.tree else None

    def get_proof(self, item_index):
        proof = []
        for level in self.tree[:-1]:
            is_right_node = item_index % 2 != 0
            pair_index = item_index - 1 if is_right_node else item_index + 1

            if pair_index < len(level):
                proof.append({'hash': level[pair_index], 'is_right': not is_right_node})
            item_index //= 2
        return proof

def verify_proof(item, proof, root):
    current_hash = hashlib.sha256(item.encode('utf-8')).hexdigest()
    for sibling in proof:
        if sibling['is_right']:
            current_hash = hash_pair(current_hash, sibling['hash'])
        else:
            current_hash = hash_pair(sibling['hash'], current_hash)
    return current_hash == root

class FractalMerklePath:
    def __init__(self):
        self.path = []

    def add_proof_level(self, item, proof, root):
        self.path.append({"item": item, "proof": proof, "root": root})

    def verify(self):
        # The first item in the path is the transaction itself.
        # Each subsequent item is the root of the previous level's proof.
        for i in range(len(self.path)):
            level = self.path[i]
            if not verify_proof(level["item"], level["proof"], level["root"]):
                return False
            if i + 1 < len(self.path):
                # Check that the root of this level is the item in the next level
                if level["root"] != self.path[i+1]["item"]:
                    return False
        return True

if __name__ == '__main__':
    # Level 1: Transaction in a Triad
    transactions = ["tx_A", "tx_B", "tx_C", "tx_D"]
    tx_tree = SimpleMerkleTree(transactions)
    tx_root = tx_tree.get_root()
    tx_proof = tx_tree.get_proof(1) # Proof for "tx_B"

    # Level 2: Triad in a parent Triad
    child_triad_hashes = ["hash_1", tx_root, "hash_3", "hash_4"]
    parent_tree = SimpleMerkleTree(child_triad_hashes)
    parent_root = parent_tree.get_root()
    parent_proof = parent_tree.get_proof(1) # Proof for tx_root

    # Build the fractal Merkle path
    fractal_path = FractalMerklePath()
    fractal_path.add_proof_level("tx_B", tx_proof, tx_root)
    fractal_path.add_proof_level(tx_root, parent_proof, parent_root)

    # Verify the path
    is_valid = fractal_path.verify()
    print(f"Is the fractal Merkle path valid? {is_valid}")

    # Tamper with the path to show verification failure
    fractal_path.path[0]["item"] = "tx_E"
    is_tampered_valid = fractal_path.verify()
    print(f"Is the tampered fractal Merkle path valid? {is_tampered_valid}")
