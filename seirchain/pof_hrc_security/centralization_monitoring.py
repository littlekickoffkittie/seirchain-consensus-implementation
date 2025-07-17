from collections import Counter
import random

class MinedTriad:
    def __init__(self, miner_id):
        self.miner_id = miner_id

def simulate_triad_stream(num_triads, miner_pool):
    """
    Simulates a stream of mined Triads.
    """
    for _ in range(num_triads):
        # In a real scenario, the miner would be determined by the PoF solution.
        # Here, we'll just pick a random miner from the pool.
        miner = random.choice(miner_pool)
        yield MinedTriad(miner)

def analyze_miner_distribution(triad_stream, total_triads, warning_threshold=0.5):
    """
    Analyzes the distribution of miners in a stream of Triads.
    """
    miner_counts = Counter(triad.miner_id for triad in triad_stream)

    print("Miner Distribution:")
    for miner, count in miner_counts.items():
        percentage = (count / total_triads) * 100
        print(f"  - {miner}: {count} Triads ({percentage:.2f}%)")
        if percentage / 100 > warning_threshold:
            print(f"    **WARNING**: Miner {miner} has exceeded the {warning_threshold*100}% threshold!")

if __name__ == '__main__':
    # Scenario 1: Healthy distribution
    print("--- Scenario 1: Healthy Distribution ---")
    healthy_miners = [f"miner_{i}" for i in range(10)]
    healthy_stream = simulate_triad_stream(1000, healthy_miners)
    analyze_miner_distribution(healthy_stream, 1000)

    # Scenario 2: Potential centralization
    print("\n--- Scenario 2: Potential Centralization ---")
    centralized_miners = ["dominant_miner"] * 6 + [f"miner_{i}" for i in range(4)]
    centralized_stream = simulate_triad_stream(1000, centralized_miners)
    analyze_miner_distribution(centralized_stream, 1000)
