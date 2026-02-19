import random
from agent.implementation.q_table import QTable


def choose_action(q_table, state, valid_actions, epsilon):
    """
    Selects an action using the Epsilon-Greedy strategy.

    - Exploration (probability epsilon): Choose a random valid action.
    - Exploitation (probability 1 - epsilon): Choose the greedy (best) action from the Q-Table.

    """
    if not valid_actions:
        return None

    # Exploration: random action
    if random.random() < epsilon:
        return random.choice(valid_actions)

    # Exploitation: best action from Q-table
    return q_table.best_action(state, valid_actions)