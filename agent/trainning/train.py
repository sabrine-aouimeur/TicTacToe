
"""
Main training loop for the Reinforcement Learning agent.
"""

import os
import sys
import random
import csv

# Add root path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from environnement.game_env import BasicGame
from agent.implementation.agent import Agent
from environnement.game_rules import GameRules
from agent.implementation.stats import Stats

def train(episodes=50000):
    """
    Trains the agent using Self-Play.

    Args:
        episodes (int): Number of games to play.
    """
    agent = Agent()
    game = BasicGame()
    stats = Stats()

    model_path = "q_table.pkl"
    if os.path.exists(model_path):
        try:
            agent.load_model(model_path)
            print(f"Loaded existing model (Size: {agent.q_table.size()})")
        except:
            print("Error loading model, starting fresh.")

    print(f"Starting training for {episodes} episodes...")

    for episode in range(episodes):
        state = game.reset()
        done = False
        
        # History to update Q-table at the end of the game
        # Each entry: (state, action, valid_moves_at_that_state)
        history = {1: [], -1: []}
        
        while not done:
            player = game.current_player
            valid_moves = game.get_validMoves()
            
            # Choose action
            action = agent.act(state, valid_moves)
            
            # Record move
            history[player].append((state, action, valid_moves))
            
            # Step in environment
            next_state, _, done = game.step(action)
            state = next_state

        # Game over - Give rewards
        winner = GameRules.check_winner(game.board)
        
        if winner == 1:
            stats.record_win()
            stats.add_reward(1)
        elif winner == -1:
            stats.record_loss()
            stats.add_reward(-1)
        else:
            stats.record_draw()
            stats.add_reward(0)

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
            
            # Backpropagate rewards
            # We iterate backwards through the history to update previous states
            for i in range(len(history[player]) - 2, -1, -1):
                s, a, _ = history[player][i]
                next_s, _, next_v = history[player][i+1] # next_v are valid moves at next_s
                
                # Update Q(s,a) using Q(next_s, next_a)
                agent.learn(s, a, 0.0, next_s, next_v, False)

        # Decay epsilon
        agent.decay_epsilon(decay_rate=0.9999) 

        if episode % 5000 == 0:
            print(f"Episode {episode} | epsilon: {agent.epsilon:.4f} | Q-size: {agent.q_table.size()} | Win Rate: {stats.get_win_rate():.2f}")

    agent.save_model(model_path)
    print(f"Training finished. Final Q-table size: {agent.q_table.size()}")
    
    # Save Stats to CSV
    save_stats(stats)


def save_stats(stats):
    """
    Saves training statistics to a CSV file.
    """
    filename = "training_stats.csv"
    file_exists = os.path.isfile(filename)
    
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Total Games", "Wins", "Losses", "Draws", "Win Rate"])
        
        writer.writerow([stats.total_games, stats.wins, stats.losses, stats.draws, f"{stats.get_win_rate():.2f}"])
    
    print(f"Stats saved to {filename}")

if __name__ == "__main__":
    train(50000)
