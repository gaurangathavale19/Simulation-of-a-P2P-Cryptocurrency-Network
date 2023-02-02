import argparse
import random
import numpy as np
from node import Node
# nodes = []


# def sim():
if __name__ == "__main__":
    # global nodes

    # Command line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('--n_peers', required=True, help='Enter number of nodes')
    parser.add_argument('--slow_nodes', required=True, help='Enter the percentage of slow nodes')
    parser.add_argument('--lowCPU_nodes', required=True, help='Enter the percentage of low CPU nodes')

    args = parser.parse_args()

    ##### Start 1 #####

    n = int(args.n_peers)
    z0 = int(args.slow_nodes)
    z1 = int(args.lowCPU_nodes)
    number_of_slow_nodes = int(n*z0/100)
    number_of_low_CPU_nodes = int(n*z1/100)

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

    for i in range(n):
        nodes.append(Node(i, speeds[i], computation_powers[i], random.randint(20,40)))

    for node in nodes:
        print(node.node_id, node.speed, node.computation_power, node.coins)

    ##### End 1 #####

    ##### Start 4 #####

    adj_matrix = [[0 for i in range(n)] for j in range(n)]

    for i in range(n-1):
        adj_matrix[i][i+1] = 1

    min1 = 3
    max1 = min(n-2, 7)

    for i in range(n):
        for j in range(i):
            adj_matrix[i][j] = adj_matrix[j][i]
        number_of_ones = random.randint(min1, max1)
        number_of_ones -= sum(adj_matrix[i])
        test = [1]*number_of_ones + [0]*(n-i-1-number_of_ones)
        random.shuffle(test)
        
        j=i+2
        k=0
        while(j<n):
            adj_matrix[i][j] = test[k]
            k += 1
            j += 1

    print(adj_matrix)

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
        d = np.random.exponential(mean, 1)[0]

        p = np.random.uniform(low=10, high=500)

        # latency
        latency=p+m/c+d

        print('Latency from ' + str(sender_id) + ' to ' + str(receiver_id) + ':', latency)
    
    for i in range(n-1):
        for j in range(i+1, n):
            if(adj_matrix[i][j] == 1):
                message = 'TxnID: ' + str(i) + ' pays ' + str(j) + ' 10 coins'
                send_message(message, i, j)
        
    ##### End 5 #####

    