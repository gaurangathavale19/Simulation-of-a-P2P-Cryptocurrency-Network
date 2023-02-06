import random
import hashlib
from event import Event
import numpy as np
from transaction import Transaction
from queue import Queue
from graphviz import Graph


class Node:
    # speed: slow = 0, fast = 1
    # computation_power: low = 0, high = 1
    def __init__(self, node_id, speed, computation_power, coins):
        self.node_id = node_id
        self.speed = speed
        self.computation_power = computation_power
        self.coins = coins
        self.neighbours=[]
        self.visited_transactions={}
        self.unverified_txn={}
        self.block_curr_mine_time=None
        self.hashing_power=None
        self.transactions=None

    

    def generate_transaction(self, n, current_time,txn_mean_time):
        sender_id=self.node_id
        receiver_id = random.randint(0,n-1)
        while(sender_id == receiver_id):
            receiver_id = random.randint(0,n-1)
        
        coins = random.randint(1,self.coins)
        generated_event_time = np.random.exponential(txn_mean_time) + current_time  #todo
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

        p = neighbour['propogation_delay']
        latency=p+message_len/c+d

        # print('Latency from ' + str(sender_id) + ' to ' + str(receiver_id) + ':', latency)
        return round(latency,2)

    def get_transactions(self,current_time,txn):
        
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


    def visualize(self):
        block_map={}
        id_to_count = {}
        node_counter=0

        for block_id,(block,_) in self.block_tree.items():
            prev_block_hash=block.prev_block_hash
            block_map.setdefault(prev_block_hash,{})[block_id]=block


        graph = Graph('block_parent', filename=str(self.node_id))
        graph.attr(rankdir='LR', splines='line')
        hash_queue=Queue()
        hash_queue.put(0)

        while not hash_queue.empty():
            queue_size=hash_queue.qsize()
            t=Graph('child')
            for i in range(queue_size):
                parent_hash=hash_queue.get()
                for child_id,block in block_map.get(parent_hash,{}).items():
                    t.node(str(node_counter))
                    node_counter_str=str(node_counter)
                    id_to_count[child_id]=node_counter_str
                    if not parent_hash:
                        graph.edge(node_counter_str,id_to_count[block.prev_block_hash])
                    node_counter=node_counter+1
                    if child_id in block_map:
                        hash_queue.put(child_id)

            graph.subgraph(t)

        graph.render('results/'+str(self.node_id),view=True)


            
            






    