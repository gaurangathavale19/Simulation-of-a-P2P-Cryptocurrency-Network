import random
import numpy as np
from block import Block
from event import Event
from transaction import Transaction
class Node:
    # speed: slow = 0, fast = 1
    # computation_power: low = 0, high = 1
    def __init__(self, node_id, speed, computation_power, hashing_power, block_inter_arrival_mean_time, transaction_inter_arrival_mean_time, simulator_global_time, transaction_list, next_mining_time):
        self.node_id = node_id
        self.speed = speed
        self.computation_power = computation_power
        self.block_inter_arrival_mean_time = block_inter_arrival_mean_time
        self.transaction_inter_arrival_mean_time = transaction_inter_arrival_mean_time
        self.hashing_power = hashing_power

        #added for maintaing transactions
        self.unverfied_transactions = {}

        # added for maintaining blocks and blockchain
        self.next_mining_time = next_mining_time
        self.genesis_block = Block(creator_id=node_id, creation_time=simulator_global_time, peer_balance=self.populate_peer_balance(transaction_list), transaction_list=transaction_list, previous_block_hash=0)
        self.blockchain_tree, self.candidate_blocks = self.initialize_blockchain()
        self.longest_chain = {'block': self.genesis_block, 'length': 1}
        self.blocks = set()
        self.unverified_blocks = {}
        pass

    def initialize_blockchain(self):
        blockchain_tree = {}
        blockchain_tree[self.genesis_block.block_id] = (self.genesis_block, 1)
        return blockchain_tree, blockchain_tree # this will also be the candidate block

    def populate_peer_balance(self, transaction_list):
        peer_balance = {}
        for txn in transaction_list:
            peer_balance[txn.receiver_id] = txn.coins
        return peer_balance
    
    def generate_block(self, simulator_global_time, event):
        if self.next_mining_time < event.event_start_time: # need to analyze this once
            return []
        events = []

        self.next_mining_time = simulator_global_time + np.random.exponential(self.block_inter_arrival_mean_time/self.hashing_power) # need to analyze this once
        events.append(Event(curr_location=self.node_id, type="Block", event_start_time=self.next_mining_time,  sender_id=self.node_id, receiver_id="all", event_data=None))
        
        valid_txns = []
        parent_block = self.longest_chain['block']
        peer_balance = parent_block.peer_balance
        for txn_id, txn  in self.unverfied_transactions.items():
            if(txn.transaction_type=='payment'):
                if (peer_balance[txn.sender_id] >= txn.coins):
                    peer_balance[txn.sender_id] -= txn.coins
                    peer_balance[txn.receiver_id] += txn.coins
                    valid_txns.append(txn)
                    del self.unverfied_transactions[txn_id]
            else:
                peer_balance[txn.to_id] += txn.coins
                valid_txns.append(txn)
                del self.unverfied_transactions[txn_id]
            if len(valid_txns) == 999: # 1000th Transaction would be added as mining reward
                break
        valid_txns.append(Transaction(sender_id="coinbase", receiver_id=self.node_id, coins=50, transaction_type="mines", timestamp=simulator_global_time)) # mining reward is 50
        peer_balance[self.node_id] += 50
        block = Block(creator_id=self.node_id , creation_time=event.event_start_time, peer_balance=peer_balance, transaction_list=valid_txns, previous_block_hash=parent_block.block_id) # need to understand creation_time=event.event_start_time
        self.blockchain_tree[block.block_id] = (block, parent_block['length']+1)
        self.longest_chain = (block, parent_block['length']+1)
        self.blocks.add(block.block_id)
        return self.broadcast_block(simulator_global_time, block, events)

    def receive_block(self, block, simulator_global_time):
        if block.block_id in self.blocks:
            return []
        self.blocks.add(block.id)
        pass

    def broadcast_block(self, simulator_global_time, block, event_list):
        for peer in self.neighbours:
            delay = peer['propagation_delay']
            bottleneck_bandwidth = peer['bottleneck_bandwidth']
            delay += (8*1000*len(block.transaction_list)/bottleneck_bandwidth)*1000 #in milliseconds
            delay += np.random.exponential((96*1000)/bottleneck_bandwidth)*1000 # d_ij in milliseconds
            event_list.append(Event(curr_location=peer['node']['node_id'], type="Block", event_data=None, sender_id=block.creator_id, receiver_id="all", event_start_time=simulator_global_time+delay))
        return event_list

    def verify_block(self, simulator_global_time, block):
        pass