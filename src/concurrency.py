class TransactionalMemory:
    def __init__(self):
        self.data = {}
        self.transactions = {}

    def begin_transaction(self, tx_id):
        self.transactions[tx_id] = {'read_set': set(), 'write_set': {}}

    def read(self, tx_id, key):
        if tx_id not in self.transactions:
            self.begin_transaction(tx_id)
        self.transactions[tx_id]['read_set'].add(key)
        return self.data.get(key)

    def write(self, tx_id, key, value):
        if tx_id not in self.transactions:
            self.begin_transaction(tx_id)
        self.transactions[tx_id]['write_set'][key] = value

    def commit_transaction(self, tx_id):
        if tx_id not in self.transactions:
            return False, "Transaction not found"

        transaction = self.transactions[tx_id]
        # Validate read set
        for key in transaction['read_set']:
            # In a real system, we'd check against a committed version.
            # For this simulation, we assume no other transactions have committed.
            pass

        # Apply write set
        for key, value in transaction['write_set'].items():
            self.data[key] = value

        del self.transactions[tx_id]
        return True, "Commit successful"

    def abort_transaction(self, tx_id):
        if tx_id in self.transactions:
            del self.transactions[tx_id]
            return True, "Abort successful"
        return False, "Transaction not found"
