import time
import hashlib

class VDF:
    """
    A simulated Verifiable Delay Function (VDF).

    A real VDF is a function that takes a long time to compute but is fast to verify.
    This is crucial for preventing miners from pre-computing future results.
    The most common constructions (e.g., using repeated squaring in a group of
    unknown order) are too complex to implement from scratch here.

    This class SIMULATES the behavior of a VDF:
    1.  **Delay:** The `compute` method introduces an artificial `time.sleep()` to simulate
        the computational delay.
    2.  **Verifiability:** It produces a "proof" that is easy to verify. In our simulation,
        the proof is simply a hash chain, which isn't a true VDF proof but serves
        the structural purpose.
    """
    def __init__(self, challenge: bytes, difficulty: int):
        """
        Initializes the VDF.

        Args:
            challenge: The input seed for the VDF (e.g., hash of the parent Triad).
            difficulty: The number of iterations, simulating the delay. A higher
                        number means a longer (simulated) computation time.
        """
        if difficulty < 1:
            raise ValueError("VDF difficulty must be at least 1.")
        self.challenge = challenge
        self.difficulty = difficulty
        self.output = None
        self.proof = None

    def compute(self) -> tuple[bytes, bytes]:
        """
        Simulates the long computation process.
        Generates an output and a proof.
        """
        print(f"Simulating VDF computation for {self.difficulty} iterations...")
        start_time = time.time()

        current_hash = self.challenge
        for _ in range(self.difficulty):
            current_hash = hashlib.sha256(current_hash).digest()
            # In a real VDF, this is the slow part. We don't need to sleep
            # here as the computation itself will take time. For a simulation
            # where hashing is fast, a sleep could be added if desired.
            # time.sleep(0.001) # Optional: to make the delay more noticeable

        self.output = current_hash
        # The "proof" in this simulation is the final output itself.
        # A real VDF has a more complex proof structure.
        self.proof = self.output

        end_time = time.time()
        print(f"VDF computation finished in {end_time - start_time:.4f} seconds.")

        return self.output, self.proof

    @staticmethod
    def verify(challenge: bytes, difficulty: int, output: bytes, proof: bytes) -> bool:
        """
        Verifies the VDF output quickly.

        In our simulation, verification involves re-computing the hash chain,
        which is not "fast" in the true VDF sense, but it's deterministic and
        correctly validates the computation. A true VDF would have a much
        faster verification algorithm that doesn't repeat the work.
        """
        if output != proof:
            # In our simplified scheme, output and proof are the same.
            return False

        current_hash = challenge
        for _ in range(difficulty):
            current_hash = hashlib.sha256(current_hash).digest()

        return current_hash == output
