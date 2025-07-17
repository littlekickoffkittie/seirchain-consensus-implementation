import time

class ReputationManager:
    def __init__(self, ban_threshold=5, ban_duration=60):
        self.reputations = {}
        self.ban_threshold = ban_threshold
        self.ban_duration = ban_duration

    def report_invalid_triad(self, node_id):
        """
        Reports that a node has proposed an invalid Triad.
        """
        if node_id not in self.reputations:
            self.reputations[node_id] = {'strikes': 0, 'banned_until': 0}

        self.reputations[node_id]['strikes'] += 1

    def should_ban(self, node_id):
        """
        Checks if a node should be banned.
        """
        if node_id not in self.reputations:
            return False

        return self.reputations[node_id]['strikes'] >= self.ban_threshold

    def ban(self, node_id):
        """
        Bans a node for a certain duration.
        """
        if node_id in self.reputations:
            self.reputations[node_id]['banned_until'] = time.time() + self.ban_duration

    def is_banned(self, node_id):
        """
        Checks if a node is currently banned.
        """
        if node_id not in self.reputations:
            return False

        return self.reputations[node_id]['banned_until'] > time.time()

class Network:
    def __init__(self, reputation_manager):
        self.reputation_manager = reputation_manager

    def receive_triad(self, triad, proposing_node_id):
        """
        Receives a Triad from a node and processes it.
        """
        if self.reputation_manager.is_banned(proposing_node_id):
            print(f"Ignoring Triad from banned node {proposing_node_id}")
            return

        # Assume the triad is invalid for this simulation
        is_valid = False
        if not is_valid:
            self.reputation_manager.report_invalid_triad(proposing_node_id)
            if self.reputation_manager.should_ban(proposing_node_id):
                self.reputation_manager.ban(proposing_node_id)
                print(f"Node {proposing_node_id} has been banned.")

if __name__ == '__main__':
    reputation_manager = ReputationManager(ban_threshold=3)
    network = Network(reputation_manager)
    malicious_node = "malicious_node_123"

    # Malicious node sends invalid triads
    for i in range(5):
        print(f"Receiving triad {i+1} from {malicious_node}")
        network.receive_triad("invalid_triad", malicious_node)

    # Check if the node is banned
    if reputation_manager.is_banned(malicious_node):
        print(f"\n{malicious_node} is currently banned.")
    else:
        print(f"\n{malicious_node} is not banned.")
