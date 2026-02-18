import random
from q_table import best_action

def choose_action(q_table, state, valid_actions, epsilon):
    """
    Selects an action using the epsilon greedy strategy.
    
    - With probability epsilon: chooses a random valid action (exploration)
    - Otherwise: chooses the best action from the Q-table (exploitation)

    at first epsilon = 1 -> exploration then with training epsilon will decrease to 0 -> exploitation
    """
    if not valid_actions:
        return None

    # Exploration: random action
    if random.random() < epsilon:
        return random.choice(valid_actions)

    # Exploitation: best action from Q-table
    return q_table.best_action(state, valid_actions)
