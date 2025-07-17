"""
Triad-Based Sharding Module

Implements deterministic hashing functions for mapping smart contracts and accounts
to specific Triad IDs (shards) in the SeirChain Virtual Machine.
"""

from .triad_sharding import TriadSharding
from .cross_shard import TwoPhaseCommit

__all__ = ['TriadSharding', 'TwoPhaseCommit']
