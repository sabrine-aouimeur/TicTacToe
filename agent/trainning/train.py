import os
import sys
import random

# Ajouter le chemin racine au PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from environnement.game_env import BasicGame
from agent.implementation.agent import Agent  
from environnement.game_rules import GameRules

def train(episodes=50000):
    agent = Agent()
    game = BasicGame()

    model_path = "q_table.pkl"
    if os.path.exists(model_path):
        try:
            agent.load_model(model_path)
            print(f"Chargement du modèle existant... (Taille: {agent.q_table.size()})")
        except:
            print("Erreur lors du chargement, démarrage d'un nouveau modèle.")

    print(f"Démarrage de l'entraînement pour {episodes} épisodes...")

    for episode in range(episodes):
        state = game.reset()
        done = False
        
        # History to update Q-table at the end of the game
        # Each entry: (state, action, valid_moves_at_that_state)
        history = {1: [], -1: []}
        
        # Decide if this game is against a random opponent
        # 1: Agent vs Agent, 2: Agent vs Random, 3: Random vs Agent
        train_mode = random.choice([1, 1, 2, 3]) 

        while not done:
            player = game.current_player
            valid_moves = game.get_validMoves()
            
            # Choose action: Agent or Random
            if (train_mode == 2 and player == -1) or (train_mode == 3 and player == 1):
                action = random.choice(valid_moves)
            else:
                action = agent.act(state, valid_moves)
            
            # Record move
            history[player].append((state, action, valid_moves))
            
            # Step in environment
            next_state, _, done = game.step(action)
            state = next_state

        # Game over - Give rewards
        winner = GameRules.check_winner(game.board)
        
        for player in [1, -1]:
            if not history[player]:
                continue
                
            # Final reward based on outcome
            if winner == player:
                reward = 1.0
            elif winner == -player:
                reward = -1.0
            else:
                reward = 0.5 # Better reward for draw to encourage defense

            # Update the last move with the terminal reward
            last_state, last_action, _ = history[player][-1]
            agent.learn(last_state, last_action, reward, state, [], True)
            
            # Backpropagate rewards using the correct valid moves for each state
            for i in range(len(history[player]) - 2, -1, -1):
                s, a, _ = history[player][i]
                next_s, _, next_v = history[player][i+1] # next_v are valid moves at next_s
                
                # Update Q(s,a) using Q(next_s, next_a)
                # But since we want max_future_q, we use the valid moves at next_s
                agent.learn(s, a, 0.0, next_s, next_v, False)

        # Réduction epsilon
        agent.decay_epsilon(decay_rate=0.9999) # Slower decay for better convergence

        if episode % 5000 == 0:
            print(f"Episode {episode} | epsilon: {agent.epsilon:.4f} | Q-size: {agent.q_table.size()}")

    agent.save_model(model_path)
    print(f"Training terminé. Taille finale de la Q-table: {agent.q_table.size()}")

if __name__ == "__main__":
    train(50000)
