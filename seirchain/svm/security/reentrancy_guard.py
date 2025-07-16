"""
Reentrancy Attack Protection

Implements reentrancy guards to protect smart contracts from reentrancy attacks
using mutex locks and state management.
"""

import threading
from typing import Dict, Any, Optional
from contextlib import contextmanager


class ReentrancyGuard:
    """
    Provides reentrancy protection for smart contracts using mutex locks.
    """
    
    def __init__(self):
        """Initialize the reentrancy guard."""
        self._locks: Dict[str, threading.Lock] = {}
        self._call_stack: Dict[str, int] = {}
        
    def _get_lock(self, contract_address: str) -> threading.Lock:
        """Get or create a lock for a specific contract."""
        if contract_address not in self._locks:
            self._locks[contract_address] = threading.Lock()
        return self._locks[contract_address]
    
    def is_locked(self, contract_address: str) -> bool:
        """Check if a contract is currently locked."""
        return self._call_stack.get(contract_address, 0) > 0
    
    @contextmanager
    def non_reentrant(self, contract_address: str):
        """
        Context manager for non-reentrant function calls.
        
        Args:
            contract_address: Address of the contract being protected
        """
        lock = self._get_lock(contract_address)
        
        if self.is_locked(contract_address):
            raise ReentrancyError("Reentrancy detected")
        
        lock.acquire()
        try:
            self._call_stack[contract_address] = self._call_stack.get(contract_address, 0) + 1
            yield
        finally:
            self._call_stack[contract_address] -= 1
            if self._call_stack[contract_address] <= 0:
                del self._call_stack[contract_address]
            lock.release()
    
    def protect_function(self, func):
        """
        Decorator to protect functions from reentrancy.
        
        Args:
            func: Function to protect
            
        Returns:
            Decorated function with reentrancy protection
        """
        def wrapper(self_instance, *args, **kwargs):
            contract_address = getattr(self_instance, 'address', 'default')
            with self.non_reentrant(contract_address):
                return func(self_instance, *args, **kwargs)
        return wrapper


class ReentrancyError(Exception):
    """Exception raised when reentrancy is detected."""
    pass


class VulnerableContract:
    """
    Example of a vulnerable smart contract that can be attacked via reentrancy.
    """
    
    def __init__(self, address: str):
        """Initialize the vulnerable contract."""
        self.address = address
        self.balances: Dict[str, int] = {}
        self.total_supply = 0
        
    def deposit(self, user: str, amount: int):
        """Deposit funds into the contract."""
        if user not in self.balances:
            self.balances[user] = 0
        self.balances[user] += amount
        self.total_supply += amount
        
    def withdraw(self, user: str, amount: int) -> bool:
        """
        Vulnerable withdraw function - can be reentered.
        
        Args:
            user: User address
            amount: Amount to withdraw
            
        Returns:
            True if withdrawal was successful
        """
        if user not in self.balances or self.balances[user] < amount:
            return False
            
        # VULNERABILITY: External call before state update
        # In a real attack, this would call an attacker's contract
        print(f"Sending {amount} to {user}")
        
        # State update happens after external call
        self.balances[user] -= amount
        self.total_supply -= amount
        
        return True


class SecureContract:
    """
    Example of a secure smart contract with reentrancy protection.
    """
    
    def __init__(self, address: str):
        """Initialize the secure contract."""
        self.address = address
        self.balances: Dict[str, int] = {}
        self.total_supply = 0
        self.reentrancy_guard = ReentrancyGuard()
        
    def deposit(self, user: str, amount: int):
        """Deposit funds into the contract."""
        if user not in self.balances:
            self.balances[user] = 0
        self.balances[user] += amount
        self.total_supply += amount
        
    def withdraw(self, user: str, amount: int) -> bool:
        """
        Secure withdraw function with reentrancy protection.
        
        Args:
            user: User address
            amount: Amount to withdraw
            
        Returns:
            True if withdrawal was successful
        """
        with self.reentrancy_guard.non_reentrant(self.address):
            if user not in self.balances or self.balances[user] < amount:
                return False
                
            # State update happens before external call
            self.balances[user] -= amount
            self.total_supply -= amount
            
            # Safe external call
            print(f"Sending {amount} to {user}")
            
            return True


class MutexLock:
    """
    Simple mutex implementation for reentrancy protection.
    """
    
    def __init__(self):
        """Initialize the mutex."""
        self._locked = False
        
    def acquire(self):
        """Acquire the mutex lock."""
        if self._locked:
            raise ReentrancyError("Mutex already locked")
        self._locked = True
        
    def release(self):
        """Release the mutex lock."""
        if not self._locked:
            raise RuntimeError("Mutex not locked")
        self._locked = False
        
    def __enter__(self):
        """Context manager entry."""
        self.acquire()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.release()


# Example usage
if __name__ == "__main__":
    # Test vulnerable contract
    vulnerable = VulnerableContract("0x123")
    vulnerable.deposit("user1", 100)
    vulnerable.withdraw("user1", 50)
    
    # Test secure contract
    secure = SecureContract("0x456")
    secure.deposit("user1", 100)
    secure.withdraw("user1", 50)
    
    # Test mutex
    mutex = MutexLock()
    with mutex:
        print("Mutex acquired and released safely")
