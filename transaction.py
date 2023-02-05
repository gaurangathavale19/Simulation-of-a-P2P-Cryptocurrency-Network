# from simulator import *

class Transaction:
    def __init__(self, transaction_message, sender_id, receiver_id, coins, transaction_type):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.coins = coins
        self.transaction_id = 1
        self.transaction_type = transaction_type
        if(self.transaction_type == "payment"):
            self.transaction_message = "{} pays {} {} coins".format(sender_id, receiver_id, coins)
        elif(self.transaction_type == "mines"):
            self.transaction_message = "{} mines 50 coins".format(sender_id)
        else:
            self.transaction_message = "{} {} {}".format(sender_id)
        

    # sim()

    # def check_balance_of_sender(message, nodes):


    