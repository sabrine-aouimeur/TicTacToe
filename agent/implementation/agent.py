# Main agent brain controls everything


# - epsilon, alpha, gamma
# - choose action (call policy)
# - learn after each move
# - reduce epsilon over time
# - interact with game/env
# - update stats
# - save/load q-table

# func:
    # __init__
    # act(state, valid_moves)
    # learn(state, action, reward, next_state, done)
    # decay_epsilon()
    # save_model()
    # load_model()
