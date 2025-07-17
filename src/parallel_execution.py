import multiprocessing
import time

def transaction_task(tx_id, duration):
    """A dummy transaction that takes a certain amount of time."""
    print(f"Executing transaction {tx_id}...")
    time.sleep(duration)
    print(f"Transaction {tx_id} finished.")
    return tx_id * 2

def execute_parallel(transactions):
    """
    Simulates the parallel execution of transactions within a single Triad.

    Args:
        transactions: A list of tuples, where each tuple contains
                      the arguments for `transaction_task`.

    Returns:
        A list of results from the executed transactions.
    """
    with multiprocessing.Pool() as pool:
        results = pool.starmap(transaction_task, transactions)
    return results
