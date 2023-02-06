import argparse
import random
import numpy as np
import hashlib
from node import Node
# from transaction import Transaction
# nodes = []
latencies = []


# def sim():
if __name__ == "__main__":
    # global nodes

    # Command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_peers', required=True, help='Enter number of nodes')
    parser.add_argument('--slow_nodes', required=True, help='Enter the percentage of slow nodes')
    parser.add_argument('--lowCPU_nodes', required=True, help='Enter the percentage of low CPU nodes')
    parser.add_argument('--termination_time', required=True, help='Enter the termination time of the simulation')

    args = parser.parse_args()

    ##### Start 1 #####
    Ttx = 30
    termination_time = args.termination_time
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

    for i in range(total_nodes):
        nodes.append(Node(i, speeds[i], computation_powers[i]))

    for node in nodes:
        print(node.node_id, node.speed, node.computation_power, node.coins)

    ##### End 1 #####

    ##### Start 2 #####

    def generate_transaction_id(transaction_message, transaction_arrival_time):
        transaction_id = hashlib.sha256((transaction_message + ' ' + str(transaction_arrival_time)).encode()).hexdigest()

    def generate_transaction(Ttx, total_nodes, sender_id, current_time):
        receiver_id = random.randint(0,total_nodes-1)
        while(sender_id == receiver_id):
            receiver_id = random.randint(0,total_nodes-1)

        
        coins = random.randint(1,nodes[sender_id].coins)
        transaction_message = str(sender_id) + ' pays ' + str(receiver_id) + ' ' + str(coins) + ' coins'
        transaction_arrival_time = np.random.exponential(Ttx) + current_time
        transaction_id = generate_transaction_id(transaction_message, transaction_arrival_time)


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
                while(len(mat[peer]) == 8):
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


    ##### End 4 #####

    ##### Start 5 #####
    def send_message(message, sender_id, receiver_id):
        if(nodes[sender_id].speed == 1 and nodes[receiver_id].speed == 1):
            c = 100 * 10**6
        else:
            c = 5 * 10**6
       
        m = len(message)

        # d from exponential dist with mean 96/c
        
        mean = 96 * 10**3 / c
        d = np.random.exponential(mean)

        p = np.random.uniform(low=10, high=500)

        # latency
        latency=p+m/c+d

        # print('Latency from ' + str(sender_id) + ' to ' + str(receiver_id) + ':', latency)
        return round(latency,2)
    

    for i in range(total_nodes-1):
        for j in range(i+1, total_nodes):

            if(adj_matrix[i][j] == 1):
                message = 'TxnID: ' + str(i) + ' pays ' + str(j) + ' 10 coins'
                latencies[i][j] = latencies[j][i] = send_message(message, i, j)

    for i in latencies:
        print(i)        
    ##### End 5 #####

