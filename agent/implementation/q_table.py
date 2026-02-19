"""
Implements the Q-Table data structure for storing state-action values.
"""

import random
from typing import Dict, Tuple, List, Optional


class QTable:
    """
    A simple Q-Table implementation using a Python dictionary.

    The keys are tuples of (state, action), and the values are the Q-values (floats).
    State is expected to be a tuple (frozen representation of the board).
    Action is expected to be a tuple (row, col).
    """

    def __init__(self):
        """Initializes an empty Q-Table."""
        self._q_table: Dict[Tuple, float] = {}

    def get(self, state: Tuple, action: Tuple[int, int]) -> float:
        """
        Retrieves the Q-value for a specific state-action pair.

        Args:
            state: The current state tuple.
            action: The action tuple (row, col).

        Returns:
            The stored Q-value, or 0.0 if the pair has never been visited.
        """
        return self._q_table.get((state, action), 0.0)

    def set(self, state: Tuple, action: Tuple[int, int], value: float) -> None:
        """
        Updates the Q-value for a specific state-action pair.

        Args:
            state: The state tuple.
            action: The action tuple.
            value: The new Q-value to store.
        """
        self._q_table[(state, action)] = value

    def max_q(self, state: Tuple, valid_actions: List[Tuple[int, int]]) -> float:
        """
        Finds the maximum Q-value achievable from the current state given a list of valid actions.

        Args:
            state: The current state.
            valid_actions: List of possible actions.

        Returns:
            The maximum Q-value found, or 0.0 if no actions are valid.
        """
        if not valid_actions:
            return 0.0
        
        return max(self.get(state, a) for a in valid_actions)

    def best_action(self, state: Tuple, valid_actions: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        Determines the best action to take in the current state (Greedy policy).
        If multiple actions have the same highest Q-value, one is chosen randomly.

        Args:
            state: The current state.
            valid_actions: List of valid actions.

        Returns:
            The best action (row, col), or None if no actions are valid.
        """
        if not valid_actions:
            return None
        
        # Get Q-values for all valid actions
        q_values = [self.get(state, a) for a in valid_actions]
        
        # Find the maximum value
        max_q_val = max(q_values)
        
        # Collect all actions that share this maximum value (to handle ties)
        best_actions = [a for a, q in zip(valid_actions, q_values) if q == max_q_val]
        
        # Return a random choice among the best options
        return random.choice(best_actions)

    def size(self) -> int:
        """
        Returns the total number of state-action pairs stored in the table.
        """
        return len(self._q_table)
