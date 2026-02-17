

class GameRules:
   
    def check_winner(board):
        # Rows and Columns 
        for i in range(3):
            # Check rows
            if board[i][0] + board[i][1] + board[i][2] == 3 or board[i][0] + board[i][1] + board[i][2] == -3:
                return board[i][0]
            # Check columns
            if board[0][i] + board[1][i] + board[2][i] == 3 or board[0][i] + board[1][i] + board[2][i] == -3:
                return board[0][i]
        
        # Diagonals
        if board[0][0] + board[1][1] + board[2][2] == 3 or board[0][0] + board[1][1] + board[2][2] == -3:
            return board[0][0]
        if board[0][2] + board[1][1] + board[2][0] == 3 or board[0][2] + board[1][1] + board[2][0] == -3:
            return board[0][2]
        
        return 0

 
    def is_draw(board): 
        # Is the board full
        for i in range(3): 
            for j in range(3):
                if board[i][j] == 0:
                    return False
        return True

 
    def is_over(board):
        if GameRules.check_winner(board) != 0:
            return True
        return GameRules.is_draw(board)

   
    def evaluate(board, player):
        # Reward for RL agent
        winner = GameRules.check_winner(board)
        if winner == player:
            return 1 # Win
        if winner == -player:
            return -1 # Loss
        return 0 # Draw/Not over

