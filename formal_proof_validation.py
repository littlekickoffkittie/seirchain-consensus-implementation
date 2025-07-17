import hashlib

class Transaction:
    def __init__(self, from_address, to_address, amount, signature=None):
        self.from_address = from_address
        self.to_address = to_address
        self.amount = amount
        self.signature = signature

    def calculate_hash(self):
        """
        Calculates the hash of the transaction.
        """
        tx_string = f"{self.from_address}{self.to_address}{self.amount}"
        return hashlib.sha256(tx_string.encode()).hexdigest()

    def sign(self, private_key):
        """
        Signs the transaction with a private key.
        In a real system, this would use a proper cryptographic library.
        Here, we'll just use a hash of the private key as a signature.
        """
        self.signature = hashlib.sha256(private_key.encode()).hexdigest()

def validate_ledger(ledger, statement):
    """
    Validates a formal methods statement against a ledger.
    """
    if statement == "all transactions are signed":
        for tx in ledger:
            if tx.signature is None:
                return False, f"Transaction {tx.calculate_hash()} is not signed."
        return True, "All transactions are signed."
    else:
        return False, "Unknown statement."

if __name__ == '__main__':
    # Create a simulated ledger
    ledger = [
        Transaction("Alice", "Bob", 50),
        Transaction("Bob", "Charlie", 20),
        Transaction("Charlie", "Alice", 10)
    ]

    # Sign some of the transactions
    ledger[0].sign("alice_private_key")
    ledger[2].sign("charlie_private_key")

    # --- Validation ---

    # 1. Check a valid ledger
    print("--- Checking a partially signed ledger ---")
    is_valid, message = validate_ledger(ledger, "all transactions are signed")
    print(f"Result: {is_valid}, {message}\n")

    # 2. Sign all transactions and check again
    print("--- Checking a fully signed ledger ---")
    for tx in ledger:
        if tx.signature is None:
            tx.sign(f"{tx.from_address}_private_key")

    is_valid_2, message_2 = validate_ledger(ledger, "all transactions are signed")
    print(f"Result: {is_valid_2}, {message_2}")
