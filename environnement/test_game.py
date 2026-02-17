
from game_env import BasicGame
from game_rules import GameRules

def test():
    game = BasicGame()
    print(" testing ")
    game.show()
    
    # predefined moves for testing
    # moves = [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)]
    
    # here i made 2 mode predefined moves and manual moves
    while not GameRules.is_over(game.board):

        print(f"\n Player {game.current_player} turn")
        m = input("Enter move : row col (ex -> 1 1 )  ")
        
        # Convert  string to  tuple (x, y)
        r, c = map(int, m.split())
        state, p = game.step((r, c))
        game.show()
         
    
    winner = GameRules.check_winner(game.board)
    if winner != 0:
        print(f"\n Game Over!!!!!!!!!!!!!!!!!!! \n Winner: {winner} congratsssssssss ")
    else:
        print("\n Game Over! no winner ;[")

if __name__ == "__main__":
    test()
