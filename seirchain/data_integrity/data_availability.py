import random

class FullNode:
    def __init__(self, triad_data):
        self.triad_data = triad_data
        self.chunk_size = 256 # bytes
        self.chunks = self._chunk_data()

    def _chunk_data(self):
        """
        Splits the triad data into smaller chunks.
        """
        return [self.triad_data[i:i + self.chunk_size] for i in range(0, len(self.triad_data), self.chunk_size)]

    def get_chunk(self, chunk_index):
        """
        Returns a specific chunk of the triad data.
        """
        if chunk_index < len(self.chunks):
            return self.chunks[chunk_index]
        return None

class LightClient:
    def __init__(self, full_node, num_chunks):
        self.full_node = full_node
        self.num_chunks = num_chunks

    def check_availability(self, num_samples=5):
        """
        Checks data availability by sampling random chunks.
        """
        if num_samples > self.num_chunks:
            num_samples = self.num_chunks

        sampled_indices = random.sample(range(self.num_chunks), num_samples)

        for index in sampled_indices:
            chunk = self.full_node.get_chunk(index)
            if chunk is None:
                # If any requested chunk is missing, data is not available.
                return False
        return True

if __name__ == '__main__':
    # Simulate some triad data
    triad_data = b"a" * 1024 * 10 # 10 KB of data

    # A full node has the complete data
    full_node = FullNode(triad_data)

    # A light client wants to verify data availability
    light_client = LightClient(full_node, len(full_node.chunks))

    # Check availability
    is_available = light_client.check_availability()
    print(f"Is the data available (according to the light client)? {is_available}")

    # Simulate a case where the full node is malicious and withholds data
    class MaliciousFullNode(FullNode):
        def get_chunk(self, chunk_index):
            # This malicious node withholds the last 5 chunks
            if chunk_index >= len(self.chunks) - 5:
                return None
            return super().get_chunk(chunk_index)

    malicious_node = MaliciousFullNode(triad_data)
    light_client_with_malicious_node = LightClient(malicious_node, len(malicious_node.chunks))

    # The light client will likely detect the missing data
    # We run this multiple times to show that it will eventually fail
    for i in range(10):
        is_available_malicious = light_client_with_malicious_node.check_availability(num_samples=10)
        print(f"Run {i+1}: Is the data available from the malicious node? {is_available_malicious}")
        if not is_available_malicious:
            break
