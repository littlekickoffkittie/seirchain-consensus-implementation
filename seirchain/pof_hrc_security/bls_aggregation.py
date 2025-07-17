from py_ecc.bls import G2ProofOfPossession as bls
import random

def generate_bls_key_pair():
    """
    Generates a BLS key pair.
    """
    private_key = bls.KeyGen(random.randbytes(32))
    public_key = bls.SkToPk(private_key)
    return private_key, public_key

def sign_message(message, private_key):
    """
    Signs a message with a BLS private key.
    """
    return bls.Sign(private_key, message)

def aggregate_signatures(signatures):
    """
    Aggregates a list of BLS signatures.
    """
    return bls.Aggregate(signatures)

def verify_aggregated_signature(aggregated_signature, public_keys, message):
    """
    Verifies an aggregated BLS signature.
    """
    aggregated_public_key = bls._AggregatePKs(public_keys)
    return bls.Verify(aggregated_public_key, message, aggregated_signature)

if __name__ == '__main__':
    import random

    # 1. Generate key pairs for a committee of validators
    committee_size = 10
    committee_keys = [generate_bls_key_pair() for _ in range(committee_size)]
    private_keys = [key[0] for key in committee_keys]
    public_keys = [key[1] for key in committee_keys]

    # 2. A message (e.g., a triad hash) is proposed
    message = b"triad_hash_123"

    # 3. Each validator signs the message
    signatures = [sign_message(message, pk) for pk in private_keys]

    # 4. Aggregate the signatures
    aggregated_signature = aggregate_signatures(signatures)
    print(f"Aggregated Signature: {aggregated_signature.hex()}")

    # 5. Verify the aggregated signature
    is_valid = verify_aggregated_signature(aggregated_signature, public_keys, message)
    print(f"Is aggregated signature valid? {is_valid}")

    # 6. Test with a smaller subset of signatures (should still be valid)
    subset_size = 7
    subset_signatures = signatures[:subset_size]
    subset_public_keys = public_keys[:subset_size]
    aggregated_subset_signature = aggregate_signatures(subset_signatures)
    is_subset_valid = verify_aggregated_signature(aggregated_subset_signature, subset_public_keys, message)
    print(f"Is subset aggregated signature valid? {is_subset_valid}")

    # 7. Test with a signature for a different message (should be invalid)
    invalid_message = b"different_triad_hash"
    invalid_signature = sign_message(invalid_message, private_keys[0])
    invalid_aggregated_signature = aggregate_signatures(signatures[1:] + [invalid_signature])
    is_invalid_aggregation_valid = verify_aggregated_signature(invalid_aggregated_signature, public_keys, message)
    print(f"Is invalid aggregated signature valid? {is_invalid_aggregation_valid}")
