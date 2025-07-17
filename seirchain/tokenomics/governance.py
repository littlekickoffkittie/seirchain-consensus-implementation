class GovernanceContract:
    def __init__(self, initial_params):
        self.params = initial_params
        self.proposals = {}
        self.next_proposal_id = 0

    def create_proposal(self, parameter_to_change, new_value):
        """
        Creates a new proposal to change a consensus parameter.
        """
        proposal_id = self.next_proposal_id
        self.proposals[proposal_id] = {
            "parameter": parameter_to_change,
            "new_value": new_value,
            "votes": {},
            "executed": False
        }
        self.next_proposal_id += 1
        return proposal_id

    def vote(self, proposal_id, voter_address, stake):
        """
        Allows a token holder to vote on a proposal.
        The vote weight is determined by the voter's stake.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal does not exist.")

        self.proposals[proposal_id]["votes"][voter_address] = stake

    def get_proposal_votes(self, proposal_id):
        """
        Gets the total votes for a proposal.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal does not exist.")

        return sum(self.proposals[proposal_id]["votes"].values())

    def execute_proposal(self, proposal_id, total_stake, quorum_threshold=0.4, pass_threshold=0.5):
        """
        Executes a proposal if it has met the quorum and pass thresholds.
        """
        if proposal_id not in self.proposals:
            raise ValueError("Proposal does not exist.")

        proposal = self.proposals[proposal_id]
        if proposal["executed"]:
            raise ValueError("Proposal has already been executed.")

        total_votes = self.get_proposal_votes(proposal_id)

        # Check for quorum
        if (total_votes / total_stake) < quorum_threshold:
            print(f"Proposal {proposal_id} failed: Quorum not met.")
            return False

        # In a more complex system, there would be "yes" and "no" votes.
        # For simplicity, we'll assume all votes are "yes" and check against a pass threshold.
        if (total_votes / total_stake) > pass_threshold:
            self.params[proposal["parameter"]] = proposal["new_value"]
            proposal["executed"] = True
            print(f"Proposal {proposal_id} passed and executed.")
            return True
        else:
            print(f"Proposal {proposal_id} failed: Pass threshold not met.")
            return False

if __name__ == '__main__':
    initial_params = {"committee_size": 21, "block_time": 10}
    governance = GovernanceContract(initial_params)

    # Create a proposal to change the committee size
    proposal_id = governance.create_proposal("committee_size", 31)
    print(f"Created proposal {proposal_id} to change committee_size to 31")

    # Simulate voting
    total_stake = 10000
    voters = {
        "voter_A": 3000,
        "voter_B": 2500,
        "voter_C": 500
    }
    for voter, stake in voters.items():
        governance.vote(proposal_id, voter, stake)

    print(f"\nTotal votes for proposal {proposal_id}: {governance.get_proposal_votes(proposal_id)}")

    # Attempt to execute the proposal
    governance.execute_proposal(proposal_id, total_stake)

    print("\nCurrent consensus parameters:", governance.params)
