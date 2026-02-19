import tkinter as tk
import math
import sys
import os

# Ensure the root directory is in sys.path so we can import 'agent' and 'environnement'
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if root_dir not in sys.path:
    sys.path.append(root_dir)

from agent.implementation.agent import Agent
from environnement.game_env import BasicGame

class TicTacToeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("900x600")
        self.root.configure(bg="#150025")
       

        
        self.canvas = tk.Canvas(self.root, bg="#150025", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.player_symbol = None
        self.who_starts = None
        self.board = [None] * 9
        self.current_turn = None
        self.current_screen = "menu"

      
        self.COLORS = {
            "bg": "#150025",
            "box": "#2D0048",
            "selected_box": "#590099", # Lighter/Neon color when selected
            "lime": "#FF007F",         # Neon Pink
            "orange": "#00F0FF",       # Neon Cyan
            "gray": "#5a5a5a",         # Color for disabled state
            "blue_faint": "#2D0048",   # Subtle purple for BG text
            "grid": "#590099"          # Electric Purple
        }
        
        self.current_screen = "menu"
        self.canvas.bind("<Configure>", self.on_resize)

        # Timer and Pause State
        self.elapsed_time = 0
        self.is_paused = False
        self.timer_id = None

        self.game_env = BasicGame()
        # Initialiser avec epsilon=0 pour que l'IA utilise ses connaissances (Genius mode)
        # Si epsilon=1, elle joue totalement au hasard.
        self.ai_agent = Agent(epsilon=0.0)

        # Utilisation du chemin absolu pour trouver le modèle
        model_path = os.path.join(root_dir, "q_table.pkl")
        try:
          self.ai_agent.load_model(model_path)
          print(f"Model loaded: {model_path}")
        except:
          print(f"No saved model found at {model_path}")

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
        elif self.current_screen == "game_over":
            self.draw_game_over(w, h)

    def draw_menu(self, w, h):

        faint_font = ("Arial Rounded MT Bold", int(h * 0.07), "bold")
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
        text = self.canvas.create_text(w/2, h/2, text="Tic Tac Toe", fill="white", font=("Arial Rounded MT Bold", text_size, "bold"))
        
        self.canvas.tag_bind(rect, "<Button-1>", lambda e: self.switch_to_game())
        self.canvas.tag_bind(text, "<Button-1>", lambda e: self.switch_to_game())
        
    def draw_game(self, w, h):
        # --- Section 1: Choose Symbol ---
        self.canvas.create_text(
            w/2, h*0.3,
            text="Choose your symbol",
            fill="white",
            font=("Arial Rounded MT Bold", int(h*0.06), "bold")
        )

        btn_w = w * 0.12
        btn_h = h * 0.18
        y_sym = h * 0.4
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

        # --- Section 2: PLAY Button ---
        play_btn_w = w * 0.18
        play_btn_h = h * 0.09
        pb_x1 = (w - play_btn_w) / 2
        pb_y1 = h * 0.75
        pb_x2 = pb_x1 + play_btn_w
        pb_y2 = pb_y1 + play_btn_h

        is_active = self.player_symbol is not None
        play_color = self.COLORS["orange"] if is_active else self.COLORS["gray"]
        play_text_color = "white" if is_active else "#aaaaaa"

        play_rect = self.draw_round_rect(pb_x1, pb_y1, pb_x2, pb_y2, r=12, fill=play_color)
        play_text = self.canvas.create_text(w/2, (pb_y1 + pb_y2)/2, text="PLAY", fill=play_text_color, font=("Arial Rounded MT Bold", int(play_btn_h * 0.5), "bold"))
        
        if is_active:
            self.canvas.tag_bind(play_rect, "<Button-1>", lambda e: self.start_game())
            self.canvas.tag_bind(play_text, "<Button-1>", lambda e: self.start_game())

    def choose_starter(self, starter):
        # Method kept for compatibility if needed, but no longer used in UI
        self.who_starts = starter
        self.draw()

    def switch_to_game(self):
        self.current_screen = "game"
        self.draw()

    def switch_to_menu(self):
        self.current_screen = "menu"
        self.draw()

    def draw_playing(self, w, h):
        pass
        
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

        # --- Timer Display ---
        time_str = self.format_time(self.elapsed_time)
        self.canvas.create_text(
            w * 0.1, h * 0.08,
            text=f"Time: {time_str}",
            fill="white",
            font=("Arial Rounded MT Bold", int(h * 0.04), "bold"),
            anchor="w"
        )

        # --- Pause Button ---
        if not self.winner:
            pause_text = "RESUME" if self.is_paused else "PAUSE"
            btn_color = self.COLORS["orange"] if self.is_paused else self.COLORS["grid"]
            p_w, p_h = w * 0.12, h * 0.06
            px1 = w * 0.88 - p_w
            py1 = h * 0.05
            p_rect = self.draw_round_rect(px1, py1, px1 + p_w, py1 + p_h, r=10, fill=btn_color)
            p_lbl = self.canvas.create_text(px1 + p_w/2, py1 + p_h/2, text=pause_text, fill="white", font=("Arial Rounded MT Bold", int(p_h*0.5), "bold"))
            
            self.canvas.tag_bind(p_rect, "<Button-1>", lambda e: self.toggle_pause())
            self.canvas.tag_bind(p_lbl, "<Button-1>", lambda e: self.toggle_pause())

        pass

    def start_game(self):
        # Reset Logic Environment
        self.game_env.reset()
        self.board = [None] * 9
        self.winner = None
        self.winning_line = None
        
        # Reset Timer and Pause
        self.elapsed_time = 0
        self.is_paused = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.start_timer()

        # Force Human to always start (Human = 1, AI = -1 in BasicGame)
        self.who_starts = "Human" # Ensure it's set
        self.human_id = 1
        self.ai_id = -1
            
        self.current_screen = "playing"
        self.draw()

    def start_timer(self):
        self.timer_id = self.root.after(1000, self.update_timer)

    def update_timer(self):
        if not self.is_paused and not self.winner:
            self.elapsed_time += 1
            # Redraw only the timer part if possible, but draw() is simpler for now
            self.draw()
            
        if not self.winner:
            self.timer_id = self.root.after(1000, self.update_timer)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.draw()

    def sync_board(self):
        """Syncs game_env.board (2D) to self.board (1D for display)"""
        for r in range(3):
            for c in range(3):
                val = self.game_env.board[r][c]
                idx = r * 3 + c
                if val == 0:
                    self.board[idx] = None
                elif val == self.human_id:
                    self.board[idx] = self.player_symbol
                else:
                    opponent_symbol = "O" if self.player_symbol == "X" else "X"
                    self.board[idx] = opponent_symbol
        
        # Check logic for winner
        from environnement.game_rules import GameRules
        winner_id = GameRules.check_winner(self.game_env.board)
        if winner_id != 0:
            if winner_id == self.human_id:
                self.winner = "Human"
            elif winner_id == self.ai_id:
                self.winner = "AI"
            
            # Find winning line for display
            self.winning_line = self.get_winning_line_indices()
        elif self.game_env.moves_count == 9:
            self.winner = "Draw"

        self.draw()

        if self.winner:
            self.handle_game_end()

    def get_winning_line_indices(self):
        wins = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8), # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8), # Cols
            (0, 4, 8), (2, 4, 6)             # Diags
        ]
        for combo in wins:
            vals = [self.board[i] for i in combo]
            if vals[0] and vals[0] == vals[1] == vals[2]:
                return combo
        return None

    def handle_click(self, idx):
        # Only allow click if it's human turn and game not over and not paused
        if not self.is_paused and self.game_env.current_player == self.human_id and self.board[idx] is None and not self.winner:
            r, c = divmod(idx, 3)
            self.game_env.step((r, c))
            self.sync_board()
            
            if not self.winner:
                # Trigger AI move
                self.root.after(500, self.ai_move)

    def ai_move(self):
        if self.winner or self.is_paused:
            return

        state = self.game_env.get_state()
        valid_moves = self.game_env.get_validMoves()
        
        # Act
        action = self.ai_agent.act(state, valid_moves)
        
        # Step
        self.game_env.step(action)
        self.sync_board()

    def handle_game_end(self):
        # Transistion to game over screen after a delay
        self.root.after(1500, self.switch_to_game_over)

    def switch_to_game_over(self):
        self.current_screen = "game_over"
        self.draw()

    def draw_game_over(self, w, h):
        # Result Text
        if self.winner == "Draw":
            result_text = "No one Won"
            result_color = "white"
        elif self.winner == "Human":
            result_text = "You Won"
            result_color = self.COLORS["lime"]
        else:
            result_text = "AI Won"
            result_color = self.COLORS["orange"]

        self.canvas.create_text(
            w/2, h*0.35,
            text=result_text,
            fill=result_color,
            font=("Arial Rounded MT Bold", int(h*0.12), "bold")
        )

        # Buttons
        btn_w, btn_h = w * 0.3, h * 0.1
        
        # Play Again Button
        pa_x1 = (w - btn_w) / 2
        pa_y1 = h * 0.55
        pa_rect = self.draw_round_rect(pa_x1, pa_y1, pa_x1 + btn_w, pa_y1 + btn_h, r=15, fill=self.COLORS["box"])
        pa_text = self.canvas.create_text(w/2, pa_y1 + btn_h/2, text="PLAY AGAIN", fill="white", font=("Arial Rounded MT Bold", int(btn_h*0.4), "bold"))
        
        # Back to Menu Button
        mm_x1 = (w - btn_w) / 2
        mm_y1 = h * 0.7
        mm_rect = self.draw_round_rect(mm_x1, mm_y1, mm_x1 + btn_w, mm_y1 + btn_h, r=15, fill=self.COLORS["grid"])
        mm_text = self.canvas.create_text(w/2, mm_y1 + btn_h/2, text="MENU", fill="white", font=("Arial Rounded MT Bold", int(btn_h*0.4), "bold"))

        self.canvas.tag_bind(pa_rect, "<Button-1>", lambda e: self.start_game())
        self.canvas.tag_bind(pa_text, "<Button-1>", lambda e: self.start_game())
        self.canvas.tag_bind(mm_rect, "<Button-1>", lambda e: self.switch_to_menu())
        self.canvas.tag_bind(mm_text, "<Button-1>", lambda e: self.switch_to_menu())

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
