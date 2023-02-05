import random
class Node:
    # speed: slow = 0, fast = 1
    # computation_power: low = 0, high = 1
    def __init__(self, node_id, speed, computation_power):
        self.node_id = node_id
        self.speed = speed
        self.computation_power = computation_power
        self.coins = random.randint(20,40)