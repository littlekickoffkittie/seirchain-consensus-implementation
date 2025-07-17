"""
Triad-Based Sharding Implementation

This module implements the deterministic hashing function that assigns
smart contract and account addresses to specific Triad IDs (shards).
"""

import hashlib
from typing import Tuple, Dict, Any
from seirchain.structures.triad import Triad


class TriadSharding:
    """
    Implements Triad-based sharding for the SeirChain Virtual Machine.
    
    Uses deterministic hashing to map addresses to specific Triad IDs,
    ensuring consistent shard assignment across the network.
    """
    
    def __init__(self, num_triads: int = 1024):
        """
        Initialize the sharding system.
        
        Args:
            num_triads: Total number of triads (shards) in the system
        """
        self.num_triads = num_triads
        self.shard_mapping: Dict[str, int] = {}
        
    def _hash_address(self, address: str) -> str:
        """
        Create a deterministic hash for an address.
        
        Args:
            address: Smart contract or account address
            
        Returns:
            SHA-256 hash as hexadecimal string
        """
        return hashlib.sha256(address.encode()).hexdigest()
    
    def get_triad_id(self, address: str) -> int:
        """
        Determine which Triad ID (shard) an address belongs to.
        
        Args:
            address: Smart contract or account address
            
        Returns:
            Triad ID (shard number) between 0 and num_triads-1
        """
        if address in self.shard_mapping:
            return self.shard_mapping[address]
            
        # Create deterministic hash
        hash_hex = self._hash_address(address)
        
        # Convert first 8 bytes of hash to integer
        hash_int = int(hash_hex[:16], 16)
        
        # Map to triad ID using modulo
        triad_id = hash_int % self.num_triads
        
        # Cache the mapping
        self.shard_mapping[address] = triad_id
        
        return triad_id
    
    def get_shard_range(self, triad_id: int) -> Tuple[int, int]:
        """
        Get the address range for a specific triad shard.
        
        Args:
            triad_id: The triad ID
            
        Returns:
            Tuple of (start_hash, end_hash) for the shard range
        """
        range_size = 2**256 // self.num_triads
        start_hash = triad_id * range_size
        end_hash = (triad_id + 1) * range_size - 1
        
        return (start_hash, end_hash)
    
    def is_address_in_triad(self, address: str, triad_id: int) -> bool:
        """
        Check if an address belongs to a specific triad.
        
        Args:
            address: The address to check
            triad_id: The triad ID to check against
            
        Returns:
            True if address belongs to the triad, False otherwise
        """
        return self.get_triad_id(address) == triad_id
    
    def get_addresses_for_triad(self, addresses: list, triad_id: int) -> list:
        """
        Filter addresses that belong to a specific triad.
        
        Args:
            addresses: List of addresses to filter
            triad_id: The triad ID to filter for
            
        Returns:
            List of addresses that belong to the specified triad
        """
        return [addr for addr in addresses if self.get_triad_id(addr) == triad_id]
    
    def get_shard_distribution(self, addresses: list) -> Dict[int, int]:
        """
        Get the distribution of addresses across shards.
        
        Args:
            addresses: List of addresses to analyze
            
        Returns:
            Dictionary mapping triad IDs to count of addresses
        """
        distribution = {}
        for address in addresses:
            triad_id = self.get_triad_id(address)
            distribution[triad_id] = distribution.get(triad_id, 0) + 1
        return distribution


class FractalSharding(TriadSharding):
    """
    Advanced fractal sharding that considers the hierarchical structure
    of the Triad Matrix for more sophisticated shard assignment.
    """
    
    def __init__(self, max_depth: int = 10):
        """
        Initialize fractal sharding with hierarchical structure.
        
        Args:
            max_depth: Maximum depth of the fractal hierarchy
        """
        super().__init__(num_triads=3**max_depth)
        self.max_depth = max_depth
        
    def get_fractal_coordinates(self, address: str) -> Tuple[int, ...]:
        """
        Get the fractal coordinates for an address within the Triad Matrix.
        
        Args:
            address: The address to map
            
        Returns:
            Tuple of coordinates representing position in fractal hierarchy
        """
        triad_id = self.get_triad_id(address)
        
        # Convert to ternary representation for fractal coordinates
        coordinates = []
        temp = triad_id
        
        for _ in range(self.max_depth):
            coordinates.append(temp % 3)
            temp //= 3
            
        return tuple(reversed(coordinates))
    
    def get_parent_triad(self, triad_id: int) -> int:
        """
        Get the parent triad ID in the fractal hierarchy.
        
        Args:
            triad_id: The child triad ID
            
        Returns:
            Parent triad ID
        """
        return triad_id // 3
    
    def get_child_triads(self, triad_id: int) -> list:
        """
        Get the child triad IDs in the fractal hierarchy.
        
        Args:
            triad_id: The parent triad ID
            
        Returns:
            List of child triad IDs
        """
        base = triad_id * 3
        return [base, base + 1, base + 2]


# Example usage and testing
if __name__ == "__main__":
    # Test basic sharding
    sharding = TriadSharding(num_triads=64)
    
    test_addresses = [
        "0x1234567890abcdef1234567890abcdef12345678",
        "0xabcdef1234567890abcdef1234567890abcdef12",
        "0x1111111111111111111111111111111111111111",
        "0x2222222222222222222222222222222222222222"
    ]
    
    print("Basic Triad Sharding:")
    for addr in test_addresses:
        triad_id = sharding.get_triad_id(addr)
        print(f"Address {addr[:10]}... -> Triad {triad_id}")
    
    # Test fractal sharding
    fractal_sharding = FractalSharding(max_depth=4)
    
    print("\nFractal Sharding:")
    for addr in test_addresses[:2]:
        coords = fractal_sharding.get_fractal_coordinates(addr)
        triad_id = fractal_sharding.get_triad_id(addr)
        print(f"Address {addr[:10]}... -> Triad {triad_id}, Coordinates {coords}")
