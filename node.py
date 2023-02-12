import random
import numpy as np
from block import Block
from event import Event
from transaction import Transaction
import hashlib
from queue import Queue
from graphviz import Graph
class Node:
    # speed: slow = 0, fast = 1
    # computation_power: low = 0, high = 1
    def __init__(self, node_id, speed, computation_power, coins, hashing_power, block_inter_arrival_mean_time, transaction_inter_arrival_mean_time, simulator_global_time, next_mining_time):
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
        # self.blockchain_tree, self.candidate_blocks = self.initialize_blockchain()
        self.blockchain_tree = {}
        self.candidate_blocks = {}
        # self.longest_chain = {'block': self.genesis_block, 'length': 1}
        self.longest_chain = {}
        self.blocks = set()
        self.unverified_blocks = {}
        
        self.coins = coins
        self.neighbours=[]
        self.visited_transactions={}
        self.unverified_txn={}
        self.block_curr_mine_time=None
        # self.hashing_power=None
        self.transactions=None
        self.block_arrival_timing={}

     
    def generate_transaction(self, n, current_time,txn_mean_time):
        print(current_time)
        sender_id=self.node_id
        receiver_id = random.randint(0,n-1)
        while(sender_id == receiver_id):
            receiver_id = random.randint(0,n-1)
        
        coins = random.randint(1,self.coins)
        exp_time = np.random.exponential(txn_mean_time)
        print('Exp_time:', exp_time)
        generated_event_time = exp_time + current_time  #todo
        print('Transaction generation delta:', current_time)
        txn=Transaction(sender_id,receiver_id,coins,"payment",generated_event_time)
        event=Event(self,"TXN",txn,sender_id,receiver_id,generated_event_time)
        return event

    def calc_latency(self,neighbour,message_len):
        if(self.speed == 1 and neighbour['node'].speed==1):
            c = 100 * 10**6
        else:
            c = 5 * 10**6
       
        # m = len(message)

        # d from exponential dist with mean 96/c
        
        mean = 96 * 10**3 / c
        d = np.random.exponential(mean)

        p = neighbour['propagation_delay']
        latency=p+message_len/c+d

        # print('Latency from ' + str(sender_id) + ' to ' + str(receiver_id) + ':', latency)
        return round(latency,2)

    def get_transactions(self,current_time,txn):
        print('inside get_transaction')
        reciever_id=txn.receiver_id
        sender_id=txn.sender_id
        message_len=8192 
        for key,value in self.visited_transactions.items():
            if key==txn.transaction_id:
                return []
        txnid=txn.transaction_id
        self.visited_transactions[txnid]=1
        new_events_generated=[]
        self.unverified_txn[txnid]=txn
        for neighbour in self.neighbours:
            lat=self.calc_latency(neighbour,message_len)
            new_event_time=lat+current_time
            new_event=Event(self,"TXN",txn,sender_id,reciever_id,new_event_time)#todo
            new_events_generated.append(new_event)

        return new_events_generated



    
    def generate_block(self, simulator_global_time, event):
        print('INSIDE GENERATE_BLOCK')
        # print(s)
        if self.next_mining_time != event.event_start_time: # need to analyze this once
        # if self.next_mining_time != event.event_start_time: # need to analyze this once
            self.next_mining_time = simulator_global_time + np.random.exponential(self.block_inter_arrival_mean_time/self.hashing_power) # need to analyze this once
            return [Event(curr_node=self.node_id, type="BLK", event_data=None, sender_id=self.node_id, receiver_id="all", event_start_time=self.next_mining_time)]
            # return []
        events = []
        print(self.hashing_power)
        exp_time = np.random.exponential(self.block_inter_arrival_mean_time)
        print('Mining exp_time:', exp_time)
        print(simulator_global_time)
        self.next_mining_time = simulator_global_time + exp_time # need to analyze this once
        print('Next_mining_time:', self.next_mining_time)
        # print('above global_simulator_time:', simulator_global_time)
        # print('above next_mining time:', self.next_mining_time)
        # print('Transaction generation:', self.next_mining_time)
        valid_txns = []
        parent_block = self.longest_chain
        peer_balance = parent_block['block'].peer_balance
        print(peer_balance)
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
        block = Block(creator_id=self.node_id , creation_time=event.event_start_time, peer_balance=peer_balance, transaction_list=valid_txns, previous_block_hash=parent_block['block'].block_id) # need to understand creation_time=event.event_start_time
        block.peers_visited.append(self.node_id)
        events.append(Event(curr_node=self.node_id, type="BLK", event_data=None, sender_id=self.node_id, receiver_id="all", event_start_time=self.next_mining_time))
        self.blockchain_tree[block.block_id] = (block, parent_block['length']+1)
        self.longest_chain = {'block': block, 'length': parent_block['length']+1}
        self.block_arrival_timing[block.block_id] = simulator_global_time
        self.blocks.add(block.block_id)
        return self.broadcast_block(simulator_global_time, block, events)

    def receive_block(self, simulator_global_time, block):
        print('inside receive block')
        
        # Check if the block is seen earlier - to avoid loop
        if block.block_id in self.blocks:
            return []
        
        self.blocks.add(block.block_id)
        block.peers_visited.append(self.node_id)
        # print(block)

        previous_block_hash = block.previous_block_hash

        # print(previous_block_hash)
        # print(self.blockchain_tree.keys())

        # Check if the incoming block's previous_hash is present in the blockchain tree
        if previous_block_hash not in self.blockchain_tree.keys():
            # Add to list of unverified blocks
            self.unverified_blocks[block.block_id] = block
        else:
            # Check the validity of blocks, if verified, then: 
            if self.verify_block(block):
                #print('done with verify block')
                #print(block.peer_balance)
                # for txn in block.transaction_list:
                #     print(txn.sender_id, txn.coins)
                for transaction in block.transaction_list:
                    print(transaction.sender_id, transaction.receiver_id, transaction.coins)
                    print(block.peer_balance)
                    if(transaction.transaction_type == 'payment'):

                        block.peer_balance[transaction.sender_id] -= transaction.coins
                        block.peer_balance[transaction.receiver_id] += transaction.coins

                # if(len(block.transaction_list) > 1):
                #     quit()

                # Add it to the blockchain tree
                self.blockchain_tree[block.block_id] = (block, self.blockchain_tree[block.previous_block_hash][1] + 1)
                self.block_arrival_timing[block.block_id] = simulator_global_time
                # print(self.blockchain_tree)

                # Update longest chain
                if(self.longest_chain['length'] < self.blockchain_tree[block.block_id][1]):
                    self.longest_chain['block'] = block
                    self.longest_chain['length'] = self.blockchain_tree[block.block_id][1]

        unverified_block_flag = True
        # print(self.unverified_blocks)

        while(unverified_block_flag and len(self.unverified_blocks)!=0):
            # print(self.unverified_blocks)
            for unverified_block_id, unverified_block in self.unverified_blocks.items():
                if(unverified_block.previous_block_hash in self.blockchain_tree.keys()):
                    if self.verify_block(unverified_block):
                        self.blockchain_tree[unverified_block.block_id] = (unverified_block, self.blockchain_tree[unverified_block.previous_block_hash][1] + 1)
                        self.block_arrival_timing[unverified_block.block_id] = simulator_global_time
                        if(self.longest_chain['length'] < self.blockchain_tree[unverified_block.block_id][1]):
                            self.longest_chain['block'] = unverified_block
                            self.longest_chain['length'] = self.blockchain_tree[unverified_block.block_id][1]
                        del self.unverified_blocks[unverified_block_id]
                        unverified_block_flag = True
                        break

                unverified_block_flag = False
            #print('stuck')
        
        # Broadcast the blocks - to the node's peers
        return self.broadcast_block(simulator_global_time, block, event_list=[])

    def broadcast_block(self, simulator_global_time, block, event_list):
        print('inside broadcast:', simulator_global_time)
        for peer in self.neighbours:
            if peer['node'].node_id not in block.peers_visited:
                print(block.block_id, block.peers_visited)
                delay = peer['propagation_delay']
                bottleneck_bandwidth = peer['bottleneck_bandwidth']
                delay += (8*1000*len(block.transaction_list)/(bottleneck_bandwidth * 10**6)) # in seconds
                delay += np.random.exponential((96*1000)/(bottleneck_bandwidth * 10**6)) # d_ij in seconds
                event_list.append(Event(curr_node=peer['node'].node_id, type="BLK", event_data=block, sender_id=block.creator_id, receiver_id="all", event_start_time=simulator_global_time+delay))
        return event_list

    def verify_block(self, block):
        block_transactions = block.transaction_list
        previous_block = self.blockchain_tree[block.previous_block_hash][0]
        previous_peer_balance = previous_block.peer_balance

        # For each transaction in the block, check if the sender's balance >= transaction amount (Using the parent/prev block's peer_balance)
        for transaction in block_transactions:
            if(transaction.transaction_type == 'payment'):
                if(previous_peer_balance[transaction.sender_id] < transaction.coins):
                    return False
                else:
                    previous_peer_balance[transaction.sender_id] -= transaction.coins
                    previous_peer_balance[transaction.receiver_id] += transaction.coins
            else:
                previous_peer_balance[transaction.receiver_id] += transaction.coins
        
        # Check whether the peer_balance after applying transactions on previous_peer_balance is same as the one provided in the incoming block
        if block.peer_balance != previous_peer_balance:      
            return False
        
        # Remove the verified transactions from the unverified treansactions list
        for transaction in block_transactions:
            if transaction.transaction_id in self.unverified_txn.keys():
                del self.unverified_txn[transaction.transaction_id]
        
        # Since the block is verified, add the block to the blockchain tree and update the longest chain length
        # self.blockchain_tree[block.block_id] = (block, self.blockchain_tree[block.previous_block_hash][1] + 1)

        # Update the longest chain if new block added changes the longest chain length
        # if(self.longest_chain['length'] < self.blockchain_tree[block.block_id][1]):
        #     self.longest_chain['block'] = block
        #     self.longest_chain['length'] = self.blockchain_tree[block.block_id][1]

        return True

    def visualize(self):
        print("visualize")
        block_map={}
        id_to_count = {}
        node_counter=0
        hash_queue=Queue()
        hash_queue.put(0)
        g=Graph('parent',filename=str(self.node_id))
        node_counter = 0
        id_to_count = {}

        print(self.blockchain_tree)

        for block_id,(block,_) in self.blockchain_tree.items():
            previous_block_hash=block.previous_block_hash
            block_map.setdefault(previous_block_hash,{})[block_id]=block


        g.attr(rankdir='LR',splines='line')
        while not hash_queue.empty():
            size=hash_queue.qsize()
            t=Graph('child')
            
            for i in range(size):
                parent_hash = hash_queue.get()
                parent_hash_dict=block_map[parent_hash]
                for id,block in parent_hash_dict.items():
                    node_counter_str=str(node_counter)
                    t.node(node_counter_str)
                    id_to_count[id]=node_counter_str
                    if id in block_map:
                        hash_queue.put(id)
                    if parent_hash!=0:
                        hash_prev_block=block.previous_block_hash
                        g.edge(node_counter_str,id_to_count[hash_prev_block])
                    node_counter=node_counter+1
            g.subgraph(t)
        g.render('results/'+str(self.node_id),view=True) 
