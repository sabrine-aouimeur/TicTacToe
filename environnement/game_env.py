


class BasicGame:
    def __init__(self):

        # 0: empty, 1: X, -1: O

        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.choose_yoursign("X") 
        self.moves_count = 0

    #the player can choose in the start if he takes O or X
    def choose_yoursign(self, sign):
        if sign == "X":
            self.current_player = 1
        elif sign == "O":
            self.current_player = -1
        else:
            print("Invalid sign ")
            self.current_player = 1 # Default is X

    def step(self, action):
        r, c = action
     
        if not self.is_valid(r, c):
            print(f"Invalid move ({r},{c}) Try again")
            return self.get_state(), self.current_player
            
        self.board[r][c] = self.current_player
        self.moves_count += 1
        
        moved_player = self.current_player 
        self.switch_player() # Next turn
        
        return self.get_state(), moved_player

    def switch_player(self):
        self.current_player *= -1

    def is_valid(self, r, c):
        #  cell is empty
        if self.board[r][c] != 0:
            return False
        return True

    def get_validMoves(self):
        # Find all zeros to get valid moves 
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]

    def get_state(self):  
        # Return a copy
        return [row[:] for row in self.board]

    def reset(self):
        self.board = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.choose_yoursign("X")
        self.moves_count = 0
        return self.get_state()


    def show(self):
        # Simple print board
        symbols = {0: '.', 1: 'X', -1: 'O'}
        print("\nBoard:")
        for row in self.board:
            print(" ".join([symbols[cell] for cell in row]))

# adding fuctions for modes and for who start first
