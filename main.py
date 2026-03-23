import tkinter as tk
from tkinter import font as tkfont
import threading
import time

from minimax import ai_play
from utils import result, terminal, utility, players, actions, winner


# ── Paleta ────────────────────────────────────────────────────────────────────
BG          = "#0d0d0d"
PANEL       = "#141414"
CELL_BG     = "#1a1a1a"
CELL_HOVER  = "#222222"
BORDER      = "#2a2a2a"
ACCENT_X    = "#e63946"  
ACCENT_O    = "#457b9d"  
TEXT_LIGHT  = "#f1faee"
TEXT_DIM    = "#6b7280"
WIN_GLOW    = "#ffd166"

EMPTY_BOARD = [[None, None, None],
               [None, None, None],
               [None, None, None]]


def copy_board(b):
    return [row[:] for row in b]


class TicTacToeApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tic-Tac-Toe  ·  vs IA")
        self.resizable(False, False)
        self.configure(bg=BG)

        # Estado
        self.board       = copy_board(EMPTY_BOARD)
        self.human       = "X"        # humano siempre empieza como X
        self.game_over   = False
        self.ai_thinking = False
        self.buttons     = {}

        self._build_fonts()
        self._build_ui()
        self._update_status("Tu turno — juegas con ✕", ACCENT_X)

    # ── Fuentes ───────────────────────────────────────────────────────────────
    def _build_fonts(self):
        self.font_title  = tkfont.Font(family="Courier New", size=18, weight="bold")
        self.font_mark   = tkfont.Font(family="Courier New", size=46, weight="bold")
        self.font_status = tkfont.Font(family="Courier New", size=12)
        self.font_btn    = tkfont.Font(family="Courier New", size=10)

    # ── UI ────────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Título
        tk.Label(self, text="[ TIC-TAC-TOE ]", font=self.font_title,
                 bg=BG, fg=TEXT_LIGHT, pady=18).pack()

        # Tablero
        grid_frame = tk.Frame(self, bg=BORDER, padx=3, pady=3)
        grid_frame.pack(padx=30)

        for row in range(3):
            for col in range(3):
                btn = tk.Button(
                    grid_frame,
                    text="",
                    font=self.font_mark,
                    width=3, height=1,
                    bg=CELL_BG,
                    fg=TEXT_LIGHT,
                    activebackground=CELL_HOVER,
                    activeforeground=TEXT_LIGHT,
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda c=col, r=row: self._human_move(c, r)
                )
                btn.grid(row=row, column=col, padx=2, pady=2)
                btn.bind("<Enter>", lambda e, b=btn: self._on_hover(b, True))
                btn.bind("<Leave>", lambda e, b=btn: self._on_hover(b, False))
                self.buttons[(row, col)] = btn

        # Status
        self.status_var = tk.StringVar()
        tk.Label(self, textvariable=self.status_var, font=self.font_status,
                 bg=BG, fg=TEXT_DIM, pady=14, wraplength=340).pack()

        # Botón reiniciar
        restart_btn = tk.Button(
            self, text="⟳  NUEVA PARTIDA",
            font=self.font_btn,
            bg=PANEL, fg=TEXT_DIM,
            activebackground=BORDER, activeforeground=TEXT_LIGHT,
            relief="flat", bd=0, padx=18, pady=8,
            cursor="hand2",
            command=self._restart
        )
        restart_btn.pack(pady=(0, 22))
        restart_btn.bind("<Enter>", lambda e: restart_btn.config(fg=TEXT_LIGHT))
        restart_btn.bind("<Leave>", lambda e: restart_btn.config(fg=TEXT_DIM))

    # ── Interacción ───────────────────────────────────────────────────────────
    def _on_hover(self, btn, entering):
        if btn["text"] == "" and not self.game_over and not self.ai_thinking:
            btn.config(bg=CELL_HOVER if entering else CELL_BG)

    def _human_move(self, col, row):
        """col, row porque utils usa (columna, fila)"""
        if self.game_over or self.ai_thinking:
            return
        if players(self.board) != self.human:
            return
        if self.board[row][col] is not None:
            return

        self.board = result(self.board, (col, row))
        self._render_board()

        if self._check_end():
            return

        # Turno de la IA
        self._update_status("IA pensando…", TEXT_DIM)
        self.ai_thinking = True
        threading.Thread(target=self._ai_move, daemon=True).start()

    def _ai_move(self):
        time.sleep(0.35)          # pausa breve para que se vea natural
        move = ai_play(self.board)
        if move is not None:
            self.board = result(self.board, move)
        self.after(0, self._after_ai)

    def _after_ai(self):
        self.ai_thinking = False
        self._render_board()
        if not self._check_end():
            self._update_status("Tu turno — juegas con ✕", ACCENT_X)

    # ── Render ────────────────────────────────────────────────────────────────
    def _render_board(self, highlight=None):
        for (row, col), btn in self.buttons.items():
            val = self.board[row][col]
            if val == "X":
                btn.config(text="✕", fg=ACCENT_X, bg=CELL_BG, state="disabled",
                           disabledforeground=ACCENT_X)
            elif val == "O":
                btn.config(text="○", fg=ACCENT_O, bg=CELL_BG, state="disabled",
                           disabledforeground=ACCENT_O)
            else:
                btn.config(text="", bg=CELL_BG, state="normal")

        if highlight:
            for (row, col) in highlight:
                self.buttons[(row, col)].config(bg="#2d2d1a")   # tinte dorado sutil

    def _check_end(self):
        if not terminal(self.board):
            return False

        self.game_over = True
        score = utility(self.board)
        winning_cells = winner(self.board)

        if winning_cells:
            self._render_board(highlight=winning_cells)

        # Deshabilitar todo
        for btn in self.buttons.values():
            btn.config(state="disabled", cursor="arrow")

        if score == 1:
            self._update_status("¡Ganaste! 🎉", WIN_GLOW)
        elif score == -1:
            self._update_status("Ganó la IA 🤖", ACCENT_O)
        else:
            self._update_status("Empate — ¡buen juego! 🤝", TEXT_LIGHT)

        return True

    # ── Status & Restart ──────────────────────────────────────────────────────
    def _update_status(self, msg, color=TEXT_DIM):
        self.status_var.set(msg)
        for widget in self.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("textvariable") == str(self.status_var):
                widget.config(fg=color)
                return
        # fallback: buscar por variable
        for widget in self.winfo_children():
            try:
                if widget.cget("textvariable"):
                    widget.config(fg=color)
            except tk.TclError:
                pass

    def _restart(self):
        self.board       = copy_board(EMPTY_BOARD)
        self.game_over   = False
        self.ai_thinking = False
        self._render_board()
        self._update_status("Tu turno — juegas con ✕", ACCENT_X)
        for btn in self.buttons.values():
            btn.config(state="normal", cursor="hand2", bg=CELL_BG)


if __name__ == "__main__":
    app = TicTacToeApp()
    app.mainloop()