import argparse
import random
import numpy as np
import hashlib
from node import Node
import heapq
from event import Event
from block import Block
from transaction import Transaction
# from transaction import Transaction
# nodes = []
latencies = []
global_queue=[]


# def sim():
if __name__ == "__main__":
    # global nodes

    # Command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_peers', required=True, help='Enter number of nodes')
    parser.add_argument('--slow_nodes', required=True, help='Enter the percentage of slow nodes')
    parser.add_argument('--lowCPU_nodes', required=True, help='Enter the percentage of low CPU nodes')
    parser.add_argument('--txn_mean_time', required=True, help='Enter interarrival mean time  between txn')

    args = parser.parse_args()



    ##### Start 1 #####
    termination_time = 2000
    n = int(args.n_peers)
    z0 = int(args.slow_nodes)
    z1 = int(args.lowCPU_nodes)
    txn_mean_time=int(args.txn_mean_time)
    number_of_slow_nodes = int(n*z0/100)
    number_of_low_CPU_nodes = int(n*z1/100)
    latencies = [[0 for i in range(n)] for j in range(n)]

    print('Number of nodes:', n)
    print('Number of slow nodes:', number_of_slow_nodes)
    print('Number of low CPU nodes:', number_of_low_CPU_nodes)

    speeds = []
    computation_powers = []
    nodes = []

    for i in range(n):
        if(number_of_slow_nodes > 0):
            speeds.append(0)
            number_of_slow_nodes -= 1
        else:
            speeds.append(1)
        if(number_of_low_CPU_nodes > 0):
            computation_powers.append(0)
            number_of_low_CPU_nodes -= 1
        else:
            computation_powers.append(1)
    
    random.shuffle(speeds)
    random.shuffle(computation_powers)

    initial_txns=[]
    for id in range(n):
        coins=random.randint(20,40)
        nodes.append(Node(id, speeds[id], computation_powers[id], coins))
        # sender_id, receiver_id, coins, transaction_type, timestamp
        txn=Transaction("coinbase",id,coins,"init",0)
        initial_txns.append(txn)

    for id in range(n):
        nodes[id].genesis_block = Block(id,0,initial_txns,0)

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
    max1 = min(n-1, 8)

    for i in range(n):
        mat[i] = []

    for i in range(n):
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
                peer = random.randint(0, n-1)
                while(len(mat[peer]) == 8 or i==peer):
                    peer = random.randint(0, n-1)
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
    # print("wlrihwev")
    adj_matrix = [[0 for _ in range(n)] for _ in range(n)]
    for k,v in mat.items():
        if(len(v) < 4 or len(v) > 8):
            print(len(v))
        for index in v:
            adj_matrix[k][index] = 1
    # print(adj_matrix)
    # for i in adj_matrix:
    #     print(i)

    ##### End 4 ####


    #start 5a

    ## Initializing neighbours of each node
    latency_matrix=[[0 for i in range(n)] for i in range(n)]
    for i in range(0,n):
        neighbour_list=[]
        for j in range(0,n):
            if(adj_matrix[i][j]):
                peer_inf={}
                if(latency_matrix[j][i]==0):
                    peer_inf['propogation_delay']=(np.random.uniform(low=10, high=500))/1000  #todo
                    latency_matrix[i][j]=peer_inf['propogation_delay']
                else:
                    peer_inf['propogation_delay']=latency_matrix[j][i]
                peer_inf['node']=nodes[j]
                peer_inf['nodeid']=j
                if nodes[i].speed==1 and nodes[j].speed==1:
                    peer_inf['bottlenext_bandwidth']=100
                else:
                    peer_inf['bottlenext_bandwidth']=50

                neighbour_list.append(peer_inf)
                    
        nodes[i].neighbours=neighbour_list
        # print(nodes[i].neighbours)
    #end 5a


    #start5b

    
    number_of_high_nodes=n-number_of_low_CPU_nodes
    low_hk=1/(number_of_low_CPU_nodes+10*(number_of_high_nodes))
    high_hk=10*low_hk

    for i in range(n):
        if nodes[i].computation_power:
            nodes[i].hashing_power=high_hk
        else:
            nodes[i].hashing_power=low_hk


    #start5b

    #end5b


    #start 5c

    current_time=0

    ###initializing first txn

    

    for id in range(n):
        new_event=nodes[id].generate_transaction(n,current_time,txn_mean_time)
        heapq.heappush(global_queue,new_event)
    '''
    for id in range(n):
        #todo interblock_arrival_time?
        interblock_arrival_time=10
        d = np.random.exponential(interblock_arrival_time,1)
        nodes[id].block_curr_mine_time=d+current_time
        new_event=Event(nodes[i],"BLK",None,nodes[i],"all",current_time+d)
        heapq.heappush(global_queue,new_event)
    '''
    ##end 5c


    #start 6
    termination_time=100
    # heapq.heappush(global_queue,)
    while(current_time<termination_time):
        curr_event=heapq.heappop(global_queue)
        if curr_event.type=="BLK":
            pass
            # curr_node_id=curr_node.node_id
            # event_content=curr_event.content
            # sender_id=curr_event.sender_id
            # if curr_node== sender_id:
            #     events_generated=curr_node.create_block(current_time,curr_event)
            # else:
            #     events_generated=curr_node.recieve_block(current_time,event_content)
        else:
            curr_node=curr_event.curr_node
            curr_node_id=curr_node.node_id
            event_content=curr_event.event_data
            sender_id=curr_event.sender_id
            current_time=curr_event.event_start_time
            print(current_time," ",curr_node_id," ",event_content.transaction_message," ",sender_id)
            events_generated=curr_node.get_transactions(current_time,event_content)

            if curr_node_id == sender_id:
                new_event=curr_node.generate_transaction(n,current_time,txn_mean_time)
                events_generated.append(new_event)

        for event in events_generated:
            heapq.heappush(global_queue,event)



            


            


        
        


    # end6