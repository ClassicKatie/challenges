import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class BucketRunner(object):
    """
    The bucket runner sets up the problem that we have, and then executes to
    find the answer.

    """
    iterations = 0

    def __init__(self, bucket_a_size: int, bucket_b_size: int, goal: int):
        self.big_bucket = Bucket(max(bucket_a_size, bucket_b_size))
        print("Created big bucket size {}".format(self.big_bucket.max_volume))
        self.small_bucket = Bucket(min(bucket_a_size, bucket_b_size))
        print("Created small bucket size {}".format(self.small_bucket.max_volume))
        self.goal = goal

    def execute_suboptimal(self):
        """
        This is the inefficient algorithm given by the prompt

        Fill the small when it is empty,
        Dump the big when it is full,
        keep transferring small to big until you solve the problem.
        """

        print("Buckets are sized {} and {}. Goal is {}".format(
            self.big_bucket.max_volume, self.small_bucket.max_volume,
            self.goal))

        while self.big_bucket.current_volume != self.goal and \
                self.small_bucket.current_volume != self.goal:
            if self.iterations > 1000:
                raise Exception("yikes! I think something went wrong")
            if self.small_bucket.is_empty():
                print("\tSmall bucket is empty. Filling to {} units".format(
                    self.small_bucket.max_volume))
                self.small_bucket.fill_from_lake()
            if self.big_bucket.is_full():
                print("\tBig bucket is full. Dumping")
                self.big_bucket.dump()
            self.small_bucket.transfer_to_bucket(self.big_bucket)
            self.iterations += 1
            print("Big bucket: {}, small bucket: {}".format(
                self.big_bucket.current_volume,
                self.small_bucket.current_volume))
        print("Goal volume acquired in {} steps".format(self.iterations))


    def execute_optimal(self):
        """
        This is the efficient algorithm given by the prompt

        Fill the big when it is empty,
        Dump the small when it is full,
        keep transferring big to small until you solve the problem.V
        """

        print("Buckets are sized {} and {}. Goal is {}".format(
            self.big_bucket.max_volume, self.small_bucket.max_volume,
            self.goal))

        while self.big_bucket.current_volume != self.goal and \
                self.small_bucket.current_volume != self.goal:
            if self.iterations > 10000:
                raise Exception("yikes! I think something went wrong")
            if self.big_bucket.is_empty():
                print("\tBig bucket is empty. Filling to {} units".format(
                    self.big_bucket.max_volume))
                self.big_bucket.fill_from_lake()
            if self.small_bucket.is_full():
                print("\tSmall bucket is full. Dumping")
                self.small_bucket.dump()
            self.big_bucket.transfer_to_bucket(self.small_bucket)
            self.iterations += 1
            print("Big bucket: {}, small bucket: {}".format(
                self.big_bucket.current_volume,
                self.small_bucket.current_volume))

        print("Goal volume acquired in {} steps".format(self.iterations))


class Bucket(object):
    max_valume = 0
    current_volume = 0

    def __init__(self, size: int):
        """
        A bucket has two kinds of attributes: static attributes that are
        inherent to the object (such as the size of the bucket) and dynamic
        attributes, such as how much water is currently in the bucket. We set
        the former when initializing the object

        """
        if size > 99:
            raise ValueError("maximum bucket size is 99")
        self.max_volume = size

    def fill_from_lake(self):
        self.current_volume = self.max_volume
        return self.current_volume

    def transfer_to_bucket(self, other_bucket):
        can_transfer = other_bucket.max_volume - other_bucket.current_volume
        if self.current_volume > can_transfer:
            # If this bucket has more water in it than the other bucket,
            # then the other bucket can only fill to the top, and some
            # water will remain in this bucket
            print("\tthis bucket has more water than the other can receive")
            print("\ttransferring {} to the other bucket".format(can_transfer))
            other_bucket.current_volume = other_bucket.max_volume
            self.current_volume -= can_transfer
        else:
            # Otherwise we will transfer all the water from this bucket into
            # the other one
            print("\ttrasnferring {} to the other bucket".format(self.current_volume))
            other_bucket.current_volume += self.current_volume
            self.current_volume = 0

    def fill_from_bucket(self, other_bucket):
        can_take = self.max_volume - self.current_volume
        if other_bucket.current_volume > can_take:
            # If the other bucket has more water in it than
            # this bucket, then this bucket can only fill to the top
            # and we will leave some water in the other bucket
            print("\tbig bucket has more water than small bucket can receive")
            print("\ttransferring {} to the small bucket".format(can_take))
            self.current_volume = self.max_volume
            other_bucket.current_volume -= can_take
        else:
            # Otherwise, we will dump all the water from the other bucket into
            # this one
            print("\tbig bucket can transfer all its water to small bucket")
            self.current_volume += other_bucket.current_volume
            other_bucket.current_volume = 0
            self.current_volume += other_bucket.current_volume

    def dump(self):
        # dump the water from this bucket into the lake
        self.current_volume = 0

    def is_full(self):
        return self.max_volume == self.current_volume

    def is_empty(self):
        return self.current_volume == 0


if __name__ == '__main__':
    BucketRunner(3, 5, 4).execute_optimal()
    BucketRunner(3, 5, 4).execute_suboptimal()
