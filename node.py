import random
from block import Block
from event import Event
class Node:
    # speed: slow = 0, fast = 1
    # computation_power: low = 0, high = 1
    def __init__(self, node_id, speed, computation_power, simulator_global_time, transaction_list, next_mining_time):
        self.node_id = node_id
        self.speed = speed
        self.computation_power = computation_power
        self.block_inter_arrival_mean_time = 

        # added for maintaining blockchain
        self.peer_balance = self.populate_peer_balance()
        self.next_mining_time = next_mining_time
        self.genesis_block = Block(creator_id=node_id, creation_time=simulator_global_time, transaction_list=transaction_list, previous_block_hash=0)
        self.blockchain_tree, self.candidate_blocks = self.initialize_blockchain()
        self.blocks = []
        self.unverified_blocks = {}
        pass
    
    def populate_peer_balance(self, transaction_list):
        peer_balance = {}
        for txn in transaction_list:
            peer_balance[txn.receiver_id] = txn.coins
        return peer_balance

    def initialize_blockchain(self):
        blockchain_tree = {}
        blockchain_tree[self.genesis_block.block_id] = (self.genesis_block, 1)
        return blockchain_tree, blockchain_tree # this will also be the candidate block
    
    def generate_block(self, simulator_global_time, event):
        if self.next_mining_time < event.event_start_time:
            return []
        events = []
        events.append(Event(self.curr_mining_time,"Block",self.id,"all",None,self.id))
        pass

    def receive_block(self, simulator_global_time, event):
        pass

    def broadcast_block(self, simulator_global_time, block, event_list):
        pass

    def verify(self, simulator_global_time, block):
        pass