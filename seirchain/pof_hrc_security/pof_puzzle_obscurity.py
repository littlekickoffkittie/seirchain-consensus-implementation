from seirchain.core.crypto import hash_data

def get_dynamic_difficulty(vdf_output):
    """
    Determines the puzzle difficulty based on the VDF output.
    This is a simple example; a real implementation could be more complex.
    """
    # Use the last character of the VDF output as a hex digit to determine difficulty
    return int(vdf_output[-1], 16) % 5 + 1  # Difficulty between 1 and 5

def check_dynamic_pattern(triad_hash, vdf_output):
    """
    Checks if the triad hash matches the dynamic pattern determined by the VDF output.
    """
    difficulty = get_dynamic_difficulty(vdf_output)
    return triad_hash.startswith('0' * difficulty)

class ObscurePoFPuzzle:
    def __init__(self, triad):
        self.triad = triad

    def mine(self):
        """
        Mines the Triad by finding a hash that matches the dynamic pattern.
        """
        if not self.triad.vdf_output:
            raise ValueError("VDF output not present in the Triad.")

        while not check_dynamic_pattern(self.triad.hash, self.triad.vdf_output):
            self.triad.nonce += 1
            self.triad.hash = self.triad.calculate_hash()

        return self.triad
