from copy import deepcopy
import numpy as np

def tour_cost(state, adj_matrix):
    cost = 0
    for i in range(len(state)-1):
        cost += adj_matrix[state[i]][state[i+1]]
    
    return cost

def random_swap(state):
    copied_state = deepcopy(state)
    idx1, idx2 = np.random.choice(len(state), size=2, replace=False)
    copied_state[idx1], copied_state[idx2] = copied_state[idx2], copied_state[idx1]

    return copied_state

def simulated_annealing(initial_state, adj_matrix, initial_T = 1000):
    T = initial_T
    current_state = initial_state
    iters = 0

    while True:
        T *= 0.99
        if T < 10 ** -14:
            return current_state, iters
        
        random_successor = random_swap(current_state)
        deltaE = tour_cost(current_state, adj_matrix) - tour_cost(random_successor, adj_matrix)

        if deltaE > 0:
            current_state = random_successor
        elif deltaE <= 0:
            u = np.random.uniform()
            if u <= np.e ** (deltaE/T):
                current_state = random_successor

        iters += 1
