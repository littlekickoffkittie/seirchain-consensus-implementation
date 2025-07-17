from seir_chain.data_structures.triad import Triad
from seir_chain.consensus.vdf import VDF
from seir_chain.crypto.hashing import sha256_hash

class PoF:
    """
    Implements the Proof-of-Fractal (PoF) consensus mechanism.
    This version is enhanced with a Verifiable Delay Function (VDF) to provide
    entropy to the puzzle, mitigating pre-computation attacks.
    """
    def __init__(self, triad: Triad, vdf_difficulty: int):
        self.triad = triad
        self.vdf_difficulty = vdf_difficulty

    def get_puzzle_challenge(self) -> bytes:
        """
        The initial challenge for the VDF is the header hash of the Triad being worked on.
        This binds the VDF computation to a specific parent and set of transactions.
        """
        return self.triad.get_header_hash()

    def create_puzzle(self) -> tuple[bytes, bytes]:
        """
        Generates the time-locked puzzle using the VDF.
        The output of the VDF becomes the new target for the PoW puzzle.

        Returns:
            A tuple (vdf_output, vdf_proof).
        """
        challenge = self.get_puzzle_challenge()
        vdf = VDF(challenge, self.vdf_difficulty)
        vdf_output, vdf_proof = vdf.compute()
        return vdf_output, vdf_proof

    @staticmethod
    def solve_puzzle(triad: Triad, vdf_output: bytes) -> int:
        """
        Solves the Proof-of-Work part of the puzzle.
        The miner must find a nonce such that the hash of the (header + vdf_output)
        meets the Triad's difficulty target.

        Args:
            triad: The Triad being mined.
            vdf_output: The unpredictable output from the VDF.

        Returns:
            The winning nonce.
        """
        print(f"Starting PoW search for Triad height {triad.height}...")
        target = 2**256 - 1
        target = target >> triad.difficulty

        nonce = 0
        while True:
            triad.nonce = nonce
            header_hash = triad.get_header_hash()

            # The final hash includes the VDF output, making it unpredictable
            puzzle_hash_input = header_hash + vdf_output
            final_hash = sha256_hash(puzzle_hash_input)

            if int.from_bytes(final_hash, 'big') < target:
                print(f"Solution found! Nonce: {nonce}")
                return nonce

            nonce += 1

    @staticmethod
    def verify_solution(triad: Triad, vdf_difficulty: int, vdf_output: bytes, vdf_proof: bytes) -> bool:
        """
        Verifies a solved PoF puzzle.

        Verification requires three steps:
        1.  Verify the VDF itself: Was the `vdf_output` correctly derived from the Triad's hash?
        2.  Verify the PoW: Does the final hash (using the found nonce and VDF output) meet the difficulty target?

        Args:
            triad: The Triad with the proposed solution (nonce).
            vdf_difficulty: The VDF difficulty parameter.
            vdf_output: The output of the VDF used in the puzzle.
            vdf_proof: The proof from the VDF computation.

        Returns:
            True if the entire solution is valid, False otherwise.
        """
        # 1. Verify the VDF
        # The VDF challenge is based on the header hash BEFORE the nonce was found.
        # We must temporarily reset the nonce to its initial state (0) to recreate the correct challenge hash.
        original_nonce = triad.nonce
        triad.nonce = 0
        challenge = triad.get_header_hash() # Re-calculate the initial challenge with nonce=0
        triad.nonce = original_nonce # Restore the nonce for the PoW check

        if not VDF.verify(challenge, vdf_difficulty, vdf_output, vdf_proof):
            print("Verification failed: VDF is invalid.")
            return False

        # 2. Verify the PoW
        target = 2**256 - 1
        target = target >> triad.difficulty

        header_hash = triad.get_header_hash() # Hash with the proposed nonce
        puzzle_hash_input = header_hash + vdf_output
        final_hash = sha256_hash(puzzle_hash_input)

        if int.from_bytes(final_hash, 'big') >= target:
            print("Verification failed: PoW does not meet target difficulty.")
            return False

        print("PoF solution verified successfully.")
        return True
