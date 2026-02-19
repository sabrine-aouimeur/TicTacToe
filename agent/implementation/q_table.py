"""
Implements the Q-Table data structure for storing state-action values.
"""

import random


class QTable:

    def __init__(self):

        self._q_table = {}

    def get(self, state, action):
        """
        Retrieves the Q-value for a specific state-action pair.

        """
        return self._q_table.get((state, action), 0.0)

    def set(self, state, action, value):
        """
        Updates the Q-value for a specific state-action pair.

        """
        self._q_table[(state, action)] = value

    def max_q(self, state, valid_actions):
        """
        Finds the maximum Q-value achievable from the current state given a list of valid actions.
        """
        if not valid_actions:
            return 0.0
        
        return max(self.get(state, a) for a in valid_actions)

    def best_action(self, state, valid_actions):
        """
        Determines the best action to take in the current state (Greedy policy).
        If multiple actions have the same highest Q-value, one is chosen randomly.

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

    def size(self):
        """
        Returns the total number of state-action pairs stored in the table.
        """
        return len(self._q_table)
