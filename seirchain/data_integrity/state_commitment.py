import hashlib
import json

class State:
    def __init__(self):
        self.accounts = {}

    def apply_transaction(self, tx):
        """
        Applies a transaction to the state.
        This is a simplified model of state transition.
        """
        if tx.from_address not in self.accounts:
            self.accounts[tx.from_address] = 1000 # Starting balance
        if tx.to_address not in self.accounts:
            self.accounts[tx.to_address] = 1000

        if self.accounts[tx.from_address] >= tx.amount:
            self.accounts[tx.from_address] -= tx.amount
            self.accounts[tx.to_address] += tx.amount
            return True
        return False

    def get_state_commitment(self):
        """
        Calculates a commitment to the current state.
        In a real implementation, this would be the root of a Patricia Merkle Trie.
        """
        # Sorting the dictionary ensures a deterministic hash
        sorted_accounts = sorted(self.accounts.items())
        return hashlib.sha256(json.dumps(sorted_accounts).encode('utf-8')).hexdigest()

class TriadWithStateCommitment:
    def __init__(self, timestamp, transactions, previous_hash, previous_state_commitment):
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.previous_state_commitment = previous_state_commitment
        self.state_commitment = None
        self.hash = None

    def process_transactions(self, initial_state):
        """
        Processes the transactions in the Triad and calculates the new state commitment.
        """
        state = initial_state
        for tx in self.transactions:
            state.apply_transaction(tx)
        self.state_commitment = state.get_state_commitment()
        self.hash = self.calculate_hash()
        return state

    def calculate_hash(self):
        """
        Calculates the hash of the Triad, including the state commitment.
        """
        triad_data = f"{self.timestamp}{self.transactions}{self.previous_hash}{self.state_commitment}"
        return hashlib.sha256(triad_data.encode('utf-8')).hexdigest()

if __name__ == '__main__':
    from seirchain.core.transaction import Transaction

    # Initial state
    state = State()
    initial_state_commitment = state.get_state_commitment()
    print(f"Initial state commitment: {initial_state_commitment}")

    # Create a Triad
    transactions = [Transaction("A", "B", 100), Transaction("C", "D", 50)]
    triad = TriadWithStateCommitment(0, transactions, "genesis_hash", initial_state_commitment)

    # Process the Triad
    new_state = triad.process_transactions(state)
    print(f"\nNew state commitment: {triad.state_commitment}")
    print(f"Triad hash: {triad.hash}")

    # Verify the new state
    print("\nFinal account balances:")
    for account, balance in new_state.accounts.items():
        print(f"  - {account}: {balance}")
