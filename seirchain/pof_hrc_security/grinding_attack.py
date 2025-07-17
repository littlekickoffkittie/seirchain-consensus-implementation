import hashlib
import random

def vrf_output(seed):
    """
    A simple VRF simulation. In a real implementation, this would use a
    proper VRF construction.
    """
    return hashlib.sha256(seed).hexdigest()

def is_miner_selected(vrf_output, public_key, stake, total_stake):
    """
    Determines if a miner is selected based on the VRF output.
    A higher stake increases the chance of being selected.
    """
    selection_threshold = (stake / total_stake) * (2**256 - 1)
    return int(vrf_output, 16) < selection_threshold

class MaliciousMiner:
    def __init__(self, public_key, stake):
        self.public_key = public_key
        self.stake = stake

    def grind(self, triad, total_stake, max_attempts=10000):
        """
        Attempts to find a nonce that results in a favorable VRF output.
        """
        for i in range(max_attempts):
            nonce = i
            # The miner manipulates the nonce to try to get selected
            vrf_seed = f"{triad.previous_hash}{nonce}".encode('utf-8')
            output = vrf_output(vrf_seed)
            if is_miner_selected(output, self.public_key, self.stake, total_stake):
                print(f"Grinding successful after {i+1} attempts!")
                return nonce, output
        print("Grinding failed.")
        return None, None

class HonestMiner:
    def __init__(self, public_key, stake):
        self.public_key = public_key
        self.stake = stake

    def get_vrf_output(self, triad):
        """
        An honest miner uses a pre-committed value as the nonce, preventing grinding.
        """
        # The nonce is derived from a source that the miner cannot easily manipulate,
        # such as a signature over the previous block's hash.
        precommitted_nonce = "precommitted_value"
        vrf_seed = f"{triad.previous_hash}{precommitted_nonce}".encode('utf-8')
        return vrf_output(vrf_seed)

if __name__ == '__main__':
    from seirchain.core.triad import Triad

    # Setup
    total_stake = 10000
    malicious_miner = MaliciousMiner("malicious_pk", 100) # 1% stake
    honest_miner = HonestMiner("honest_pk", 100)
    triad = Triad(0, [], 'genesis')

    # Malicious miner grinds for a favorable VRF output
    print("--- Malicious Miner Grinding Simulation ---")
    malicious_miner.grind(triad, total_stake)

    # Honest miner cannot grind
    print("\n--- Honest Miner (Mitigation) ---")
    honest_output = honest_miner.get_vrf_output(triad)
    print(f"Honest miner VRF output: {honest_output}")
    if is_miner_selected(honest_output, honest_miner.public_key, honest_miner.stake, total_stake):
        print("Honest miner was selected.")
    else:
        print("Honest miner was not selected.")
