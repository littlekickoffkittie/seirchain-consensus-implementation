import unittest
from gas import calculate_gas

class TestGas(unittest.TestCase):

    def test_calculate_gas(self):
        opcodes1 = ["PUSH", "PUSH", "ADD", "STORE"]
        self.assertEqual(calculate_gas(opcodes1), 12)

        opcodes2 = ["LOAD", "PUSH", "MUL", "STOP"]
        self.assertEqual(calculate_gas(opcodes2), 10)

        opcodes3 = ["UNKNOWN", "ADD"]
        self.assertEqual(calculate_gas(opcodes3), 4)

        opcodes4 = []
        self.assertEqual(calculate_gas(opcodes4), 0)

if __name__ == '__main__':
    unittest.main()
