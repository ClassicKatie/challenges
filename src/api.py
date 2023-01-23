""" Water Buckets API"""
import json

import hug

from bucket import BucketRunner

@hug.cli()
@hug.get(examples='bucket_a_size=3&bucket_b_size=5&goal=4')
@hug.local()
def get_bucket_transfer_steps(bucket_a_size, bucket_b_size, goal):
    """
    Gets the actions necessary to use the available buckets to get to the goal
    volume
    """
    runner = None
    try:
        runner = BucketRunner(int(bucket_a_size), int(bucket_b_size), int(goal))
        runner.run()
        return {
            'actions': runner.actions,
            'num_actions': len(runner.actions),
            }
    except Exception as err:
        return {'error': err}

if __name__ == '__main__':
    get_bucket_transfer_steps.interface.cli()
