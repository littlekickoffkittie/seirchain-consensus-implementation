import unittest
from secure_math import SafeMath

class TestSafeMath(unittest.TestCase):

    def setUp(self):
        self.safe_math = SafeMath()

    def test_add(self):
        self.assertEqual(self.safe_math.add(1, 2), 3)
        with self.assertRaises(ValueError):
            self.safe_math.add(2**256 - 1, 1)

    def test_sub(self):
        self.assertEqual(self.safe_math.sub(3, 1), 2)
        with self.assertRaises(ValueError):
            self.safe_math.sub(0, 1)

    def test_mul(self):
        self.assertEqual(self.safe_math.mul(2, 3), 6)
        with self.assertRaises(ValueError):
            self.safe_math.mul(2**255, 2)

if __name__ == '__main__':
    unittest.main()
