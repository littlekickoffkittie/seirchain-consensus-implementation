def calculate_mining_reward(triad, base_reward=100, penalty_factor=0.5):
    """
    Calculates the mining reward for a Triad.
    Empty Triads receive a penalized reward.
    """
    if not triad.transactions:
        return base_reward * penalty_factor
    else:
        # The reward could also be supplemented by transaction fees
        return base_reward

if __name__ == '__main__':
    from seirchain.core.triad import Triad
    from seirchain.core.transaction import Transaction

    # Create an empty Triad
    empty_triad = Triad(0, [])
    empty_reward = calculate_mining_reward(empty_triad)
    print(f"Reward for empty Triad: {empty_reward}")

    # Create a Triad with transactions
    transactions = [Transaction("a", "b", 10), Transaction("c", "d", 20)]
    full_triad = Triad(1, transactions)
    full_reward = calculate_mining_reward(full_triad)
    print(f"Reward for Triad with {len(full_triad.transactions)} transactions: {full_reward}")
