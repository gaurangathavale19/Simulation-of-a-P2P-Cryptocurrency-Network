# Simulation-of-a-P2P-Cryptocurrency-Network

## How to compile and run the code ?
- Install the libraries from the file requirements.txt using the command: `pip install -r requirements.txt`
- Run the code with the following command-line arguments:
  - <b>n_peers</b>: Number of peers
  - <b>slow_nodes</b>: Percetage of slow nodes/peers
  - <b>lowCPU_nodes</b>: Percentage of low CPU nodes/peers
  - <b>txn_mean_time</b>: Mean interarrival time between transactions
  - <b>blk_mean_time</b>: Mean interarrival time between blocks
  - <b>terminations_time</b>: The time after which the simulation will come to an halt
 - Command to run: 
   `python simulator.py --n_peers <n_peers> --slow_nodes <slow_nodes> --lowCPU_nodes <lowCPU_nodes> --txn_mean_time <txn_mean_time> --blk_mean_time <blk_mean_time> --termination_time <termination_time>`
 - For instance: `python simulator.py --n_peers 15 --slow_nodes 30 --lowCPU_nodes 10 --txn_mean_time 1 --blk_mean_time 5 --termination_time 1000`
    
## Output
- Network topology graph
- Each node will output the following:
  - Blockchain tree
  - Blocks in its blockchain tree along with block arrival time, number of transactions in that block and the balances of the nodes after the block is added to the blockchain tree
  - Transations in its blockchain tree along with transaction arrival time, transaction type, sender, receiver and amount(in BTC)
  - Events in the simulator along with event type, event start time, sender and receiver
