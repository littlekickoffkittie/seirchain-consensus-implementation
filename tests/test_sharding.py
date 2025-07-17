import unittest
from sharding import get_triad_id

class TestSharding(unittest.TestCase):

    def test_get_triad_id(self):
        address1 = "0x1234567890abcdef"
        address2 = "0xfedcba0987654321"
        num_triads = 10

        triad_id1 = get_triad_id(address1, num_triads)
        triad_id2 = get_triad_id(address2, num_triads)

        self.assertIsInstance(triad_id1, int)
        self.assertIsInstance(triad_id2, int)
        self.assertGreaterEqual(triad_id1, 0)
        self.assertLess(triad_id1, num_triads)
        self.assertGreaterEqual(triad_id2, 0)
        self.assertLess(triad_id2, num_triads)

        # Test determinism
        self.assertEqual(get_triad_id(address1, num_triads), get_triad_id(address1, num_triads))

if __name__ == '__main__':
    unittest.main()
