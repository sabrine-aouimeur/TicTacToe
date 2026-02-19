"""
Tracks learning progress and statistics for the agent.
Useful for debugging and visualizing improvement over time.
"""

class Stats:
    """
    Tracks win/loss/draw records and average rewards.
    """
    
    def __init__(self):
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.total_games = 0
        self.total_reward = 0.0

    def record_win(self):
        """Records a win"""
        self.wins += 1
        self.total_games += 1

    def record_loss(self):
        """Records a loss"""
        self.losses += 1
        self.total_games += 1

    def record_draw(self):
        """Records a draw"""
        self.draws += 1
        self.total_games += 1

    def add_reward(self, reward):
        """Adds to the cumulative reward"""
        self.total_reward += reward

    def get_win_rate(self):
        """Returns the current win rate """
        if self.total_games == 0:
            return 0.0
        return self.wins / self.total_games

    def reset(self):
        """Resets all statistics"""
        self.wins = 0
        self.losses = 0
        self.draws = 0
        self.total_games = 0
        self.total_reward = 0.0