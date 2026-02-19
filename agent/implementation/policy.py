"""
Implements the action selection policy (epsilon-greedy).
"""

import random
from typing import Tuple, List, Optional
from agent.implementation.q_table import QTable


def choose_action(q_table: QTable, state: Tuple, valid_actions: List[Tuple[int, int]], epsilon: float) -> Optional[Tuple[int, int]]:
    """
    Selects an action using the Epsilon-Greedy strategy.

    - Exploration (probability epsilon): Choose a random valid action.
    - Exploitation (probability 1 - epsilon): Choose the greedy (best) action from the Q-Table.

    Args:
        q_table (QTable): The agent's Q-table.
        state (Tuple): The current game state.
        valid_actions (List[Tuple[int, int]]): List of legal moves.
        epsilon (float): The probability of choosing a random action (0.0 to 1.0).

    Returns:
        A tuple (row, col) representing the chosen action, or None if no actions are available.
    """
    if not valid_actions:
        return None

    # Exploration: random action
    if random.random() < epsilon:
        return random.choice(valid_actions)

    # Exploitation: best action from Q-table
    return q_table.best_action(state, valid_actions)