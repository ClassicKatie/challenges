import unittest

from src.bucket import BucketRunner

class Base(unittest.TestCase):
    def test_standard_case(self):
        runner = BucketRunner(3, 5, 4)

    def test_big_to_small(self):
        runner = BucketRunner(3, 5, 4)
        runner.run()
        self.assertEqual(len(runner.actions), 6, 'got right number of actions')

    def test_small_to_big(self):
        runner = BucketRunner(1, 10, 2)
        runner.run()
        self.assertEqual(len(runner.actions), 4, 'got right number of actions')

    def test_goal_too_big(self):
        with self.assertRaises(ValueError):
            BucketRunner(1, 10, 20)

    def test_buckets_bad_mod(self):
        with self.assertRaises(ValueError):
            BucketRunner(2, 10, 3)

