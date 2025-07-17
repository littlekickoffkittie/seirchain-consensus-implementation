def calculate_max_tps(N, P, C_r):
    """
    Calculates the theoretical maximum TPS of a sharded blockchain.

    Args:
        N: The number of shards (Triads).
        P: The processing power of a single shard (in TPS).
        C_r: The cross-shard conflict rate (a value between 0 and 1).

    Returns:
        The theoretical maximum TPS.
    """
    return N * P * (1 - C_r)

if __name__ == "__main__":
    N = 64  # Number of Triads
    P = 1000  # Processing power of a single Triad (TPS)

    print(f"Modeling TPS with N={N} and P={P}")
    print("-" * 30)

    for C_r in [0.01, 0.05, 0.1, 0.2, 0.5]:
        max_tps = calculate_max_tps(N, P, C_r)
        print(f"Conflict Rate (C_r): {C_r:.2f} -> Max TPS: {max_tps:,.0f}")
