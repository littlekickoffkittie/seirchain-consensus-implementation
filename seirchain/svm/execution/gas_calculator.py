"""
Gas Calculation Module

Implements the gas calculation system for determining the execution cost
of smart contracts based on their operation codes and resource usage.
"""

from typing import Dict, Any, List
from enum import Enum


class Opcode(Enum):
    """Smart contract operation codes with their gas costs."""
    # Basic operations
    STOP = 0
    ADD = 3
    MUL = 5
    SUB = 3
    DIV = 5
    SDIV = 5
    MOD = 5
    SMOD = 5
    ADDMOD = 8
    MULMOD = 8
    EXP = 10
    SIGNEXTEND = 5
    
    # Comparison & bitwise operations
    LT = 3
    GT = 3
    SLT = 3
    SGT = 3
    EQ = 3
    ISZERO = 3
    AND = 3
    OR = 3
    XOR = 3
    NOT = 3
    BYTE = 3
    SHL = 3
    SHR = 3
    SAR = 3
    
    # SHA3
    SHA3 = 30
    
    # Environmental information
    ADDRESS = 2
    BALANCE = 400
    ORIGIN = 2
    CALLER = 2
    CALLVALUE = 2
    CALLDATALOAD = 3
    CALLDATASIZE = 2
    CALLDATACOPY = 3
    CODESIZE = 2
    CODECOPY = 3
    GASPRICE = 2
    EXTCODESIZE = 700
    EXTCODECOPY = 700
    RETURNDATASIZE = 2
    RETURNDATACOPY = 3
    
    # Block information
    BLOCKHASH = 20
    COINBASE = 2
    TIMESTAMP = 2
    NUMBER = 2
    DIFFICULTY = 2
    GASLIMIT = 2
    
    # Memory operations
    POP = 2
    MLOAD = 3
    MSTORE = 3
    MSTORE8 = 3
    SLOAD = 800
    SSTORE = 20000
    
    # Call operations
    CALL = 700
    CALLCODE = 700
    DELEGATECALL = 700
    STATICCALL = 700
    
    # Storage operations
    CREATE = 32000
    CREATE2 = 32000
    RETURN = 0
    REVERT = 0
    SELFDESTRUCT = 5000


