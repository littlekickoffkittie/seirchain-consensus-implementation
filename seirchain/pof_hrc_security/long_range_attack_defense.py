from seirchain.core.crypto import hash_data
from seirchain.core.triad import Triad

class AggregatedProof:
    """
    Represents an aggregated proof of a range of Triads.
    In a real implementation, this would use a cryptographic accumulator
    or a similar scheme.
    """
    def __init__(self, start_triad_hash, end_triad_hash, aggregated_signature):
        self.start_triad_hash = start_triad_hash
        self.end_triad_hash = end_triad_hash
        self.aggregated_signature = aggregated_signature

    def __repr__(self):
        return f"AggregatedProof(start={self.start_triad_hash[:10]}..., end={self.end_triad_hash[:10]}...)"

class CheckpointTriad(Triad):
    """
    A special type of Triad that contains an aggregated proof of all Triads
    since the last CheckpointTriad.
    """
    def __init__(self, timestamp, transactions, previous_hash, aggregated_proof):
        super().__init__(timestamp, transactions, previous_hash)
        self.aggregated_proof = aggregated_proof

def verify_history(checkpoint_triads):
    """
    Verifies the entire history of the blockchain by checking the chain
    of CheckpointTriads.
    """
    for i in range(1, len(checkpoint_triads)):
        prev_checkpoint = checkpoint_triads[i-1]
        current_checkpoint = checkpoint_triads[i]

        # Verify that the current checkpoint correctly references the previous one
        if current_checkpoint.aggregated_proof.start_triad_hash != prev_checkpoint.hash:
            return False

        # In a real implementation, we would verify the aggregated signature
        # against the public keys of the validators for that period.
        # For now, we'll just assume the signature is valid.

    return True
