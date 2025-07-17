class SlashingCondition:
    def __init__(self):
        self.signatures = {}

    def add_signature(self, validator_pub_key, triad_hash, signature):
        """
        Adds a signature from a validator for a given triad hash.
        """
        if validator_pub_key not in self.signatures:
            self.signatures[validator_pub_key] = []
        self.signatures[validator_pub_key].append((triad_hash, signature))

    def check_for_slashing(self, validator_pub_key):
        """
        Checks if a validator has signed two conflicting Triads.
        In this simplified model, we consider any two different triad hashes
        at the same height (or for the same previous hash) as conflicting.
        """
        validator_signatures = self.signatures.get(validator_pub_key, [])
        if len(validator_signatures) < 2:
            return False

        # In a real implementation, we would need to check the height or
        # previous hash of the triads. For now, we'll assume any two
        # different signatures are for conflicting triads.
        first_triad_hash, _ = validator_signatures[0]
        for i in range(1, len(validator_signatures)):
            other_triad_hash, _ = validator_signatures[i]
            if first_triad_hash != other_triad_hash:
                return True
        return False

class StakingLedger:
    def __init__(self, initial_stakes):
        self.stakes = initial_stakes

    def slash_validator(self, validator_pub_key):
        """
        Slashes the stake of a validator.
        """
        if validator_pub_key in self.stakes:
            slashed_amount = self.stakes[validator_pub_key]
            self.stakes[validator_pub_key] = 0
            return slashed_amount
        return 0
