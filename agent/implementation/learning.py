#  q-learning update rule only

# update:
# Q(s,a) = Q + alpha * (reward + gamma * maxQ(next_state) - Q)

# handle terminal state 

# function:
# q_update(q_table, state, action, reward, next_state, done, alpha, gamma)


def update(q_table, state, action, reward, next_state, valid_actions, done, alpha, gamma):
    """
    Update Q-value using Q-learning formula.
    """

    # Current Q value
    current_q = q_table.get(state, action)

    # Maximum future Q value
    if done:
        max_future_q = 0.0
    else:
        max_future_q = q_table.max_q(next_state, valid_actions)

    # Q-learning formula
    new_q = current_q + alpha * (reward + gamma * max_future_q - current_q)

    # Store updated value
    q_table.set(state, action, new_q)