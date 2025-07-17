"""
SeirChain Virtual Machine (SVM) - Complete Implementation

This package implements the complete SeirChain Virtual Machine with all components
for secure smart contract execution, parallel processing, and cross-shard transactions.
"""

from .sharding import TriadSharding, TwoPhaseCommit
from .execution import TransactionalMemory, GasCalculator, ParallelExecutor
from .security import SecureExecutionEnvironment, ReentrancyGuard, SafeMath
from .execution.parallel import ParallelExecutor

__all__ = [
    'TriadSharding',
    'TwoPhaseCommit',
    'TransactionalMemory',
    'GasCalculator',
    'SecureExecutionEnvironment',
    'ReentrancyGuard',
    'SafeMath',
    'ParallelExecutor'
]

# Export main SVM components
__version__ = "1.0.0"
__author__ = "SeirChain Team"
__description__ = "SeirChain Virtual Machine for secure smart contract execution"
