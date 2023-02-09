import hashlib
class Block:
    def __init__(self, creator_id, creation_time, peer_balance, transaction_list, previous_block_hash):
        self.block_id = self.set_id()

        self.creator_id = creator_id
        self.creation_time = creation_time
        self.transaction_list = transaction_list
        self.previous_block_hash = previous_block_hash
        self.peer_balance = peer_balance

    def set_id(self):
        result = " ".join([txn.transaction_message for txn in self.transaction_list]) + " " + str(self.previous_block_hash)
        return hashlib.sha256(result.encode('utf-8')).hexdigest()
