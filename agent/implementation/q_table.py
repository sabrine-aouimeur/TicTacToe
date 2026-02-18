import random

class QTable:
    def __init__(self):

        # Initialize empty Q-table using a dictionary

        self._q_table = {}

    def get(self, state, action):

        # Return Q-value for (state, action). Returns 0.0 if not found

        return self._q_table.get((state, action), 0.0)

    def set(self, state, action, value):

        # Store or update Q-value for (state, action)

        self._q_table[(state, action)] = value

    def max_q(self, state, valid_actions):

        # Return the maximum Q-value among given valid actions
        
        if not valid_actions:
            return 0.0
        
        return max(self.get(state, a) for a in valid_actions)

    def best_action(self, state, valid_actions):

        # Return the action with the highest Q-value
        
        if not valid_actions:
            return None
        
        # Get Q-values for all valid actions
        q_values = [self.get(state, a) for a in valid_actions]
        max_q_val = max(q_values)
        
        # Filter actions that share the same maximum Q-value
        best_actions = [a for a, q in zip(valid_actions, q_values) if q == max_q_val]
        
        # Return any one of the best actions (handles ties and unvisited states)
        return random.choice(best_actions)

    def size(self):

        # Return number of stored (state, action) entries
        
        return len(self._q_table)
