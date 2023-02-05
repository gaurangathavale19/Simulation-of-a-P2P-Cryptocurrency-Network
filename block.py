import hashlib
class Block:
    def __init__(self, creator_id, creation_time, transaction_list, previous_block_hash):
        self.block_id = self.set_id()
        self.creator_id = creator_id
        self.creation_time = creation_time
        self.transaction_list = transaction_list
        self.previous_block_hash = previous_block_hash
        self.peer_balance = self.populate_peer_balance(transaction_list)

    def set_id(self):
        result = " ".join(self.transaction_list) + " " + str(self.previous_block_hash)
        return hashlib.sha256(result.encode('utf-8')).hexdigest()

    def populate_peer_balance(self, transaction_list):
        peer_balance = {}
        for txn in transaction_list:
            peer_balance[txn.receiver_id] = txn.coins
        return peer_balance