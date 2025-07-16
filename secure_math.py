"""
A secure math library for smart contracts that checks for integer overflow and underflow errors.
"""

MAX_UINT256 = 2**256 - 1

class SafeMath:
    """
    A library for performing safe integer arithmetic operations.
    """

    def add(self, a, b):
        """
        Adds two numbers, checking for overflow.
        """
        c = a + b
        if c > MAX_UINT256:
            raise ValueError("Integer overflow")
        return c

    def sub(self, a, b):
        """
        Subtracts two numbers, checking for underflow.
        """
        if a < b:
            raise ValueError("Integer underflow")
        return a - b

    def mul(self, a, b):
        """
        Multiplies two numbers, checking for overflow.
        """
        if a == 0 or b == 0:
            return 0
        c = a * b
        if c > MAX_UINT256:
            raise ValueError("Integer overflow")
        return c
