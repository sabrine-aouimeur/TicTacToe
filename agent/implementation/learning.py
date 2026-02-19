"""
Q-Learning update rule implementation.
"""

from typing import Tuple, List
from agent.implementation.q_table import QTable


def update(q_table: QTable, state: Tuple, action: Tuple[int, int], reward: float, 
           next_state: Tuple, valid_actions: List[Tuple[int, int]], done: bool, 
           alpha: float, gamma: float) -> None:
    """
    Updates the Q-value for a given state-action pair using the Bellman equation.

    Formula:
        Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))

    Args:
        q_table (QTable): The agent's Q-table.
        state (Tuple): The previous state.
        action (Tuple[int, int]): The action taken.
        reward (float): The reward received.
        next_state (Tuple): The resulting state.
        valid_actions (List[Tuple[int, int]]): Valid actions in the next state.
        done (bool): Whether the episode has ended.
        alpha (float): Learning rate.
        gamma (float): Discount factor.
    """
    # Current Q-value
    current_q = q_table.get(state, action)

    # Maximum future Q-value (0 if terminal state)
    if done:
        max_future_q = 0.0
    else:
        max_future_q = q_table.max_q(next_state, valid_actions)

    # Calculate new Q-value
    new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)

    # Update the Q-table
    q_table.set(state, action, new_q)