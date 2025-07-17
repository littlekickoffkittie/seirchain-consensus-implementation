"""
This module implements the WAC token, the native cryptocurrency of the SeirChain network.
"""

import time

class WACToken:
    """
    The WAC token implementation.
    """
    def __init__(self, initial_supply, genesis_triad_address):
        self.total_supply = initial_supply
        self.balances = {genesis_triad_address: initial_supply}
        self.staked = {}
        self.genesis_time = time.time()

    def issue_initial_supply(self, supply, address):
        """
        Issues the initial supply of WAC tokens to the genesis Triad.
        This function should only be called once.
        """
        if self.total_supply > 0:
            raise Exception("Initial supply has already been issued.")
        self.total_supply = supply
        self.balances[address] = supply

    def transfer(self, sender, recipient, amount, signature):
        """
        Transfers WAC tokens from one user to another.
        """
        if self.balances.get(sender, 0) < amount:
            raise ValueError("Insufficient funds.")

        # In a real implementation, we would verify the digital signature here.
        # For this example, we will assume the signature is valid.

        self.balances[sender] -= amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount

    def stake(self, user, amount):
        """
        Stakes WAC tokens for a user.
        """
        if self.balances.get(user, 0) < amount:
            raise ValueError("Insufficient funds to stake.")

        self.balances[user] -= amount
        self.staked[user] = self.staked.get(user, 0) + amount

    def get_inflation_rate(self):
        """
        Calculates the current inflation rate.
        """
        years_since_genesis = (time.time() - self.genesis_time) / (365 * 24 * 60 * 60)
        halving_periods = int(years_since_genesis / 4)
        inflation_rate = 0.05 / (2 ** halving_periods)
        return inflation_rate

    def apply_inflation(self):
        """
        Applies inflation to the total supply.
        """
        inflation = self.total_supply * self.get_inflation_rate()
        self.total_supply += inflation
        # In a real implementation, the newly created tokens would be distributed
        # to stakers and validators.

    def quadratic_vote(self, user, votes):
        """
        Casts a vote using quadratic voting.

        Args:
            user: The user who is voting.
            votes: The number of votes to cast.

        Returns:
            The cost of the votes.
        """
        if self.balances.get(user, 0) < votes ** 2:
            raise ValueError("Insufficient funds for quadratic voting.")

        cost = votes ** 2
        self.balances[user] -= cost
        return cost
