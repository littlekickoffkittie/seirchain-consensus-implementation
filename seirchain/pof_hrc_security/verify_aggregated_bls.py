from seirchain.pof_hrc_security.bls_aggregation import verify_aggregated_signature, generate_bls_key_pair, sign_message, aggregate_signatures
from seirchain.core.triad import Triad

def verify_triad_signature(triad, public_keys, aggregated_signature):
    """
    Verifies the aggregated signature for a given Triad.
    """
    message = triad.hash.encode('utf-8')
    return verify_aggregated_signature(aggregated_signature, public_keys, message)

if __name__ == '__main__':
    # 1. Create a Triad
    triad = Triad(timestamp=0, transactions=[], previous_hash='genesis')

    # 2. Generate key pairs for a committee of validators
    committee_size = 10
    committee_keys = [generate_bls_key_pair() for _ in range(committee_size)]
    private_keys = [key[0] for key in committee_keys]
    public_keys = [key[1] for key in committee_keys]

    # 3. Each validator signs the triad hash
    message = triad.hash.encode('utf-8')
    signatures = [sign_message(message, pk) for pk in private_keys]

    # 4. Aggregate the signatures
    aggregated_signature = aggregate_signatures(signatures)

    # 5. Verify the aggregated signature for the Triad
    is_valid = verify_triad_signature(triad, public_keys, aggregated_signature)
    print(f"Is the aggregated signature for the Triad valid? {is_valid}")

    # 6. Test with a different Triad (should be invalid)
    different_triad = Triad(timestamp=1, transactions=[], previous_hash='genesis')
    is_invalid_valid = verify_triad_signature(different_triad, public_keys, aggregated_signature)
    print(f"Is the aggregated signature for a different Triad valid? {is_invalid_valid}")
