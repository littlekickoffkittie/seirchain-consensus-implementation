import random
from seirchain.pof_hrc_security.grinding_attack import vrf_output

def shuffle_validators(validators, seed):
    """
    Deterministically shuffles a list of validators based on a seed.
    """
    # Use the seed to create a random number generator with a fixed state.
    # This ensures that the shuffle is deterministic for a given seed.
    rng = random.Random(seed)
    shuffled_validators = list(validators)
    rng.shuffle(shuffled_validators)
    return shuffled_validators

def form_committees(shuffled_validators, committee_size):
    """
    Forms committees from a list of shuffled validators.
    """
    return [shuffled_validators[i:i + committee_size] for i in range(0, len(shuffled_validators), committee_size)]

if __name__ == '__main__':
    # A list of all active validators
    all_validators = [f"validator_{i}" for i in range(100)]

    # The seed for the shuffle is derived from a source that is hard to predict
    # or manipulate, such as the hash of a recent Triad combined with a VRF output.
    shuffle_seed = vrf_output(b"entropy_from_recent_triad")
    print(f"Shuffle seed: {shuffle_seed}")

    # Shuffle the validators
    shuffled = shuffle_validators(all_validators, shuffle_seed)
    print("\nShuffled validators (first 10):", shuffled[:10])

    # Form committees
    committees = form_committees(shuffled, committee_size=10)
    print("\nFormed committees:")
    for i, committee in enumerate(committees):
        print(f"  - Committee {i}: {committee}")

    # Demonstrate that the same seed produces the same shuffle
    print("\n--- Verifying Determinism ---")
    shuffled_again = shuffle_validators(all_validators, shuffle_seed)
    print("Are the two shuffles identical?", shuffled == shuffled_again)
