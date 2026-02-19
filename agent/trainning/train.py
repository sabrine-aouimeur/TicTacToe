# trainning/train.py

# 👇 Imports corrigés pour ta structure
from environnement.game_env import BasicGame
from agent.implementation.agent import Agent  # attention à l'orthographe du dossier "implemntation"
from agent.implementation.policy import choose_action
from agent.implementation.learning import update

def train(episodes=10000):
    agent = Agent()
    game = BasicGame()

    for episode in range(episodes):

        state = game.reset()
        done = False

        while not done:
            valid_moves = game.get_validMoves()
            action = agent.act(state, valid_moves)

            # Appliquer action
            next_state, moved_player = game.step(action)

            # ---- Calcul reward & done ----
            if game.check_win(moved_player):
                reward = 1 if moved_player == 1 else -1
                done = True
            elif game.moves_count == 9:
                reward = 0
                done = True
            else:
                reward = 0
                done = False

            next_valid_moves = game.get_validMoves()

            # Apprentissage
            agent.learn(state, action, reward, next_state, next_valid_moves)
            state = next_state

        # Réduction epsilon
        agent.decay_epsilon()

        if episode % 1000 == 0:
            print(f"Episode {episode} | epsilon: {agent.epsilon:.4f}")

    agent.save_model()
    print("Training terminé ✅")

if __name__ == "__main__":
    # Toujours exécuter depuis le dossier racine TicTacToe
    # python -m trainning.train
    train(20000)
