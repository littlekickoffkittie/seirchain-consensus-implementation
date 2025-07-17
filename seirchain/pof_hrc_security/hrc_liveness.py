import random

class Validator:
    def __init__(self, is_online=True):
        self.is_online = is_online

    def vote(self, triad):
        if self.is_online:
            return True, f"Vote for {triad.hash}"
        return False, "Validator offline"

class HRCCommittee:
    def __init__(self, validators):
        self.validators = validators

    def reach_consensus(self, triad):
        """
        Simulates the consensus process for a Triad.
        """
        votes = []
        for validator in self.validators:
            vote_cast, message = validator.vote(triad)
            if vote_cast:
                votes.append(message)

        # BFT requires 2/3 + 1 votes to reach consensus
        if len(votes) >= (2 * len(self.validators) / 3) + 1:
            return True, f"Consensus reached with {len(votes)} votes."
        else:
            return False, f"Consensus failed. Only {len(votes)} votes cast."

def simulate_liveness_scenario(total_validators, offline_validators):
    """
    Simulates a liveness scenario with a given number of offline validators.
    """
    validators = [Validator(is_online=i >= offline_validators) for i in range(total_validators)]
    committee = HRCCommittee(validators)

    # Create a dummy triad for the simulation
    from seirchain.core.triad import Triad
    dummy_triad = Triad(0, [], 'genesis')

    consensus_reached, message = committee.reach_consensus(dummy_triad)
    print(f"Simulating with {total_validators} total validators and {offline_validators} offline:")
    print(message)
    return consensus_reached

if __name__ == '__main__':
    # Scenario 1: Consensus should be reached
    simulate_liveness_scenario(total_validators=21, offline_validators=6)

    # Scenario 2: Consensus should fail
    simulate_liveness_scenario(total_validators=21, offline_validators=8)
