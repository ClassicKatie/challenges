# Water Buckets

Water Buckets is an api that solves the Water Pouring Problem for given bucket sizes and a goal.

## Installation

```bash
git clone <FIXME>
pip install -r requirements.txt
```

## Usage

The bucket transfer api has a single call that can be accessed either locally via http or the cli.

### local http server
To start the http server:

```python
hug -f src/api.py
```

In the browser, go to [http://localhost:8000/get_bucket_transfer_steps]() with uri parameters for `bucket_a_size`, `bucket_b_size`, and `goal` where the bucket sizes are the sizes of the irregular containers and the goal is the desired volume amount. All three inputs should be integers less than 100.

Example:
```
http://localhost:8000/get_bucket_transfer_steps?bucket_a_size=5&bucket_b_size=3&goal=4
```

### cli
To see the available commands in the cli:

```bash
hug -f src/api.py -c help
```

To run the call in the command line:

```bash
hug -f src/api.py -c get_bucket_transfer_steps 5 3  4
```

The positional arguments are the size of the first bucket; size of the second bucket; goal volume
