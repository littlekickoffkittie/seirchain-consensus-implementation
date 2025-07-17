class ProofType:
    SIMPLE_HASH = "SIMPLE_HASH"
    AGGREGATED_SIGNATURE = "AGGREGATED_SIGNATURE"

class HRCProof:
    def __init__(self, proof_type, data):
        self.proof_type = proof_type
        self.data = data

    def __repr__(self):
        return f"HRCProof(type={self.proof_type}, data={self.data[:20]}...)"

def get_proof_type_for_level(level):
    """
    Determines the proof type to use for a given level in the HRC.
    Levels closer to the root (lower level number) use more robust proofs.
    """
    if level < 3:
        return ProofType.AGGREGATED_SIGNATURE
    else:
        return ProofType.SIMPLE_HASH

def generate_proof_for_triad(triad, level):
    """
    Generates a proof for a Triad based on its level in the HRC.
    """
    proof_type = get_proof_type_for_level(level)
    if proof_type == ProofType.AGGREGATED_SIGNATURE:
        # In a real implementation, this would be an actual aggregated signature
        proof_data = f"aggregated_sig_for_{triad.hash}"
    else:
        # For lower levels, the proof is just the hash of the Triad
        proof_data = triad.hash

    return HRCProof(proof_type, proof_data)

if __name__ == '__main__':
    from seirchain.core.triad import Triad

    # Create some dummy triads
    triads = [Triad(i, [], f"prev_hash_{i}") for i in range(5)]

    # Generate proofs for different levels
    for i, triad in enumerate(triads):
        level = i
        proof = generate_proof_for_triad(triad, level)
        print(f"Level {level}: {proof}")
