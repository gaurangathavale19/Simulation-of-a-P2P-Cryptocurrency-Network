class Transaction:
    def __init__(self, sender_id, receiver_id, coins, transaction_type, timestamp):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.coins = coins
        self.timestamp = timestamp
        self.transaction_id = self.set_txn_id()
        self.transaction_type = transaction_type
        if(self.transaction_type == "payment"):
            self.transaction_message = "{} pays {} {} coins".format(sender_id, receiver_id, coins)
        elif(self.transaction_type == "mines"):
            self.transaction_message = "{} mines {} coins".format(receiver_id, coins)
        else:
            self.transaction_message = "{} init {} coins".format(receiver_id, coins)