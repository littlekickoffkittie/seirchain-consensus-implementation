from seirchain.pof_hrc_security.validator_slashing import SlashingCondition, StakingLedger
from seirchain.core.triad import Triad
from seirchain.core.crypto import generate_key_pair

def simulate_nothing_at_stake_scenario():
    """
    Simulates a scenario where a validator attempts a nothing-at-stake attack.
    """
    # 1. Setup: A validator with a stake
    validator_private_key, validator_public_key_obj = generate_key_pair()
    validator_public_key = validator_public_key_obj.to_string().hex()
    initial_stakes = {validator_public_key: 1000}
    staking_ledger = StakingLedger(initial_stakes)
    slashing_condition = SlashingCondition()

    # 2. Two competing Triads are proposed at the same height
    triad_A = Triad(timestamp=1, transactions=[], previous_hash='genesis')
    triad_B = Triad(timestamp=1, transactions=[], previous_hash='genesis_alt') # Different previous hash

    # 3. The malicious validator signs both Triads
    signature_A = validator_private_key.sign(triad_A.hash.encode('utf-8'))
    signature_B = validator_private_key.sign(triad_B.hash.encode('utf-8'))

    # 4. The signatures are broadcast to the network
    slashing_condition.add_signature(validator_public_key, triad_A.hash, signature_A)
    slashing_condition.add_signature(validator_public_key, triad_B.hash, signature_B)

    # 5. Check for slashing condition
    if slashing_condition.check_for_slashing(validator_public_key):
        slashed_amount = staking_ledger.slash_validator(validator_public_key)
        print(f"Validator {validator_public_key} slashed!")
        print(f"Slashed amount: {slashed_amount}")
        print(f"Remaining stake: {staking_ledger.stakes.get(validator_public_key, 0)}")
    else:
        print("No slashing condition detected.")

if __name__ == '__main__':
    simulate_nothing_at_stake_scenario()
