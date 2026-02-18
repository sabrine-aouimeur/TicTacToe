import tkinter as tk
import math

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("900x600")
        self.root.configure(bg="#1c3e52")
       

        
        self.canvas = tk.Canvas(self.root, bg="#1c3e52", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.player_symbol = None
        self.who_starts = None
        self.board = [None] * 9
        self.current_turn = None
        self.current_screen = "menu"

      
        self.COLORS = {
            "bg": "#1c3e52",
            "box": "#2c5f78",
            "selected_box": "#3d7a99", # Lighter color when selected
            "lime": "#c2d94c",
            "orange": "#f28b30",
            "gray": "#5a5a5a",         # Color for disabled state
            "blue_faint": "#2a5d7b", 
            "grid": "#4a7a8c"
        }
        
        self.current_screen = "menu"
        self.canvas.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        self.draw()

    def clear_canvas(self):
        self.canvas.delete("all")

    def draw(self):
        self.clear_canvas()
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if self.current_screen == "menu":
            self.draw_menu(w, h)
        elif self.current_screen == "game":
            self.draw_game(w, h)
        elif self.current_screen == "playing":
            self.draw_playing(w, h)

    def draw_menu(self, w, h):

        faint_font = ("Segoe UI", int(h * 0.07), "bold")
        self.canvas.create_text(w * 0.45, h * 0.3, text="XO XO", fill=self.COLORS["blue_faint"], font=faint_font, anchor="center", angle=15)
        self.canvas.create_text(w * 0.65, h * 0.45, text="XO XO", fill=self.COLORS["blue_faint"], font=faint_font, anchor="center", angle=15)

      
        grid_step = min(w, h) * 0.12
       
        for i in range(1, 4):
            x = i * grid_step
            self.canvas.create_line(x, 0, x, grid_step * 2.5, fill=self.COLORS["grid"], width=2)
        for j in range(1, 3): 
            y = j * grid_step
            self.canvas.create_line(0, y, grid_step * 3.5, y, fill=self.COLORS["grid"], width=2)
        
       
        for i in range(0, 3): 
            x = w - (i * grid_step)
            self.canvas.create_line(x, h, x, h - grid_step * 2.5, fill=self.COLORS["grid"], width=2)
        for j in range(0, 2): 
            y = h - (j * grid_step)
            self.canvas.create_line(w, y, w - grid_step * 3.5, y, fill=self.COLORS["grid"], width=2)

      
        self.draw_x(w * 0.08, h * 0.12, size=w*0.035, color=self.COLORS["lime"], width=8, angle=10) 
   
        self.draw_o(w * 0.33, h * 0.28, size=w*0.025, color=self.COLORS["orange"], width=8)
     
        self.draw_x(w * 0.48, h * 0.25, size=w*0.02, color=self.COLORS["lime"], width=6, angle=20)

        self.draw_x(w * 0.58, h * 0.32, size=w*0.007, color=self.COLORS["blue_faint"], width=2, angle=-10)
      
        self.draw_o(w * 0.68, h * 0.25, size=w*0.03, color=self.COLORS["orange"], width=8)
      
        self.draw_x(w * 0.9, h * 0.65, size=w*0.03, color=self.COLORS["lime"], width=8, angle=15)
       
        self.draw_o(w * 0.7, h * 0.85, size=w*0.03, color=self.COLORS["orange"], width=8)


        box_w, box_h = w * 0.5, h * 0.18
        x1, y1 = (w - box_w)/2, (h - box_h)/2
        x2, y2 = x1 + box_w, y1 + box_h
        
        rect = self.draw_round_rect(x1, y1, x2, y2, r=12, fill=self.COLORS["box"])
        text_size = int(h * 0.09)
        text = self.canvas.create_text(w/2, h/2, text="Tic Tac Toe", fill="white", font=("Segoe UI", text_size, "bold"))
        
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: self.switch_to_game())
        self.canvas.tag_bind(text, "<Button-1>", lambda e: self.switch_to_game())
        
    def draw_game(self, w, h):
        # --- Section 1: Choose Symbol ---
        self.canvas.create_text(
            w/2, h*0.18,
            text="Choose your symbol",
            fill="white",
            font=("Segoe UI", int(h*0.06), "bold")
        )

        btn_w = w * 0.12
        btn_h = h * 0.18
        y_sym = h * 0.28
        y_sym_end = y_sym + btn_h

        # X Button
        x1_start = w * 0.35
        x1_end = x1_start + btn_w
        x_fill = self.COLORS["selected_box"] if self.player_symbol == "X" else self.COLORS["box"]
        x_btn = self.draw_round_rect(x1_start, y_sym, x1_end, y_sym_end, r=15, fill=x_fill)
        self.draw_x((x1_start + x1_end)/2, (y_sym + y_sym_end)/2, size=w*0.025, color=self.COLORS["lime"], width=8)

        # O Button
        x2_start = w * 0.53
        x2_end = x2_start + btn_w
        o_fill = self.COLORS["selected_box"] if self.player_symbol == "O" else self.COLORS["box"]
        o_btn = self.draw_round_rect(x2_start, y_sym, x2_end, y_sym_end, r=15, fill=o_fill)
        self.draw_o((x2_start + x2_end)/2, (y_sym + y_sym_end)/2, size=w*0.025, color=self.COLORS["orange"], width=8)

        self.canvas.tag_bind(x_btn, "<Button-1>", lambda e: self.choose_symbol("X"))
        self.canvas.tag_bind(o_btn, "<Button-1>", lambda e: self.choose_symbol("O"))

        # --- Section 2: Who Starts? ---
        self.canvas.create_text(
            w/2, h*0.55,
            text="Who starts?",
            fill="white",
            font=("Segoe UI", int(h*0.06), "bold")
        )

        starter_btn_w = w * 0.15
        starter_btn_h = h * 0.08
        y_start = h * 0.62
        y_start_end = y_start + starter_btn_h

        # "YOU" Button
        sy1_start = w * 0.33
        sy1_end = sy1_start + starter_btn_w
        sy_fill = self.COLORS["selected_box"] if self.who_starts == "Human" else self.COLORS["box"]
        sy_btn = self.draw_round_rect(sy1_start, y_start, sy1_end, y_start_end, r=10, fill=sy_fill)
        self.canvas.create_text((sy1_start + sy1_end)/2, (y_start + y_start_end)/2, text="YOU", fill="white", font=("Segoe UI", int(starter_btn_h*0.4), "bold"))

        # "AI" Button
        sa1_start = w * 0.52
        sa1_end = sa1_start + starter_btn_w
        sa_fill = self.COLORS["selected_box"] if self.who_starts == "Computer" else self.COLORS["box"]
        sa_btn = self.draw_round_rect(sa1_start, y_start, sa1_end, y_start_end, r=10, fill=sa_fill)
        self.canvas.create_text((sa1_start + sa1_end)/2, (y_start + y_start_end)/2, text="AI", fill="white", font=("Segoe UI", int(starter_btn_h*0.4), "bold"))

        self.canvas.tag_bind(sy_btn, "<Button-1>", lambda e: self.choose_starter("Human"))
        self.canvas.tag_bind(sa_btn, "<Button-1>", lambda e: self.choose_starter("Computer"))

        # --- Section 3: PLAY Button ---
        play_btn_w = w * 0.18
        play_btn_h = h * 0.09
        pb_x1 = (w - play_btn_w) / 2
        pb_y1 = h * 0.8
        pb_x2 = pb_x1 + play_btn_w
        pb_y2 = pb_y1 + play_btn_h

        is_active = (self.player_symbol is not None) and (self.who_starts is not None)
        play_color = self.COLORS["orange"] if is_active else self.COLORS["gray"]
        play_text_color = "white" if is_active else "#aaaaaa"

        play_rect = self.draw_round_rect(pb_x1, pb_y1, pb_x2, pb_y2, r=12, fill=play_color)
        play_text = self.canvas.create_text(w/2, (pb_y1 + pb_y2)/2, text="PLAY", fill=play_text_color, font=("Segoe UI", int(play_btn_h * 0.5), "bold"))
        
        if is_active:
            self.canvas.tag_bind(play_rect, "<Button-1>", lambda e: self.start_game())
            self.canvas.tag_bind(play_text, "<Button-1>", lambda e: self.start_game())

    def choose_starter(self, starter):
        self.who_starts = starter
        self.draw()

    def start_game(self):
        self.board = [None] * 9
        self.winner = None
        self.winning_line = None
        
        if self.who_starts == "Human":
            self.current_turn = self.player_symbol
        else:
            self.current_turn = "O" if self.player_symbol == "X" else "X"
            
        self.current_screen = "playing"
        self.draw()

    def draw_playing(self, w, h):
        # Header
        title = f"{self.winner} Wins!" if self.winner else "Tic Tac Toe"
        self.canvas.create_text(w/2, h*0.08, text=title, fill="white", font=("Segoe UI", int(h*0.06), "bold"))
        
        # Grid dimensions and centering
        grid_size = min(w, h) * 0.6
        x_start = (w - grid_size) / 2
        y_start = (h - grid_size) / 2
        cell_size = grid_size / 3
        
        # Draw stylized grid lines
        grid_color = self.COLORS["grid"]
        line_width = 5
        
        for i in range(1, 3):
            # Vertical lines
            lx = x_start + i * cell_size
            self.canvas.create_line(lx, y_start, lx, y_start + grid_size, fill=grid_color, width=line_width, capstyle="round")
            # Horizontal lines
            ly = y_start + i * cell_size
            self.canvas.create_line(x_start, ly, x_start + grid_size, ly, fill=grid_color, width=line_width, capstyle="round")
            
        # Draw board contents and click areas
        for idx in range(9):
            row, col = divmod(idx, 3)
            cx = x_start + col * cell_size + cell_size/2
            cy = y_start + row * cell_size + cell_size/2
            
            # Clickable area (only if no winner)
            if not self.winner:
                rect = self.canvas.create_rectangle(
                    x_start + col * cell_size, 
                    y_start + row * cell_size, 
                    x_start + (col+1) * cell_size, 
                    y_start + (row+1) * cell_size, 
                    fill="", outline="", width=0
                )
                self.canvas.tag_bind(rect, "<Button-1>", lambda e, i=idx: self.handle_click(i))

            # Draw symbol if present
            symbol = self.board[idx]
            if symbol == "X":
                self.draw_x(cx, cy, size=cell_size*0.3, color=self.COLORS["lime"], width=8)
            elif symbol == "O":
                self.draw_o(cx, cy, size=cell_size*0.3, color=self.COLORS["orange"], width=8)

        # Draw Winning Line
        if self.winning_line:
            idx1, idx2, idx3 = self.winning_line
            r1, c1 = divmod(idx1, 3)
            r3, c3 = divmod(idx3, 3)
            x1 = x_start + c1 * cell_size + cell_size/2
            y1 = y_start + r1 * cell_size + cell_size/2
            x3 = x_start + c3 * cell_size + cell_size/2
            y3 = y_start + r3 * cell_size + cell_size/2
            
            self.canvas.create_line(x1, y1, x3, y3, fill="white", width=10, capstyle="round")

    
    def handle_click(self, idx):
        if self.board[idx] is None and not self.winner:
            self.board[idx] = self.current_turn
            
            # Check for winner
            winner, line = self.check_winner()
            if winner:
                self.winner = winner
                self.winning_line = line
            else:
                # Toggle turn
                self.current_turn = "O" if self.current_turn == "X" else "X"
            
            self.draw()

    def check_winner(self):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols
            (0, 4, 8), (2, 4, 6)             # Diags
        ]
        for combo in wins:
            a, b, c = combo
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a], combo
        return None, None


    def switch_to_game(self):
        self.current_screen = "game"
        self.draw()

    def switch_to_menu(self):
        self.current_screen = "menu"
        self.draw()

    def draw_x(self, x, y, size, color, width=4, angle=0):
        # Calculate rotated endpoints for two lines forming an X
        rad = math.radians(angle)
        rad45 = math.radians(45)
        
        for a in [rad45, -rad45]:
            x1 = x + size * math.cos(rad + a)
            y1 = y + size * math.sin(rad + a)
            x2 = x + size * math.cos(rad + a + math.pi)
            y2 = y + size * math.sin(rad + a + math.pi)
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=width)

    def draw_o(self, x, y, size, color, width=4):
        self.canvas.create_oval(x-size, y-size, x+size, y+size, outline=color, width=width)

    def draw_round_rect(self, x1, y1, x2, y2, r=10, **kwargs):
        points = [x1+r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y2-r, x2, y2, x2-r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y1+r, x1, y1]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)


    def choose_symbol(self, symbol):
      self.player_symbol = symbol
      self.draw()

if __name__ == "__main__":
    
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