class GasCalculator:
    """
    Calculates gas costs for smart contract execution based on operation codes.
    """
    
    def __init__(self):
        """Initialize the gas calculator."""
        self.base_gas_costs = {
            opcode: opcode.value for opcode in Opcode
        }
        
        # Additional gas costs for memory and storage
        self.memory_gas_cost = 3  # Gas per word
        self.storage_gas_cost = 20000  # Gas per storage slot
        
    def calculate_opcode_gas(self, opcode: Opcode, *args) -> int:
        """
        Calculate gas cost for a single operation.
        
        Args:
            opcode: The operation code
            *args: Additional arguments that might affect gas cost
            
        Returns:
            Gas cost for the operation
        """
        base_cost = self.base_gas_costs.get(opcode, 0)
        
        # Additional costs based on operation type
        if opcode == Opcode.SHA3:
            # SHA3 has additional cost based on data size
            if args and len(args) > 0:
                data_size = args[0]
                return base_cost + (data_size * 6)
                
        elif opcode == Opcode.SSTORE:
            # SSTORE has different costs for zero vs non-zero storage
            if args and len(args) >= 2:
                old_value = args[0]
                new_value = args[1]
                if old_value == 0 and new_value != 0:
                    return 20000  # Storage creation
                elif old_value != 0 and new_value == 0:
                    return 5000   # Storage deletion refund
                else:
                    return 5000   # Storage update
        
        elif opcode in [Opcode.CALL, Opcode.CALLCODE, 
                       Opcode.DELEGATECALL, Opcode.STATICCALL]:
            # Call operations have additional gas based on call data
            if args and len(args) > 0:
                call_data_size = args[0] if args[0] else 0
                return base_cost + (call_data_size * 3)
                
        return base_cost
    
    def calculate_memory_gas(self, memory_size: int) -> int:
        """
        Calculate gas cost for memory usage.
        
        Args:
            memory_size: Size of memory in bytes
            
        Returns:
            Gas cost for memory usage
        """
        if memory_size == 0:
            return 0
            
        # Memory gas cost is quadratic
        words = (memory_size + 31) // 32
        return words * self.memory_gas_cost + (words * words) // 512
    
    def calculate_storage_gas(self, storage_slots: int) -> int:
        """
        Calculate gas cost for storage operations.
        
        Args:
            storage_slots: Number of storage slots accessed
            
        Returns:
            Gas cost for storage operations
        """
        return storage_slots * self.storage_gas_cost
    
    def calculate_transaction_gas(self, bytecode: List[Dict[str, Any]], 
                                memory_size: int = 0, 
                                storage_slots: int = 0) -> Dict[str, int]:
        """
        Calculate total gas cost for a smart contract execution.
        
        Args:
            bytecode: List of operations with their arguments
            memory_size: Total memory usage in bytes
            storage_slots: Number of storage slots accessed
            
        Returns:
            Dictionary with detailed gas breakdown
        """
        total_gas = 0
        opcode_gas = 0
        memory_gas = 0
        storage_gas = 0
        
        # Calculate opcode gas
        for operation in bytecode:
            opcode = operation.get('opcode')
            args = operation.get('args', [])
            gas = self.calculate_opcode_gas(opcode, *args)
            opcode_gas += gas
            
        # Calculate memory gas
        memory_gas = self.calculate_memory_gas(memory_size)
        
        # Calculate storage gas
        storage_gas = self.calculate_storage_gas(storage_slots)
        
        total_gas = opcode_gas + memory_gas + storage_gas
        
        return {
            'total_gas': total_gas,
            'opcode_gas': opcode_gas,
            'memory_gas': memory_gas,
            'storage_gas': storage_gas
        }
    
    def estimate_gas_limit(self, bytecode: List[Dict[str, Any]], 
                         memory_size: int = 0, 
                         storage_slots: int = 0) -> int:
        """
        Estimate the gas limit needed for a smart contract execution.
        
        Args:
            bytecode: List of operations with their arguments
            memory_size: Estimated memory usage in bytes
            storage_slots: Estimated storage slots to access
            
        Returns:
            Estimated gas limit
        """
        gas_breakdown = self.calculate_transaction_gas(bytecode, memory_size, storage_slots)
        
        # Add 20% buffer for safety
        return int(gas_breakdown['total_gas'] * 1.2)
    
    def validate_gas_limit(self, gas_limit: int, bytecode: List[Dict[str, Any]], 
                          memory_size: int = 0, storage_slots: int = 0) -> bool:
        """
        Validate if the provided gas limit is sufficient.
        
        Args:
            gas_limit: The gas limit to validate
            bytecode: List of operations with their arguments
            memory_size: Memory usage in bytes
            storage_slots: Storage slots to access
            
        Returns:
            True if gas limit is sufficient, False otherwise
        """
        required_gas = self.calculate_transaction_gas(bytecode, memory_size, storage_slots)
        return gas_limit >= required_gas['total_gas']


# Example usage
if __name__ == "__main__":
    calculator = GasCalculator()
    
    # Example bytecode
    bytecode = [
        {'opcode': Opcode.PUSH1, 'args': [100]},
        {'opcode': Opcode.PUSH1, 'args': [200]},
        {'opcode': Opcode.ADD},
        {'opcode': Opcode.SSTORE, 'args': [0, 300]},
        {'opcode': Opcode.LOG1}
    ]
    
    gas_breakdown = calculator.calculate_transaction_gas(
        bytecode, 
        memory_size=1024, 
        storage_slots=2
    )
    
    print("Gas Breakdown:")
    print(f"Total Gas: {gas_breakdown['total_gas']}")
    print(f"Opcode Gas: {gas_breakdown['opcode_gas']}")
    print(f"Memory Gas: {gas_breakdown['memory_gas']}")
    print(f"Storage Gas: {gas_breakdown['storage_gas']}")
    
    estimated_limit = calculator.estimate_gas_limit(bytecode, 1024, 2)
    print(f"Estimated Gas Limit: {estimated_limit}")
