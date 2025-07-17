"""
Two-Phase Commit Protocol for Cross-Shard Transactions

Implements a simple two-phase commit protocol for ensuring atomicity
in cross-shard transactions between Triads in the SeirChain Virtual Machine.
"""

import uuid
import time
from typing import Dict, List, Any, Optional
from enum import Enum
from dataclasses import dataclass


class TransactionStatus(Enum):
    """Status of a cross-shard transaction."""
    INITIATED = "initiated"
    PREPARING = "preparing"
    PREPARED = "prepared"
    COMMITTING = "committing"
    COMMITTED = "committed"
    ABORTING = "aborting"
    ABORTED = "aborted"


@dataclass
class CrossShardTransaction:
    """Represents a cross-shard transaction."""
    tx_id: str
    triad_ids: List[int]
    operations: Dict[int, Any]  # triad_id -> operations
    status: TransactionStatus
    coordinator_triad: int
    participants: Dict[int, bool]  # triad_id -> prepared status
    timestamp: float


class TwoPhaseCommit:
    """
    Implements the two-phase commit protocol for cross-shard transactions.
    
    Ensures atomicity across multiple Triads in the SeirChain Virtual Machine.
    """
    
    def __init__(self):
        """Initialize the two-phase commit coordinator."""
        self.transactions: Dict[str, CrossShardTransaction] = {}
        self.pending_operations: Dict[str, Dict[int, Any]] = {}
        
    def begin_cross_shard_transaction(self, triad_ids: List[int], 
                                    operations: Dict[int, Any],
                                    coordinator_triad: int = None) -> str:
        """
        Begin a new cross-shard transaction.
        
        Args:
            triad_ids: List of triad IDs involved in the transaction
            operations: Dictionary mapping triad IDs to their operations
            coordinator_triad: The triad acting as coordinator
            
        Returns:
            Transaction ID
        """
        tx_id = str(uuid.uuid4())
        
        if coordinator_triad is None:
            coordinator_triad = triad_ids[0]
            
        self.transactions[tx_id] = CrossShardTransaction(
            tx_id=tx_id,
            triad_ids=triad_ids,
            operations=operations,
            status=TransactionStatus.INITIATED,
            coordinator_triad=coordinator_triad,
            participants={triad_id: False for triad_id in triad_ids},
            timestamp=time.time()
        )
        
        return tx_id
    
    def prepare_phase(self, tx_id: str) -> Dict[int, bool]:
        """
        Execute the prepare phase of the two-phase commit.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Dictionary mapping triad IDs to their prepare status
        """
        if tx_id not in self.transactions:
            return {}
            
        transaction = self.transactions[tx_id]
        transaction.status = TransactionStatus.PREPARING
        
        # Simulate preparing each participant
        prepare_results = {}
        for triad_id in transaction.triad_ids:
            # In a real implementation, this would involve network communication
            # For simulation, we'll randomly decide if preparation succeeds
            import random
            prepare_success = random.random() > 0.1  # 90% success rate
            prepare_results[triad_id] = prepare_success
            transaction.participants[triad_id] = prepare_success
        
        # Check if all participants prepared successfully
        all_prepared = all(transaction.participants.values())
        
        if all_prepared:
            transaction.status = TransactionStatus.PREPARED
        else:
            transaction.status = TransactionStatus.ABORTING
            
        return prepare_results
    
    def commit_phase(self, tx_id: str) -> bool:
        """
        Execute the commit phase of the two-phase commit.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            True if commit was successful, False otherwise
        """
        if tx_id not in self.transactions:
            return False
            
        transaction = self.transactions[tx_id]
        
        if transaction.status != TransactionStatus.PREPARED:
            return False
            
        transaction.status = TransactionStatus.COMMITTING
        
        # Simulate committing each participant
        commit_success = True
        for triad_id in transaction.triad_ids:
            # In a real implementation, this would involve network communication
            # For simulation, we'll assume commit succeeds if prepared
            if not transaction.participants[triad_id]:
                commit_success = False
                break
        
        if commit_success:
            transaction.status = TransactionStatus.COMMITTED
            # Apply the actual operations here
            self._apply_operations(transaction)
        else:
            transaction.status = TransactionStatus.ABORTED
            
        return commit_success
    
    def abort_transaction(self, tx_id: str) -> bool:
        """
        Abort a cross-shard transaction.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            True if abort was successful
        """
        if tx_id not in self.transactions:
            return False
            
        transaction = self.transactions[tx_id]
        transaction.status = TransactionStatus.ABORTING
        
        # Simulate aborting each participant
        for triad_id in transaction.triad_ids:
            # In a real implementation, this would involve network communication
            pass
            
        transaction.status = TransactionStatus.ABORTED
        return True
    
    def _apply_operations(self, transaction: CrossShardTransaction):
        """
        Apply the operations of a committed transaction.
        
        Args:
            transaction: The committed transaction
        """
        # In a real implementation, this would execute the actual operations
        # For now, we'll just log them
        for triad_id, operation in transaction.operations.items():
            print(f"Applying operation to triad {triad_id}: {operation}")
    
    def get_transaction_status(self, tx_id: str) -> Optional[TransactionStatus]:
        """
        Get the current status of a transaction.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Current transaction status or None if not found
        """
        if tx_id not in self.transactions:
            return None
        return self.transactions[tx_id].status
    
    def get_transaction_info(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information about a transaction.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Dictionary with transaction information
        """
        if tx_id not in self.transactions:
            return None
            
        transaction = self.transactions[tx_id]
        return {
            'tx_id': transaction.tx_id,
            'triad_ids': transaction.triad_ids,
            'status': transaction.status.value,
            'coordinator_triad': transaction.coordinator_triad,
            'participants': transaction.participants,
            'timestamp': transaction.timestamp
        }
    
    def cleanup_old_transactions(self, max_age: float = 3600.0):
        """
        Clean up old completed transactions.
        
        Args:
            max_age: Maximum age in seconds before cleanup
        """
        current_time = time.time()
        to_remove = []
        
        for tx_id, transaction in self.transactions.items():
            if transaction.status in [TransactionStatus.COMMITTED, TransactionStatus.ABORTED]:
                if current_time - transaction.timestamp > max_age:
                    to_remove.append(tx_id)
        
        for tx_id in to_remove:
            del self.transactions[tx_id]


class CrossShardCoordinator:
    """
    Coordinates cross-shard transactions across the Triad Matrix.
    """
    
    def __init__(self, two_phase_commit: TwoPhaseCommit):
        """
        Initialize the coordinator.
        
        Args:
            two_phase_commit: TwoPhaseCommit instance
        """
        self.two_phase_commit = two_phase_commit
        
    def execute_cross_shard_transfer(self, from_triad: int, to_triad: int, 
                                   amount: float, from_address: str, 
                                   to_address: str) -> str:
        """
        Execute a cross-shard token transfer.
        
        Args:
            from_triad: Source triad ID
            to_triad: Destination triad ID
            amount: Amount to transfer
            from_address: Source address
            to_address: Destination address
            
        Returns:
            Transaction ID
        """
        operations = {
            from_triad: {
                'type': 'debit',
                'address': from_address,
                'amount': amount
            },
            to_triad: {
                'type': 'credit',
                'address': to_address,
                'amount': amount
            }
        }
        
        tx_id = self.two_phase_commit.begin_cross_shard_transaction(
            [from_triad, to_triad], operations, from_triad
        )
        
        # Execute the two-phase commit
        prepare_results = self.two_phase_commit.prepare_phase(tx_id)
        
        # Check if all participants prepared successfully
        if all(prepare_results.values()):
            success = self.two_phase_commit.commit_phase(tx_id)
            return tx_id if success else None
        else:
            self.two_phase_commit.abort_transaction(tx_id)
            return None
    
    def execute_multi_shard_operation(self, triad_operations: Dict[int, Any]) -> str:
        """
        Execute an operation across multiple shards.
        
        Args:
            triad_operations: Dictionary mapping triad IDs to operations
            
        Returns:
            Transaction ID
        """
        triad_ids = list(triad_operations.keys())
        tx_id = self.two_phase_commit.begin_cross_shard_transaction(
            triad_ids, triad_operations
        )
        
        # Execute the two-phase commit
        prepare_results = self.two_phase_commit.prepare_phase(tx_id)
        
        if all(prepare_results.values()):
            success = self.two_phase_commit.commit_phase(tx_id)
            return tx_id if success else None
        else:
            self.two_phase_commit.abort_transaction(tx_id)
            return None


# Example usage
if __name__ == "__main__":
    # Test two-phase commit
    coordinator = TwoPhaseCommit()
    
    # Create a cross-shard transaction
    triad_ids = [1, 2, 3]
    operations = {
        1: {'action': 'transfer', 'amount': 100},
        2: {'action': 'update_balance', 'amount': 100},
        3: {'action': 'log_transaction', 'amount': 100}
    }
    
    tx_id = coordinator.begin_cross_shard_transaction(triad_ids, operations)
    print(f"Started transaction: {tx_id}")
    
    # Prepare phase
    prepare_results = coordinator.prepare_phase(tx_id)
    print(f"Prepare results: {prepare_results}")
    
    # Commit phase
    success = coordinator.commit_phase(tx_id)
    print(f"Transaction committed: {success}")
    
    # Check status
    status = coordinator.get_transaction_status(tx_id)
    print(f"Final status: {status}")
