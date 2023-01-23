import logging
import math

logger = logging.getLogger(__name__)
logging.basicConfig(filename='debug.log', encoding='utf-8', level=logging.DEBUG)


class BucketRunner(object):
    """
    The bucket runner sets up the problem that we have, and then executes to
    find the answer.
    """

    actions = []
    small_to_big_actions = []
    big_to_small_actions = []

    def __init__(self, bucket_a_size: int, bucket_b_size: int, goal: int):
        self.big_bucket = Bucket(max(bucket_a_size, bucket_b_size))
        self.small_bucket = Bucket(min(bucket_a_size, bucket_b_size))
        self.goal = goal

        if self.goal > max(bucket_a_size, bucket_b_size):
            msg = 'Goal volume cannot be larger than the buckets'
            logger.error(msg)
            raise ValueError(msg)

        # In order to successfully transfer buckets, we need to make sure that
        # the greatest common divisor of the buckets also divides the goal.
        # Otherwise, we will only ever transfer multiples of that common
        # divisor and never reach the goal
        gcd_a_b = math.gcd(self.small_bucket.max_volume, self.big_bucket.max_volume)
        has_viable_solution = self.goal % gcd_a_b == 0
        if self.goal % gcd_a_b != 0:
            msg = 'These buckets will never be able to create the desired volume'
            logger.error(msg)
            raise ValueError(msg)

    def run(self):

        # Now that we believe that we _can_ successfully do these transfers,
        # what is the best way to do it?
        self.small_to_big()
        self.big_to_small()
        if len(self.small_to_big_actions) < len(self.big_to_small_actions):
            self.actions = self.small_to_big_actions.copy()
        else:
            self.actions = self.big_to_small_actions.copy()

    def reset(self):
        self.actions = []
        self.small_bucket.current_volume = 0
        self.big_bucket.current_volume = 0

    def small_to_big(self):
        """
        This is the inefficient algorithm given by the prompt

        Fill the small when it is empty,
        Dump the big when it is full,
        keep transferring small to big until you solve the problem.
        """

        self.reset()
        while self.big_bucket.current_volume != self.goal and \
                self.small_bucket.current_volume != self.goal:
            action = ''
            if len(self.small_to_big_actions) > 1000:
                msg = 'exceeded maximum tries'
                logger.error('DEVELOPER ERROR: ' + msg)
                raise Exception(msg)
            if self.small_bucket.is_empty():
                logger.debug("\tSmall bucket is empty. Filling to {} units".format(
                    self.small_bucket.max_volume))
                self.small_bucket.fill_from_lake()
                action = 'fill'
            elif self.big_bucket.is_full():
                logger.debug("\tBig bucket is full. Dumping")
                self.big_bucket.dump()
                action = 'dump'
            else:
                self.small_bucket.transfer_to_bucket(self.big_bucket)
                action = 'transfer'
            step = {'action': action, 'small': self.small_bucket.current_volume, 'large': self.big_bucket.current_volume}
            logger.debug(step)
            self.small_to_big_actions.append(step)
        logger.debug("Goal volume acquired in {} steps\n".format(len(self.small_to_big_actions)))


    def big_to_small(self):
        """
        This is the efficient algorithm given by the prompt

        Fill the big when it is empty,
        Dump the small when it is full,
        keep transferring big to small until you solve the problem.V
        """

        self.reset()
        action = ''
        while self.big_bucket.current_volume != self.goal and \
                self.small_bucket.current_volume != self.goal:
            if len(self.big_to_small_actions) > 100:
                msg = 'exceeded maximum tries'
                logger.error('DEVELOPER ERROR: ' + msg)
                raise Exception(msg)
            if self.big_bucket.is_empty():
                logger.debug("\tBig bucket is empty. Filling to {} units".format(
                    self.big_bucket.max_volume))
                self.big_bucket.fill_from_lake()
                action = 'fill'
            elif self.small_bucket.is_full():
                logger.debug("\tSmall bucket is full. Dumping")
                self.small_bucket.dump()
                action = 'dump'
            else:
                self.big_bucket.transfer_to_bucket(self.small_bucket)
                action = 'transfer'

            step = {'action': action, 'small': self.small_bucket.current_volume, 'large': self.big_bucket.current_volume}
            logger.debug(step)
            self.big_to_small_actions.append(step)

        logger.debug("Goal volume acquired in {} steps\n".format(len(self.big_to_small_actions)))


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
            logger.debug("\tthis bucket has more water than the other can receive")
            logger.debug("\ttransferring {} to the other bucket".format(can_transfer))
            other_bucket.current_volume = other_bucket.max_volume
            self.current_volume -= can_transfer
        else:
            # Otherwise we will transfer all the water from this bucket into
            # the other one
            logger.debug("\ttrasnferring {} to the other bucket".format(self.current_volume))
            other_bucket.current_volume += self.current_volume
            self.current_volume = 0

    def dump(self):
        # dump the water from this bucket into the lake
        self.current_volume = 0

    def is_full(self):
        return self.max_volume == self.current_volume

    def is_empty(self):
        return self.current_volume == 0
