from hashlib import sha256
from time import time
import json


class Block:

    def __init__(self, **kwargs):
        """
        Create a new block for the Blockchain

        :param timestamp: Timestamp of the block, defaults to the time the block object is created
        :param data: Data to store in the block, defaults to an empty list
        :param prevHash: Hash of the previous block, defaults to None.  Should always be specefied except for the genesis block.
        """
        self.timestamp = kwargs.get('timestamp', time())
        self.data = kwargs.get('data', [])
        self.prevHash = kwargs.get('prevHash', None)
        self._hash = None
        self.nonce = 0

    @property
    def hash(self):
        """
        Return the (non-python) hash of the block

        :return: The bytes of the hash of this block
        """
        if self._hash is None:
            hashFun = sha256()
            hashFun.update(self.encode(self.prevHash))
            hashFun.update(self.encode(self.timestamp))
            hashFun.update(self.encode(self.data))
            hashFun.update(self.encode(self.nonce))
            self._hash = hashFun.hexdigest()
        return self._hash

    def rehash(self):
        """
        Mark this block to re-calculate the hash the next time it's grabbed.
        """

        self._hash = None

    @staticmethod
    def encode(val):
        """
        Generate a UTF-8 bytes object to represent any object

        :param val: Value to encode
        :return: UTF-8 encoded byte representation of val
        """
        return str(val).encode('utf-8')

    def mine(self, difficulty):
        """
        Mine this block until a valid hash is found, based on leading zeros

        Basically, it loops until our hash starts with
        the string 0...000 with length of <difficulty>.

        :param difficulty:  length of the leading zeros to mine for
        """

        while self.hash[:difficulty] != '0' * difficulty:
            # We increases our nonce so that we can get a whole different hash.
            self.nonce += 1
            # Update our new hash with the new nonce value.
            self.rehash()


class Blockchain:

    def __init__(self):
        """
        initialize the blockchain with an empty, unmined "genesis" block.
        """
        self.chain = [Block()]
        self.blockTime = 30000
        self.difficulty = 1

    def __iter__(self):
        for c in self.chain:
            yield c

    def __getitem__(self, item):
        return self.chain[item]

    def append(self, data, **kwargs):
        """
        Add a new block to the blockchain from a new piece of data and an optional timestamp.

        :param data: Data to add to the new block.
        :param timestamp: UTC timecode of the new block
        """

        # Since we are adding a new block, prevHash will be the hash of the old latest block
        block = Block(data=data, prevHash=self[-1].hash, timestamp=kwargs.get('timestamp', time()))
        block.mine(self.difficulty)

        # Since now prevHash has a value, we must reset the block's hash
        self.chain.append(block)

        if time() - self[-1].timestamp < self.blockTime:
            self.difficulty += 1
        else:
            self.difficulty -= 1

    def isValid(self):
        """
        Iterates over the pairs of sequential blocks to validate that their previous hashes are set correctly

        :return: `True` if Valid, `False` otherwise
        """

        for prevBlock, currentBlock in zip(self[:-1], self[1:]):

            # Check validation
            if prevBlock.hash != currentBlock.prevHash:
                return False

        return True

    def __repr__(self):
        return json.dumps(
            [{k: getattr(item, k) for k in ['data', 'timestamp', 'nonce', 'hash', 'prevHash']}
             for item in self],
            indent=4
        )


if __name__ == '__main__':
    chain = Blockchain()
    chain.append({"from": "John", "to": "Bob", "amount": 100})
    chain.append({"from": "bob", "to": "john", "amount": 50})

    print(chain)