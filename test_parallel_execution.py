import unittest
import time
from parallel_execution import execute_parallel

class TestParallelExecution(unittest.TestCase):

    def test_execute_parallel(self):
        transactions = [(1, 0.1), (2, 0.1), (3, 0.1)]
        start_time = time.time()
        results = execute_parallel(transactions)
        end_time = time.time()

        # The total time should be less than the sum of individual times
        self.assertLess(end_time - start_time, 0.3)
        self.assertEqual(sorted(results), [2, 4, 6])

if __name__ == '__main__':
    unittest.main()
