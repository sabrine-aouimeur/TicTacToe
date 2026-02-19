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
    
    
    # agent.py
import pickle
from q_table import QTable
from policy import choose_action
from learning import update


class Agent:
    """
    Brain of the agent: 
    - gère epsilon, alpha, gamma
    - choisit les actions (policy)
    - apprend après chaque move (learning)
    - réduit epsilon
    - sauvegarde / charge Q-table
    """

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0):
        self.q_table = QTable()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    # Choisir action
    def act(self, state, valid_moves):
        return choose_action(self.q_table, state, valid_moves, self.epsilon)

    # Mettre à jour Q-table après move
    def learn(self, state, action, reward, next_state, valid_moves):
        update(self.q_table, state, action, reward, next_state, valid_moves, self.alpha, self.gamma)

    # Réduction de epsilon
    def decay_epsilon(self, decay_rate=0.995, min_epsilon=0.01):
        self.epsilon = max(min_epsilon, self.epsilon * decay_rate)

    # Sauvegarder Q-table
    def save_model(self, file_path="q_table.pkl"):
        with open(file_path, "wb") as f:
            pickle.dump(self.q_table, f)

    # Charger Q-table
    def load_model(self, file_path="q_table.pkl"):
        with open(file_path, "rb") as f:
            self.q_table = pickle.load(f)