from seir_chain.data_structures.triad import Triad
from seir_chain.data_structures.transaction import Transaction
from seir_chain.consensus.pof import PoF
from seir_chain.crypto.key_pair import KeyPair

def main():
    """
    A script to simulate the process of mining a new Triad using the VDF-enhanced PoF.
    """
    # 1. Setup: Create a miner identity and a new Triad to be mined.
    miner_key = KeyPair()
    miner_address = miner_key.get_address()
    print(f"Miner Address: {miner_address}")

    # Create a "genesis" or parent Triad. In a real chain, this would be the latest Triad.
    parent_triad = Triad(parent_hash=b'\x00'*32, miner_address="genesis", height=0, difficulty=10)
    parent_triad.calculate_merkle_root() # Finalize parent
    parent_hash = parent_triad.get_header_hash()
    print(f"Parent Triad Hash: {parent_hash.hex()}")

    # Create the new Triad we want to mine
    new_triad = Triad(parent_hash=parent_hash, miner_address=miner_address, height=1, difficulty=15)

    # Add a sample transaction
    tx = Transaction("COINBASE", miner_address, 50, 0, 0) # Reward transaction
    new_triad.add_transaction(tx)
    new_triad.calculate_merkle_root() # Important: Calculate merkle root before PoF

    print(f"New Triad (Height {new_triad.height}) created. Initial Header Hash: {new_triad.get_header_hash().hex()}")

    # 2. PoF Puzzle Generation (with VDF)
    # This is the time-consuming part that prevents pre-computation.
    # The VDF difficulty should be set based on network parameters.
    VDF_DIFFICULTY = 10000 # A low number for quick simulation

    pof_puzzle = PoF(new_triad, VDF_DIFFICULTY)

    # The VDF runs first, creating a time-locked puzzle
    vdf_output, vdf_proof = pof_puzzle.create_puzzle()
    print(f"VDF Output (Puzzle Target): {vdf_output.hex()}")

    # 3. PoW Puzzle Solving
    # Now the miner races to find a nonce for the PoW part.
    # The `vdf_output` is now part of the data being hashed.
    winning_nonce = pof_puzzle.solve_puzzle(new_triad, vdf_output)

    # The Triad is now "mined" with the correct nonce.
    new_triad.nonce = winning_nonce
    print(f"Mining complete. Final Triad Nonce: {new_triad.nonce}")

    # 4. Verification
    # A validator node would perform this check.
    print("\n--- Verification ---")
    is_valid = PoF.verify_solution(
        triad=new_triad,
        vdf_difficulty=VDF_DIFFICULTY,
        vdf_output=vdf_output,
        vdf_proof=vdf_proof
    )

    if is_valid:
        print("\nSUCCESS: The mined Triad's PoF solution is valid.")
    else:
        print("\nFAILURE: The mined Triad's PoF solution is invalid.")

if __name__ == "__main__":
    main()
