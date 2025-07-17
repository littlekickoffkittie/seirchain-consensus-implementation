import unittest
import time
from seirchain.wac_token import WACToken

class TestWACToken(unittest.TestCase):

    def setUp(self):
        self.token = WACToken(0, "genesis_triad")

    def test_issue_initial_supply(self):
        self.token.issue_initial_supply(1000000, "genesis_triad")
        self.assertEqual(self.token.total_supply, 1000000)
        self.assertEqual(self.token.balances["genesis_triad"], 1000000)

    def test_transfer(self):
        self.token.issue_initial_supply(1000000, "genesis_triad")
        self.token.transfer("genesis_triad", "user1", 100, "signature")
        self.assertEqual(self.token.balances["genesis_triad"], 999900)
        self.assertEqual(self.token.balances["user1"], 100)

    def test_stake(self):
        self.token.issue_initial_supply(1000000, "genesis_triad")
        self.token.stake("genesis_triad", 500)
        self.assertEqual(self.token.balances["genesis_triad"], 999500)
        self.assertEqual(self.token.staked["genesis_triad"], 500)

    def test_inflation(self):
        self.token.issue_initial_supply(1000000, "genesis_triad")
        time.sleep(1) # Ensure some time has passed for inflation calculation
        initial_supply = self.token.total_supply
        self.token.apply_inflation()
        self.assertGreater(self.token.total_supply, initial_supply)

if __name__ == '__main__':
    unittest.main()
