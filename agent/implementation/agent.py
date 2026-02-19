"""
Main agent class for the Reinforcement Learning Tic-Tac-Toe agent.
Handles the Q-Learning process, model management, and action selection.
"""

import pickle
from typing import List, Tuple, Optional
from agent.implementation.q_table import QTable
from agent.implementation.policy import choose_action
from agent.implementation.learning import update


class Agent:
    """
    Reinforcement Learning Agent using Q-Learning.
    
    Attributes:
        q_table (QTable): The storage for Q-values.
        alpha (float): Learning rate (0.0 to 1.0).
        gamma (float): Discount factor (0.0 to 1.0).
        epsilon (float): Exploration rate (0.0 to 1.0).
    """

    def __init__(self, alpha: float = 0.1, gamma: float = 0.9, epsilon: float = 1.0):
        """
        Initializes the agent with learning parameters.

        Args:
            alpha (float): Learning rate. High value = fast learning.
            gamma (float): Discount factor. Importance of future rewards.
            epsilon (float): Exploration rate. High value = more random moves.
        """
        self.q_table = QTable()
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def act(self, state: Tuple, valid_moves: List[Tuple[int, int]]) -> Optional[Tuple[int, int]]:
        """
        Decides the next action based on the current state and epsilon-greedy policy.

        Args:
            state: The current representation of the game board.
            valid_moves: A list of legal moves (row, col).

        Returns:
            The selected move (row, col) or None if no moves available.
        """
        return choose_action(self.q_table, state, valid_moves, self.epsilon)

    def learn(self, state: Tuple, action: Tuple[int, int], reward: float, 
              next_state: Tuple, valid_moves: List[Tuple[int, int]], done: bool) -> None:
        """
        Updates the Q-Table based on the result of the action taken.

        Args:
            state: The state before the action.
            action: The action taken.
            reward: The immediate reward received.
            next_state: The new state after the action.
            valid_moves: Valid moves available in the next state.
            done: Whether the game has ended.
        """
        update(self.q_table, state, action, reward, next_state, valid_moves, done, self.alpha, self.gamma)

    def decay_epsilon(self, decay_rate: float = 0.999, min_epsilon: float = 0.01) -> None:
        """
        Reduces the exploration rate (epsilon) over time to favor exploitation.

        Args:
            decay_rate: The factor by which epsilon is multiplied.
            min_epsilon: The minimum allowed value for epsilon.
        """
        self.epsilon = max(min_epsilon, self.epsilon * decay_rate)

    def save_model(self, file_path: str = "q_table.pkl") -> None:
        """
        Saves the Q-Table to a binary pickle file.
        """
        with open(file_path, "wb") as f:
            pickle.dump(self.q_table, f)

    def load_model(self, file_path: str = "q_table.pkl") -> None:
        """
        Loads the Q-Table from a binary pickle file.
        """
        with open(file_path, "rb") as f:
            self.q_table = pickle.load(f)