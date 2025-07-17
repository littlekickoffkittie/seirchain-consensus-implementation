"""
Safe Math Library

Provides secure mathematical operations for smart contracts to prevent
integer overflow and underflow vulnerabilities.
"""

import sys
from typing import Union


class SafeMath:
    """
    Safe mathematical operations with overflow/underflow protection.
    """
    
    # Define limits for different integer types
    INT8_MIN = -2**7
    INT8_MAX = 2**7 - 1
    INT16_MIN = -2**15
    INT16_MAX = 2**15 - 1
    INT32_MIN = -2**31
    INT32_MAX = 2**31 - 1
    INT64_MIN = -2**63
    INT64_MAX = 2**63 - 1
    INT128_MIN = -2**127
    INT128_MAX = 2**127 - 1
    INT256_MIN = -2**255
    INT256_MAX = 2**255 - 1
    
    UINT8_MAX = 2**8 - 1
    UINT16_MAX = 2**16 - 1
    UINT32_MAX = 2**32 - 1
    UINT64_MAX = 2**64 - 1
    UINT128_MAX = 2**128 - 1
    UINT256_MAX = 2**256 - 1
    
    @staticmethod
    def add(a: int, b: int, max_value: int = UINT256_MAX, min_value: int = 0) -> int:
        """
        Safe addition with overflow protection.
        
        Args:
            a: First operand
            b: Second operand
            max_value: Maximum allowed value
            min_value: Minimum allowed value
            
        Returns:
            Sum of a and b
            
        Raises:
            OverflowError: If result would overflow
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Operands must be integers")
            
        result = a + b
        
        if result > max_value or result < min_value:
            raise OverflowError(f"Addition overflow: {a} + {b} = {result}")
            
        return result
    
    @staticmethod
    def sub(a: int, b: int, max_value: int = UINT256_MAX, min_value: int = 0) -> int:
        """
        Safe subtraction with underflow protection.
        
        Args:
            a: First operand
            b: Second operand
            max_value: Maximum allowed value
            min_value: Minimum allowed value
            
        Returns:
            Difference of a and b
            
        Raises:
            OverflowError: If result would underflow
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Operands must be integers")
            
        result = a - b
        
        if result > max_value or result < min_value:
            raise OverflowError(f"Subtraction underflow: {a} - {b} = {result}")
            
        return result
    
    @staticmethod
    def mul(a: int, b: int, max_value: int = UINT256_MAX, min_value: int = 0) -> int:
        """
        Safe multiplication with overflow protection.
        
        Args:
            a: First operand
            b: Second operand
            max_value: Maximum allowed value
            min_value: Minimum allowed value
            
        Returns:
            Product of a and b
            
        Raises:
            OverflowError: If result would overflow
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Operands must be integers")
            
        if a == 0 or b == 0:
            return 0
            
        # Check for overflow before multiplication
        if a > 0 and b > 0 and a > max_value // b:
            raise OverflowError(f"Multiplication overflow: {a} * {b}")
        if a < 0 and b < 0 and a < min_value // b:
            raise OverflowError(f"Multiplication overflow: {a} * {b}")
        if (a > 0 and b < 0) or (a < 0 and b > 0):
            abs_result = abs(a) * abs(b)
            if abs_result > max(abs(max_value), abs(min_value)):
                raise OverflowError(f"Multiplication overflow: {a} * {b}")
                
        result = a * b
        
        if result > max_value or result < min_value:
            raise OverflowError(f"Multiplication overflow: {a} * {b} = {result}")
            
        return result
    
    @staticmethod
    def div(a: int, b: int, max_value: int = UINT256_MAX, min_value: int = 0) -> int:
        """
        Safe division with protection against division by zero.
        
        Args:
            a: Dividend
            b: Divisor
            max_value: Maximum allowed value
            min_value: Minimum allowed value
            
        Returns:
            Quotient of a and b
            
        Raises:
            ZeroDivisionError: If b is zero
            OverflowError: If result would overflow
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Operands must be integers")
            
        if b == 0:
            raise ZeroDivisionError("Division by zero")
            
        result = a // b
        
        if result > max_value or result < min_value:
            raise OverflowError(f"Division overflow: {a} / {b} = {result}")
            
        return result
    
    @staticmethod
    def mod(a: int, b: int) -> int:
        """
        Safe modulo operation.
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Remainder of a divided by b
            
        Raises:
            ZeroDivisionError: If b is zero
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Operands must be integers")
            
        if b == 0:
            raise ZeroDivisionError("Modulo by zero")
            
        return a % b
    
    @staticmethod
    def pow(a: int, b: int, max_value: int = UINT256_MAX, min_value: int = 0) -> int:
        """
        Safe exponentiation with overflow protection.
        
        Args:
            a: Base
            b: Exponent
            max_value: Maximum allowed value
            min_value: Minimum allowed value
            
        Returns:
            a raised to the power of b
            
        Raises:
            OverflowError: If result would overflow
        """
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Operands must be integers")
            
        if b < 0:
            raise ValueError("Negative exponent not supported")
            
        if b == 0:
            return 1
            
        if a == 0:
            return 0
            
        # Check for overflow
        if a > 1 and b > 0:
            temp = 1
            for _ in range(b):
                temp *= a
                if temp > max_value:
                    raise OverflowError(f"Exponentiation overflow: {a} ** {b}")
            return temp
            
        result = a ** b
        
        if result > max_value or result < min_value:
            raise OverflowError(f"Exponentiation overflow: {a} ** {b} = {result}")
            
        return result
    
    @classmethod
    def safe_uint8(cls, value: int) -> int:
        """Convert value to safe uint8."""
        if value < 0 or value > cls.UINT8_MAX:
            raise OverflowError(f"Value {value} out of uint8 range")
        return value
    
    @classmethod
    def safe_uint16(cls, value: int) -> int:
        """Convert value to safe uint16."""
        if value < 0 or value > cls.UINT16_MAX:
            raise OverflowError(f"Value {value} out of uint16 range")
        return value
    
    @classmethod
    def safe_uint32(cls, value: int) -> int:
        """Convert value to safe uint32."""
        if value < 0 or value > cls.UINT32_MAX:
            raise OverflowError(f"Value {value} out of uint32 range")
        return value
    
    @classmethod
    def safe_uint64(cls, value: int) -> int:
        """Convert value to safe uint64."""
        if value < 0 or value > cls.UINT64_MAX:
            raise OverflowError(f"Value {value} out of uint64 range")
        return value
    
    @classmethod
    def safe_uint256(cls, value: int) -> int:
        """Convert value to safe uint256."""
        if value < 0 or value > cls.UINT256_MAX:
            raise OverflowError(f"Value {value} out of uint256 range")
        return value


class SafeMathContract:
    """
    Example smart contract using SafeMath operations.
    """
    
    def __init__(self):
        """Initialize the contract."""
        self.balances: Dict[str, int] = {}
        self.total_supply = 0
        
    def transfer(self, from_address: str, to_address: str, amount: int) -> bool:
        """
        Safe transfer of tokens between addresses.
        
        Args:
            from_address: Sender address
            to_address: Recipient address
            amount: Amount to transfer
            
        Returns:
            True if transfer was successful
        """
        try:
            # Check balances
            if from_address not in self.balances:
                return False
                
            # Safe subtraction
            new_from_balance = SafeMath.sub(
                self.balances[from_address], 
                amount,
                max_value=SafeMath.UINT256_MAX
            )
            
            # Safe addition
            new_to_balance = SafeMath.add(
                self.balances.get(to_address, 0),
                amount,
                max_value=SafeMath.UINT256_MAX
            )
            
            # Update balances
            self.balances[from_address] = new_from_balance
            self.balances[to_address] = new_to_balance
            
            return True
            
        except OverflowError:
            return False
    
    def mint(self, address: str, amount: int) -> bool:
        """
        Safe minting of new tokens.
        
        Args:
            address: Address to mint to
            amount: Amount to mint
            
        Returns:
            True if minting was successful
        """
        try:
            # Safe addition for balance
            new_balance = SafeMath.add(
                self.balances.get(address, 0),
                amount,
                max_value=SafeMath.UINT256_MAX
            )
            
            # Safe addition for total supply
            new_total = SafeMath.add(
                self.total_supply,
                amount,
                max_value=SafeMath.UINT256_MAX
            )
            
            self.balances[address] = new_balance
            self.total_supply = new_total
            
            return True
            
        except OverflowError:
            return False


# Example usage
if __name__ == "__main__":
    # Test SafeMath operations
    print("Testing SafeMath operations:")
    
    # Safe addition
    try:
        result = SafeMath.add(100, 200)
        print(f"100 + 200 = {result}")
    except OverflowError as e:
        print(f"Addition failed: {e}")
    
    # Safe subtraction
    try:
        result = SafeMath.sub(200, 100)
        print(f"200 - 100 = {result}")
    except OverflowError as e:
        print(f"Subtraction failed: {e}")
    
    # Safe multiplication
    try:
        result = SafeMath.mul(10, 20)
        print(f"10 * 20 = {result}")
    except OverflowError as e:
        print(f"Multiplication failed: {e}")
    
    # Safe division
    try:
        result = SafeMath.div(100, 5)
        print(f"100 / 5 = {result}")
    except (OverflowError, ZeroDivisionError) as e:
        print(f"Division failed: {e}")
    
    # Test overflow detection
    try:
        result = SafeMath.add(SafeMath.UINT256_MAX, 1)
    except OverflowError as e:
        print(f"Overflow detected: {e}")
    
    # Test contract usage
    contract = SafeMathContract()
    contract.mint("user1", 1000)
    contract.transfer("user1", "user2", 500)
    
    print(f"User1 balance: {contract.balances.get('user1', 0)}")
    print(f"User2 balance: {contract.balances.get('user2', 0)}")
    print(f"Total supply: {contract.total_supply}")
