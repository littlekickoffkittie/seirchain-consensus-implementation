import random
import math

class SelfishMiner:
    def __init__(self, mining_power_fraction):
        self.mining_power_fraction = mining_power_fraction
        self.private_chain = []

    def mine_triad(self, public_chain_length):
        """
        Simulates the mining process. Returns True if the selfish miner
        finds a Triad before the honest network.
        """
        return random.random() < self.mining_power_fraction

    def get_hrc_approval(self, hrc_committee_size, fraction_corrupt):
        """
        Simulates the HRC approval process for a privately mined Triad.
        The selfish miner needs to control enough validators to reach the
        2/3 threshold.
        """
        num_corrupt_validators = int(hrc_committee_size * fraction_corrupt)
        required_votes = math.ceil(2 * hrc_committee_size / 3)
        return num_corrupt_validators >= required_votes

def simulate_selfish_mining(selfish_power, hrc_committee_size, fraction_corrupt, num_rounds=1000):
    """
    Simulates a selfish mining attack.
    """
    required_votes = math.ceil(2 * hrc_committee_size / 3)
    print(f"\n--- Simulating with {selfish_power*100}% power, {fraction_corrupt*100:.0f}% corrupt HRC ({hrc_committee_size} validators, {required_votes} votes needed) ---")
    selfish_miner = SelfishMiner(selfish_power)
    public_chain_length = 10
    selfish_wins = 0

    for _ in range(num_rounds):
        if selfish_miner.mine_triad(public_chain_length):
            # Selfish miner found a block. Now, try to get it approved.
            if selfish_miner.get_hrc_approval(hrc_committee_size, fraction_corrupt):
                # The selfish miner's private block is now part of the canonical chain
                public_chain_length += 1
                selfish_wins += 1
            else:
                # The HRC did not approve the selfish block, so it's orphaned.
                # The public chain extends.
                public_chain_length += 1
        else:
            # Honest network found a block
            public_chain_length += 1

    selfish_win_percentage = (selfish_wins / num_rounds) * 100
    print(f"Selfish miner with {selfish_power*100}% power and {fraction_corrupt*100}% corrupt HRC:")
    print(f"  - Won {selfish_wins} out of {num_rounds} rounds ({selfish_win_percentage:.2f}%)")
    print(f"  - Theoretical expected wins (without HRC): {selfish_power*100:.2f}%")


if __name__ == '__main__':
    # Scenario 1: Low-power selfish miner, no HRC corruption
    simulate_selfish_mining(selfish_power=0.3, hrc_committee_size=21, fraction_corrupt=0)

    # Scenario 2: High-power selfish miner, no HRC corruption
    simulate_selfish_mining(selfish_power=0.51, hrc_committee_size=21, fraction_corrupt=0)

    # Scenario 3: High-power selfish miner, with enough HRC corruption to win
    # A 2/3 majority of 21 is 14. So the attacker needs to corrupt 14 validators.
    simulate_selfish_mining(selfish_power=0.51, hrc_committee_size=21, fraction_corrupt=14/21)

    # Scenario 4: A more realistic attacker with 34% power and 30% HRC corruption
    simulate_selfish_mining(selfish_power=0.34, hrc_committee_size=21, fraction_corrupt=0.3)
