import unittest

from src.bucket import Bucket


class Base(unittest.TestCase):

    def test_initial_state(self):
        new_bucket = Bucket(4)
        self.assertEqual(new_bucket.max_volume, 4,
                         'bucket created with correct maximum volume')
        self.assertEqual(new_bucket.current_volume, 0, 'bucket created empty')

    def test_bucket_fill(self):
        bucket = Bucket(5)
        bucket.fill_from_lake()

        self.assertEqual(bucket.current_volume, 5,
                         'bucket filled to maximum value')
        self.assertTrue(bucket.is_full(), 'bucket registers as full')
        self.assertFalse(bucket.is_empty(),
                         'bucket does not register as false')

    def test_bucket_dump(self):
        bucket = Bucket(5)
        bucket.current_volume = 4
        bucket.dump()

        self.assertEqual(bucket.current_volume, 0,
                         'bucket dumped all its water')
        self.assertTrue(bucket.is_empty(), 'bucket registers as empty')
        self.assertFalse(bucket.is_full(), 'bucket does not register as full')

    def test_bucket_transfer_s_to_b(self):
        bucket_a = Bucket(3)
        bucket_b = Bucket(5)

        # full small bucket to empty large bucket should
        bucket_a.fill_from_lake()  # bucket has 3 units
        bucket_a.transfer_to_bucket(bucket_b)

        self.assertEqual(bucket_a.current_volume, 0,
                         'transferred all water out of small bucket')
        self.assertEqual(bucket_b.current_volume, 3,
                         'bucket b received all water')
        self.assertFalse(bucket_b.is_full(), 'big bucket is not full')
        self.assertFalse(bucket_b.is_empty(), 'big bucket is not empty')

    def test_bucket_transfer_b_to_s(self):
        bucket_a = Bucket(3)
        bucket_b = Bucket(5)

        bucket_b.fill_from_lake()
        bucket_b.transfer_to_bucket(bucket_a)

        self.assertEqual(bucket_a.current_volume, 3, 'small bucket filled up')
        self.assertEqual(bucket_b.current_volume, 2,
                         'big bucket has 2 units remaining')
        self.assertFalse(bucket_b.is_full(), 'big bucket is not full')
        self.assertFalse(bucket_b.is_empty(), 'big bucket is not empty')


if __name__ == '__main__':
    unittest.main()
