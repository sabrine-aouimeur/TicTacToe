import os
import sys

# Ajouter le chemin racine au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from environnement.game_env import BasicGame
from agent.implementation.agent import Agent  

def train(episodes=20000):
    agent = Agent()
    game = BasicGame()

    print(f"Démarrage de l'entraînement pour {episodes} épisodes...")

    for episode in range(episodes):
        state = game.reset()
        done = False

        while not done:
            valid_moves = game.get_validMoves()
            action = agent.act(state, valid_moves)

            # Appliquer action
            # Rappel game_env.py: return self.get_state(), reward, done
            next_state, reward, done = game.step(action)

            # Apprentissage
            next_valid_moves = game.get_validMoves()
            agent.learn(state, action, reward, next_state, next_valid_moves, done)
            
            state = next_state

        # Réduction epsilon
        agent.decay_epsilon()

        if episode % 2000 == 0:
            print(f"Episode {episode} | epsilon: {agent.epsilon:.4f}")

    agent.save_model("q_table.pkl")
    print("Training termine")

if __name__ == "__main__":
    train(20000)
