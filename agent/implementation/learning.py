from agent.implementation.q_table import QTable


def update(q_table, state, action, reward, next_state, valid_actions, done, alpha, gamma):
    """
    Updates the Q-value for a given state-action pair using the Bellman equation.

    Formula:
        Q(s, a) = Q(s, a) + alpha * (reward + gamma * max(Q(s', a')) - Q(s, a))

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