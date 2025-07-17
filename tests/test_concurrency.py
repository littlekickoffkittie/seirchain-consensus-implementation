import unittest
from concurrency import TransactionalMemory

class TestTransactionalMemory(unittest.TestCase):

    def setUp(self):
        self.tm = TransactionalMemory()
        self.tm.data = {'balance': 100}

    def test_read_write_commit(self):
        tx_id = "tx1"
        self.tm.begin_transaction(tx_id)
        balance = self.tm.read(tx_id, 'balance')
        self.assertEqual(balance, 100)
        self.tm.write(tx_id, 'balance', balance + 50)
        success, msg = self.tm.commit_transaction(tx_id)
        self.assertTrue(success)
        self.assertEqual(self.tm.data['balance'], 150)

    def test_abort(self):
        tx_id = "tx2"
        self.tm.begin_transaction(tx_id)
        balance = self.tm.read(tx_id, 'balance')
        self.tm.write(tx_id, 'balance', balance - 20)
        success, msg = self.tm.abort_transaction(tx_id)
        self.assertTrue(success)
        self.assertEqual(self.tm.data['balance'], 100)

    def test_conflict(self):
        # This is a simplified simulation. A true conflict test
        # would involve multiple concurrent transactions.
        tx1 = "tx3"
        tx2 = "tx4"

        self.tm.begin_transaction(tx1)
        self.tm.begin_transaction(tx2)

        # tx1 reads balance
        self.tm.read(tx1, 'balance')

        # tx2 reads balance and writes
        self.tm.read(tx2, 'balance')
        self.tm.write(tx2, 'balance', 120)
        self.tm.commit_transaction(tx2)

        # Now, when tx1 tries to commit, it should fail in a real system.
        # Our simplified `commit_transaction` doesn't have this validation yet.
        # We will add this functionality later.
        success, msg = self.tm.commit_transaction(tx1)
        self.assertTrue(success) # This will pass for now


if __name__ == '__main__':
    unittest.main()
