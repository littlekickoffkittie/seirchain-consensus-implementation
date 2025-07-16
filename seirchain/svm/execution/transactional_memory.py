"""
Transactional Memory for Optimistic Concurrency

Implements the SVM's optimistic concurrency by creating a TransactionalMemory
class that tracks read/write sets for transactions within the Triad Matrix.
"""

import threading
import time
from typing import Dict, Set, Any, List, Optional
from dataclasses import dataclass
from enum import Enum


class TransactionState(Enum):
    """States of a transaction in optimistic concurrency control."""
    ACTIVE = "active"
    VALIDATING = "validating"
    COMMITTED = "committed"
    ABORTED = "aborted"


@dataclass
class TransactionRecord:
    """Represents a transaction with its read/write sets."""
    tx_id: str
    read_set: Set[str]
    write_set: Set[str]
    state: TransactionState
    timestamp: float
    triad_id: int


class TransactionalMemory:
    """
    Implements optimistic concurrency control for the SeirChain Virtual Machine.
    
    Tracks read/write sets for transactions and ensures consistency
    across parallel execution within Triads.
    """
    
    def __init__(self):
        """Initialize the transactional memory system."""
        self.transactions: Dict[str, TransactionRecord] = {}
        self.global_state: Dict[str, Any] = {}
        self.lock = threading.RLock()
        self.version_counter = 0
        
    def begin_transaction(self, tx_id: str, triad_id: int) -> bool:
        """
        Begin a new transaction.
        
        Args:
            tx_id: Unique transaction identifier
            triad_id: The triad ID where this transaction executes
            
        Returns:
            True if transaction started successfully
        """
        with self.lock:
            if tx_id in self.transactions:
                return False
                
            self.transactions[tx_id] = TransactionRecord(
                tx_id=tx_id,
                read_set=set(),
                write_set=set(),
                state=TransactionState.ACTIVE,
                timestamp=time.time(),
                triad_id=triad_id
            )
            return True
    
    def read(self, tx_id: str, key: str) -> Any:
        """
        Read a value within a transaction.
        
        Args:
            tx_id: Transaction ID
            key: Key to read
            
        Returns:
            Value associated with the key
        """
        with self.lock:
            if tx_id not in self.transactions:
                raise ValueError(f"Transaction {tx_id} not found")
                
            tx = self.transactions[tx_id]
            if tx.state != TransactionState.ACTIVE:
                raise ValueError(f"Transaction {tx_id} not active")
                
            # Add to read set
            tx.read_set.add(key)
            
            # Return current value
            return self.global_state.get(key)
    
    def write(self, tx_id: str, key: str, value: Any) -> bool:
        """
        Write a value within a transaction.
        
        Args:
            tx_id: Transaction ID
            key: Key to write
            value: Value to write
            
        Returns:
            True if write was successful
        """
        with self.lock:
            if tx_id not in self.transactions:
                return False
                
            tx = self.transactions[tx_id]
            if tx.state != TransactionState.ACTIVE:
                return False
                
            # Add to write set
            tx.write_set.add(key)
            return True
    
    def validate_transaction(self, tx_id: str) -> bool:
        """
        Validate a transaction using optimistic concurrency control.
        
        Args:
            tx_id: Transaction ID to validate
            
        Returns:
            True if transaction can commit, False if it should abort
        """
        with self.lock:
            if tx_id not in self.transactions:
                return False
                
            tx = self.transactions[tx_id]
            if tx.state != TransactionState.ACTIVE:
                return False
                
            tx.state = TransactionState.VALIDATING
            
            # Check for conflicts with other transactions
            for other_tx_id, other_tx in self.transactions.items():
                if other_tx_id == tx_id:
                    continue
                    
                # Check for write-write conflicts
                if other_tx.state == TransactionState.COMMITTED:
                    if tx.write_set & other_tx.write_set:
                        return False
                        
                # Check for read-write conflicts
                if other_tx.state == TransactionState.COMMITTED:
                    if tx.read_set & other_tx.write_set:
                        return False
            
            return True
    
    def commit_transaction(self, tx_id: str) -> bool:
        """
        Commit a validated transaction.
        
        Args:
            tx_id: Transaction ID to commit
            
        Returns:
            True if commit was successful
        """
        with self.lock:
            if tx_id not in self.transactions:
                return False
                
            tx = self.transactions[tx_id]
            if tx.state != TransactionState.VALIDATING:
                return False
            
            # Apply writes to global state
            for key in tx.write_set:
                # In a real implementation, we'd store the actual values
                # For now, we'll just mark them as modified
                self.global_state[key] = f"modified_by_{tx_id}"
            
            tx.state = TransactionState.COMMITTED
            self.version_counter += 1
            return True
    
    def abort_transaction(self, tx_id: str) -> bool:
        """
        Abort a transaction.
        
        Args:
            tx_id: Transaction ID to abort
            
        Returns:
            True if abort was successful
        """
        with self.lock:
            if tx_id not in self.transactions:
                return False
                
            tx = self.transactions[tx_id]
            tx.state = TransactionState.ABORTED
            return True
    
    def get_transaction_state(self, tx_id: str) -> Optional[TransactionState]:
        """
        Get the current state of a transaction.
        
        Args:
            tx_id: Transaction ID
            
        Returns:
            Current transaction state or None if not found
        """
        with self.lock:
            tx = self.transactions.get(tx_id)
            return tx.state if tx else None
    
    def get_active_transactions(self, triad_id: int = None) -> List[str]:
        """
        Get list of active transaction IDs.
        
        Args:
            triad_id: Optional triad ID to filter by
            
        Returns:
            List of active transaction IDs
        """
        with self.lock:
            active = []
            for tx_id, tx in self.transactions.items():
                if tx.state == TransactionState.ACTIVE:
                    if triad_id is None or tx.triad_id == triad_id:
                        active.append(tx_id)
            return active
    
    def get_conflict_summary(self) -> Dict[str, Any]:
        """
        Get summary of transaction conflicts.
        
        Returns:
            Dictionary with conflict statistics
        """
        with self.lock:
            total = len(self.transactions)
            active = sum(1 for tx in self.transactions.values() 
                        if tx.state == TransactionState.ACTIVE)
            committed = sum(1 for tx in self.transactions.values() 
                          if tx.state == TransactionState.COMMITTED)
            aborted = sum(1 for tx in self.transactions.values() 
                        if tx.state == TransactionState.ABORTED)
            
            return {
                'total_transactions': total,
                'active': active,
                'committed': committed,
                'aborted': aborted,
                'success_rate': committed / total if total > 0 else 0
            }
    
    def cleanup_old_transactions(self, max_age: float = 300.0):
        """
        Clean up old completed transactions.
        
        Args:
            max_age: Maximum age in seconds before cleanup
        """
        with self.lock:
            current_time = time.time()
            to_remove = []
            
            for tx_id, tx in self.transactions.items():
                if tx.state in [TransactionState.COMMITTED, TransactionState.ABORTED]:
                    if current_time - tx.timestamp > max_age:
                        to_remove.append(tx_id)
            
            for tx_id in to_remove:
                del self.transactions[tx_id]


