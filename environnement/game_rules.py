"""
Defines the rules for the game.
"""

class GameRules:

    def check_winner(board):
        for i in range(3):
            if abs(sum(board[i])) == 3:
                return board[i][0]
            
            col_sum = board[0][i] + board[1][i] + board[2][i]
            if abs(col_sum) == 3:
                return board[0][i]

        diag1_sum = board[0][0] + board[1][1] + board[2][2]
        if abs(diag1_sum) == 3:
            return board[0][0]

        diag2_sum = board[0][2] + board[1][1] + board[2][0]
        if abs(diag2_sum) == 3:
            return board[0][2]

        return 0

    def is_draw(board):
        for row in board:
            if 0 in row:
                return False
        return True

    def is_over(board):
        return GameRules.check_winner(board) != 0 or GameRules.is_draw(board)

    def evaluate(board, player):
        winner = GameRules.check_winner(board)
        if winner == player:
            return 1
        if winner == -player:
            return -1
        return 0
