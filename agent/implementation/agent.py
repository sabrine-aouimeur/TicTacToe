import pickle
from agent.implementation.q_table import QTable
from agent.implementation.policy import choose_action
from agent.implementation.learning import update


class Agent:
  

    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0):
     
        self.q_table = QTable()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def act(self, state, valid_moves):
      
        return choose_action(self.q_table, state, valid_moves, self.epsilon)

    def learn(self, state, action, reward, 
              next_state, valid_moves, done):
       
        update(self.q_table, state, action, reward, next_state, valid_moves, done, self.alpha, self.gamma)

    def decay_epsilon(self, decay_rate=0.999, min_epsilon=0.01):
       
        self.epsilon = max(min_epsilon, self.epsilon * decay_rate)

    def save_model(self, file_path="q_table.pkl"):
        with open(file_path, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_model(self, file_path="q_table.pkl"):
        
        with open(file_path, "rb") as f:
            self.q_table = pickle.load(f)