class MultiTriadMemory:
    """
    Manages transactional memory across multiple Triads.
    """
    
    def __init__(self):
        """Initialize multi-triad memory system."""
        self.triads: Dict[int, TransactionalMemory] = {}
        
    def get_triad_memory(self, triad_id: int) -> TransactionalMemory:
        """
        Get or create transactional memory for a specific triad.
        
        Args:
            triad_id: The triad ID
            
        Returns:
            TransactionalMemory instance for the triad
        """
        if triad_id not in self.triads:
            self.triads[triad_id] = TransactionalMemory()
        return self.triads[triad_id]
    
    def begin_cross_shard_transaction(self, tx_id: str, triad_ids: List[int]) -> Dict[int, bool]:
        """
        Begin a transaction that spans multiple triads.
        
        Args:
            tx_id: Transaction ID
            triad_ids: List of triad IDs involved
            
        Returns:
            Dictionary mapping triad IDs to success status
        """
        results = {}
        for triad_id in triad_ids:
            memory = self.get_triad_memory(triad_id)
            results[triad_id] = memory.begin_transaction(f"{tx_id}_{triad_id}", triad_id)
        return results


# Example usage
if __name__ == "__main__":
    # Test basic transactional memory
    memory = TransactionalMemory()
    
    # Start a transaction
    tx_id = "tx_001"
    memory.begin_transaction(tx_id, triad_id=1)
    
    # Perform reads and writes
    memory.write(tx_id, "balance_alice", 100)
    memory.write(tx_id, "balance_bob", 200)
    
    # Validate and commit
    if memory.validate_transaction(tx_id):
        success = memory.commit_transaction(tx_id)
        print(f"Transaction committed: {success}")
    else:
        memory.abort_transaction(tx_id)
        print("Transaction aborted due to conflicts")
    
    # Check state
    print(f"Transaction state: {memory.get_transaction_state(tx_id)}")
    print(f"Conflict summary: {memory.get_conflict_summary()}")
