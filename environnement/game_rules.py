
class GameRules:
   
    def check_winner(board):
        # Rows and Columns
        for i in range(3):
            if abs(sum(board[i])) == 3:
                return board[i][0]
            col_sum = board[0][i] + board[1][i] + board[2][i]
            if abs(col_sum) == 3:
                return board[0][i]

        # Diagonals
        d1 = board[0][0] + board[1][1] + board[2][2]
        d2 = board[0][2] + board[1][1] + board[2][0]
        
        if abs(d1) == 3 or abs(d2) == 3:
            return board[1][1]
            
        return 0

 
    def is_draw(board):
        # Is the board full
        for row in board:
            if 0 in row: return False
        return True

 
    def is_over(board):
        
        if GameRules.check_winner(board) != 0:
            return True
        return GameRules.is_draw(board)

   
    def evaluate(board, player):
        # Reward for RL agent
        winner = GameRules.check_winner(board)
        if winner == player: return 1
        if winner == -player: return -1
        return 0
