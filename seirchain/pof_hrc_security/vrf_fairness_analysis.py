import hashlib
from collections import Counter

def vrf_output(seed):
    """
    A simple VRF simulation.
    """
    return hashlib.sha256(seed).hexdigest()

def is_miner_selected(vrf_output, stake, total_stake):
    """
    Determines if a miner is selected based on the VRF output.
    """
    selection_threshold = (stake / total_stake) * (2**256 - 1)
    return int(vrf_output, 16) < selection_threshold

def run_fairness_analysis(miners, total_stake, num_runs=1_000_000):
    """
    Runs a statistical analysis of the VRF miner selection.
    """
    selection_counts = Counter()

    sorted_miners = sorted(miners.items(), key=lambda item: item[0])

    for i in range(num_runs):
        seed = f"round_{i}".encode('utf-8')
        output = vrf_output(seed)

        vrf_value = int(output, 16)

        cumulative_stake = 0
        for miner_id, stake in sorted_miners:
            selection_threshold = (stake / total_stake) * (2**256 - 1)
            if vrf_value < cumulative_stake + selection_threshold:
                selection_counts[miner_id] += 1
                break
            cumulative_stake += selection_threshold

    print(f"--- VRF Fairness Analysis ({num_runs} runs) ---")
    for miner_id, stake in miners.items():
        expected_selections = (stake / total_stake) * num_runs
        actual_selections = selection_counts[miner_id]
        discrepancy = (actual_selections - expected_selections) / expected_selections * 100

        print(f"\nMiner: {miner_id} (Stake: {stake})")
        print(f"  - Expected selections: {expected_selections:.2f}")
        print(f"  - Actual selections:   {actual_selections}")
        print(f"  - Discrepancy:         {discrepancy:.2f}%")

if __name__ == '__main__':
    miners = {
        "miner_A": 100,
        "miner_B": 200,
        "miner_C": 700,
    }
    total_stake = sum(miners.values())
    run_fairness_analysis(miners, total_stake)
