#  q-learning update rule only

# update:
# Q(s,a) = Q + alpha * (reward + gamma * maxQ(next_state) - Q)

# handle terminal state 

# function:
# q_update(q_table, state, action, reward, next_state, done, alpha, gamma)


def update(self, state, action, reward, next_state, valid_actions, alpha, gamma):
    """
    Update Q-value using Q-learning formula.
    """

    # Current Q value
    current_q = self.get(state, action)

    # Maximum future Q value
    max_future_q = self.max_q(next_state, valid_actions)

    # Q-learning formula
    new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)

    # Store updated value
    self.set(state, action, new_q)