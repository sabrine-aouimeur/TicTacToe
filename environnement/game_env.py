class BasicGame:
    def __init__(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.current_player = 1
        self.moves_count = 0

    def step(self, action):
        r, c = action

        if not self.is_valid(r, c):
            return self.get_state(), -1, True  # punition si move invalide

        self.board[r][c] = self.current_player
        self.moves_count += 1

        # Check win
        if self.check_win(self.current_player):
            return self.get_state(), 1, True

        # Check draw
        if self.moves_count == 9:
            return self.get_state(), 0, True

        # Switch player
        self.switch_player()

        return self.get_state(), 0, False

    def switch_player(self):
        self.current_player *= -1

    def is_valid(self, r, c):
        return self.board[r][c] == 0

    def get_validMoves(self):
        return [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == 0]

    def get_state(self):
        return tuple(tuple(row) for row in self.board)

    def reset(self):
        self.board = [[0, 0, 0] for _ in range(3)]
        self.current_player = 1
        self.moves_count = 0
        return self.get_state()

    def check_win(self, player):
        # rows
        for row in self.board:
            if all(cell == player for cell in row):
                return True

        # columns
        for col in range(3):
            if all(self.board[row][col] == player for row in range(3)):
                return True

        # diagonals
        if all(self.board[i][i] == player for i in range(3)):
            return True
        if all(self.board[i][2-i] == player for i in range(3)):
            return True

        return False

