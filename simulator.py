import argparse
import random
import numpy as np
import hashlib
from node import Node
import heapq
from event import Event
from block import Block
from transaction import Transaction
# nodes = []
latencies = []
global_queue=[]

def populate_peer_balance(transaction_list):
    peer_balance = {}
    for txn in transaction_list:
        peer_balance[txn.receiver_id] = txn.coins
    return peer_balance

def initialize_blockchain(genesis_block):
    blockchain_tree = {}
    blockchain_tree[genesis_block.block_id] = (genesis_block, 1)
    return blockchain_tree # this will also be the candidate block

# def sim():
if __name__ == "__main__":
    # global nodes

    # Command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_peers', required=True, help='Enter number of nodes')
    parser.add_argument('--slow_nodes', required=True, help='Enter the percentage of slow nodes')
    parser.add_argument('--lowCPU_nodes', required=True, help='Enter the percentage of low CPU nodes')
    parser.add_argument('--txn_mean_time', required=True, help='Enter interarrival mean time between transactions')
    parser.add_argument('--blk_mean_time', required=True, help='Enter interarrival mean time between blocks')
    parser.add_argument('--termination_time', required=True, help='Enter the termination time of the simulation')

    args = parser.parse_args()

    ##### Start 1 #####
    simulator_global_time = 0
    txn_mean_time = int(args.txn_mean_time)
    block_inter_arrival_mean_time = int(args.blk_mean_time)
    termination_time = int(args.termination_time)
    total_nodes = int(args.n_peers)
    z0 = int(args.slow_nodes)
    z1 = int(args.lowCPU_nodes)
    number_of_slow_nodes = int(total_nodes*z0/100)
    number_of_low_CPU_nodes = int(total_nodes*z1/100)
    latencies = [[0 for i in range(total_nodes)] for j in range(total_nodes)]

    print('Number of nodes:', total_nodes)

    print('Number of slow nodes:', number_of_slow_nodes)
    print('Number of low CPU nodes:', number_of_low_CPU_nodes)

    speeds = []
    computation_powers = []
    nodes = []

    speeds = [0]*number_of_slow_nodes + [1]*(total_nodes - number_of_slow_nodes)
    computation_powers = [0]*number_of_low_CPU_nodes + [1]*(total_nodes - number_of_low_CPU_nodes)

    
    random.shuffle(speeds)
    random.shuffle(computation_powers)

    

    # for node in nodes:
    #     print(node.node_id, node.speed, node.computation_power, node.coins)

    ##### End 1 #####

    ##### Start 2 #####


    ##### End 2 #####

    ##### Start 3 #####

    

    ##### End 3 #####


    ##### Start 4 #####

    mat = {}
    min1 = 4

    max1 = min(total_nodes-1, 8)

    for i in range(total_nodes):
        mat[i] = []

    for i in range(total_nodes):

        peers = random.randint(min1, max1)
        # print('Peers:', peers)
        if(len(mat[i]) >= peers):
            continue
        set1 = set()
        if(len(mat[i]) > 0):
            test = mat[i]
            for e in test:
                set1.add(e)
        while(len(set1) < peers):
            ans = False
            # for j in range(i+1, n):
            #     if(j not in set1):
            #         ans = False
            #         break
            if(ans == False):
                peer = random.randint(0, total_nodes-1)
                while(len(mat[peer]) == 8 or i==peer):
                    peer = random.randint(0, total_nodes-1)

            # if(ans == True):
            #     peer = random.randint(0,i)
            #     while(len(mat[peer]) == 8):
            #         peer = random.randint(0,i)
            # print('PEER:', peer)
            if(peer not in set1):
                set1.add(peer)
        # print(set1)
        # print(i)
        # print('Peer:',peer)
        mat[i] = list(set1)
        for ele in set1:
            # if(ele in mat.keys()):
            if(i not in mat[ele]):
                list1 = mat[ele]
                list1.append(i)
                mat[ele] = list1
            # else:
            #     mat[ele] = [i]
        
        # print(mat)
    print("wlrihwev")

    adj_matrix = [[0 for _ in range(total_nodes)] for _ in range(total_nodes)]

    for k,v in mat.items():
        if(len(v) < 4 or len(v) > 8):
            print(len(v))
        for index in v:
            adj_matrix[k][index] = 1
    # print(adj_matrix)
    for i in adj_matrix:
        print(i)

    ##### End 4 ####



    #start5b

    
    number_of_high_nodes=total_nodes-number_of_low_CPU_nodes
    low_hk=1/(number_of_low_CPU_nodes+10*(number_of_high_nodes))
    high_hk=10*low_hk

    hashing_power_list = []

    for i in range(total_nodes):
        if computation_powers[i]:
            hashing_power_list.append(high_hk)
        else:
            hashing_power_list.append(low_hk)

    initial_txns=[]
    for id in range(total_nodes):
        coins=random.randint(20,40)
        # nodes.append(Node(id, speeds[id], computation_powers[id], coins))
        next_mining_time = simulator_global_time + np.random.exponential(block_inter_arrival_mean_time/hashing_power_list[id])
        nodes.append(Node(node_id=id, speed=speeds[id], computation_power=computation_powers[id], coins=coins, hashing_power=hashing_power_list[id], block_inter_arrival_mean_time=block_inter_arrival_mean_time, transaction_inter_arrival_mean_time=txn_mean_time, simulator_global_time=simulator_global_time, next_mining_time=next_mining_time))
        # sender_id, receiver_id, coins, transaction_type, timestamp
        txn=Transaction("coinbase",id,coins,"init",0)
        initial_txns.append(txn)
    
    
    
    for id in range(total_nodes):
        nodes[id].genesis_block = Block(creator_id=nodes[id].node_id, creation_time=simulator_global_time, peer_balance=populate_peer_balance(initial_txns), transaction_list=initial_txns, previous_block_hash=0)
        nodes[id].blockchain_tree = nodes[i].candidate_blocks = initialize_blockchain(nodes[id].genesis_block)
        nodes[id].longest_chain = {'block': nodes[id].genesis_block, 'length': 1}
        # nodes[id].genesis_block = Block(id,0,initial_txns,0)
    
    #start 5a


    ## Initializing neighbours of each node
    latency_matrix=[[0 for i in range(total_nodes)] for i in range(total_nodes)]
    for i in range(0,total_nodes):
        neighbour_list=[]
        for j in range(0,total_nodes):
            if(adj_matrix[i][j]):
                peer_inf={}
                if(latency_matrix[j][i]==0):
                    peer_inf['propagation_delay']=(np.random.uniform(low=10, high=500))/1000  #todo
                    latency_matrix[i][j]=peer_inf['propagation_delay']
                else:
                    peer_inf['propagation_delay']=latency_matrix[j][i]
                peer_inf['node']=nodes[j]
                peer_inf['node_id']=j
                if nodes[i].speed==1 and nodes[j].speed==1:
                    peer_inf['bottleneck_bandwidth']=100
                else:
                    peer_inf['bottleneck_bandwidth']=5

                neighbour_list.append(peer_inf)
                    
        nodes[i].neighbours=neighbour_list
        # print(nodes[i].neighbours)
    #end 5a


    for id in range(total_nodes):
        new_event=nodes[id].generate_transaction(total_nodes, simulator_global_time, txn_mean_time)
        heapq.heappush(global_queue,new_event)
    
    for id in range(total_nodes):
        #todo interblock_arrival_time?
        # new_event=Event(nodes[id],"BLK",None,nodes[i],"all",simulator_global_time+d)
        new_event = Event(curr_node=nodes[id].node_id, type="BLK", event_data=None, sender_id=nodes[id].node_id, receiver_id="all", event_start_time=nodes[id].next_mining_time)
        heapq.heappush(global_queue, new_event)
    
    for i in global_queue:
        print(i.type, i.event_start_time)
    ##end 5c




    #start 6
    termination_time=100
    # heapq.heappush(global_queue,)
    while(simulator_global_time<termination_time):
        curr_event = heapq.heappop(global_queue)
        # print(curr_event.type)
        if curr_event.type == "BLK":
            # pass
            curr_node_id = curr_event.curr_node
            event_content = curr_event.event_data
            sender_id = curr_event.sender_id
            if curr_node_id == sender_id:
                events_generated = curr_node.generate_block(simulator_global_time, curr_event)
            else:
                events_generated = curr_node.receive_block(simulator_global_time, event_content)
            print("BLK:", simulator_global_time, curr_node_id, sender_id)
        else:
            curr_node = curr_event.curr_node
            curr_node_id = curr_node.node_id
            event_content = curr_event.event_data
            sender_id = curr_event.sender_id
            simulator_global_time = curr_event.event_start_time
            # print("TXN:", simulator_global_time, " ", curr_node_id, " ", event_content.transaction_message, " ", sender_id)
            events_generated = curr_node.get_transactions(simulator_global_time, event_content)

            if curr_node_id == sender_id:
                new_event = curr_node.generate_transaction(total_nodes, simulator_global_time, txn_mean_time)
                events_generated.append(new_event)

        for event in events_generated:
            heapq.heappush(global_queue,event)



            


            


        
        


    # end6

