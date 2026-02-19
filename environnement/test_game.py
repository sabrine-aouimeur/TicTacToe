import sys
import os

# Ensure the root directory is in sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from agent.implementation.agent import Agent
from environnement.game_env import BasicGame
from environnement.game_rules import GameRules


def display_board(board):
    symbols = {0: ".", 1: "X", -1: "O"}
    print("\n  0 1 2")
    for i, row in enumerate(board):
        print(f"{i} " + " ".join(symbols[cell] for cell in row))


def board_to_state(board):
    return tuple(tuple(row) for row in board)


def test():
    game = BasicGame()
    ai = Agent()

    try:
        ai.load_model()
        print("Model loaded successfully.")
    except:
        print("No previous model found. Starting fresh.")

    print("=== GAME START ===")
    display_board(game.board)

    # In BasicGame, current_player starts at 1 (X)
    # Player 1: Human (X)
    # Player -1: AI (O)

    last_ai_state = None
    last_ai_action = None

    while not GameRules.is_over(game.board):
        state = board_to_state(game.board)
        valid_moves = game.get_validMoves()

        print(f"\nPlayer {'1 (Human)' if game.current_player == 1 else '2 (AI)'} turn")

        # HUMAN (Player 1)
        if game.current_player == 1:
            while True:
                try:
                    m = input("Enter move (row col): ")
                    r, c = map(int, m.split())
                    action = (r, c)

                    if action in valid_moves:
                        break
                    else:
                        print("Invalid move. Try again.")
                except:
                    print("Wrong format. Example: 1 1")
            
            # Execute human move
            game.step(action)

        # AI (Player 2 / -1)
        else:
            action = ai.act(state, valid_moves)
            print(f"AI chose: {action}")
            
            # Save state and action for learning after the reward is known
            last_ai_state = state
            last_ai_action = action
            
            # Execute AI move
            game.step(action)
            
            # Immediate feedback learning (reward for the move itself)
            reward = GameRules.evaluate(game.board, -1)
            next_state = board_to_state(game.board)
            next_valid_moves = game.get_validMoves()
            done = GameRules.is_over(game.board)
            ai.learn(last_ai_state, last_ai_action, reward, next_state, next_valid_moves, done)

        display_board(game.board)

    # Final result
    winner = GameRules.check_winner(game.board)
    
    if winner == -1:
        print("\nAI Wins 🤖")
    elif winner == 1:
        print("\nHuman Wins 👤")
    else:
        print("\nDraw 🤝")

    # Final learning step with terminal reward
    final_reward = GameRules.evaluate(game.board, -1)
    if last_ai_state is not None:
        ai.learn(last_ai_state, last_ai_action, final_reward, board_to_state(game.board), [], True)

    ai.decay_epsilon()
    ai.save_model()

    print("Model saved.")
    print("=== GAME OVER ===")


if __name__ == "__main__":
    test()
