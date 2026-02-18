#  q-learning update rule only

# update:
# Q(s,a) = Q + alpha * (reward + gamma * maxQ(next_state) - Q)

# handle terminal state 

# function:
# q_update(q_table, state, action, reward, next_state, done, alpha, gamma)
