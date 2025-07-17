from seirchain.data_integrity.state_commitment import State, TriadWithStateCommitment

def verify_state_transition(triad1, triad2, initial_state):
    """
    Verifies the state transition between two consecutive Triads.
    """
    # 1. Process the first Triad to get its final state
    state_after_triad1 = triad1.process_transactions(initial_state)

    # 2. Check that the second Triad's previous state commitment matches the first's
    if triad2.previous_state_commitment != triad1.state_commitment:
        print("Error: State commitment mismatch between Triads.")
        return False

    # 3. Process the second Triad to get its final state
    state_after_triad2 = triad2.process_transactions(state_after_triad1)

    # 4. The calculated state commitment must match the one in the Triad
    # (This is already implicitly checked in process_transactions, but we make it explicit here)
    if triad2.state_commitment != state_after_triad2.get_state_commitment():
        print("Error: Calculated state commitment does not match Triad's commitment.")
        return False

    return True


if __name__ == '__main__':
    from seirchain.core.transaction import Transaction

    # Initial state
    initial_state = State()

    # Create the first Triad
    transactions1 = [Transaction("A", "B", 100)]
    triad1 = TriadWithStateCommitment(0, transactions1, "genesis", initial_state.get_state_commitment())
    state_after_triad1 = triad1.process_transactions(initial_state)

    # Create the second Triad
    transactions2 = [Transaction("C", "D", 50)]
    triad2 = TriadWithStateCommitment(1, transactions2, triad1.hash, triad1.state_commitment)
    state_after_triad2 = triad2.process_transactions(state_after_triad1)

    # Verify the transition between the two valid Triads
    # We need to start from the state *before* triad1 was applied
    is_valid_transition = verify_state_transition(triad1, triad2, State())
    print(f"Is the state transition valid? {is_valid_transition}")

    # Create a malicious Triad with an incorrect state commitment
    malicious_triad = TriadWithStateCommitment(1, transactions2, triad1.hash, "fake_commitment")
    is_malicious_transition_valid = verify_state_transition(triad1, malicious_triad, State())
    print(f"Is the malicious state transition valid? {is_malicious_transition_valid}")
