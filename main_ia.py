import pygame
import sys
import math
import threading
import time
import random

from minimax import ai_play
from utils import result, terminal, utility, players, winner

# ── Configuración ─────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 480, 600
FPS           = 60
CELL          = 120
GRID_X        = (WIDTH - CELL * 3) // 2        # 60
GRID_Y        = 130
PIXEL         = 4   # tamaño de cada "pixel" retro

# ── Paleta Game Boy / NES retro ───────────────────────────────────────────────
BG          = ( 15,  15,  35)   # azul noche profundo
BG2         = ( 20,  20,  48)   # filas alternadas
GRID_DARK   = ( 40,  40,  80)
GRID_LIGHT  = ( 60,  60, 110)
COL_X       = (252,  98,  98)   # rojo píxel
COL_O       = ( 98, 214, 252)   # cian píxel
COL_WIN     = (252, 224,  98)   # amarillo ganador
COL_BTN     = ( 48,  48,  96)
COL_BTN_HL  = ( 80,  80, 140)
COL_TEXT    = (200, 200, 240)
COL_DIM     = ( 80,  80, 120)
COL_SHADOW  = (  8,   8,  20)
COL_STAR    = (180, 180, 220)
COL_BORDER  = ( 90,  90, 160)

# ── Sprites píxel 7×7 para X y O ─────────────────────────────────────────────
# Cada sprite es una lista de filas de 0/1
SPRITE_X = [
    [1,0,0,0,0,0,1],
    [0,1,0,0,0,1,0],
    [0,0,1,0,1,0,0],
    [0,0,0,1,0,0,0],
    [0,0,1,0,1,0,0],
    [0,1,0,0,0,1,0],
    [1,0,0,0,0,0,1],
]

SPRITE_O = [
    [0,1,1,1,1,1,0],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [1,0,0,0,0,0,1],
    [0,1,1,1,1,1,0],
]

# Fuente píxel 5×7 — solo letras/números necesarios
PIXEL_FONT = {
    'A': [[0,1,1,1,0],[1,0,0,0,1],[1,1,1,1,1],[1,0,0,0,1],[1,0,0,0,1]],
    'B': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0]],
    'C': [[0,1,1,1,1],[1,0,0,0,0],[1,0,0,0,0],[1,0,0,0,0],[0,1,1,1,1]],
    'D': [[1,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,1,1,1,0]],
    'E': [[1,1,1,1,1],[1,0,0,0,0],[1,1,1,1,0],[1,0,0,0,0],[1,1,1,1,1]],
    'G': [[0,1,1,1,1],[1,0,0,0,0],[1,0,1,1,1],[1,0,0,0,1],[0,1,1,1,1]],
    'I': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[1,1,1,1,1]],
    'J': [[0,0,0,0,1],[0,0,0,0,1],[0,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
    'M': [[1,0,0,0,1],[1,1,0,1,1],[1,0,1,0,1],[1,0,0,0,1],[1,0,0,0,1]],
    'N': [[1,0,0,0,1],[1,1,0,0,1],[1,0,1,0,1],[1,0,0,1,1],[1,0,0,0,1]],
    'O': [[0,1,1,1,0],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
    'P': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,0,0,0],[1,0,0,0,0]],
    'R': [[1,1,1,1,0],[1,0,0,0,1],[1,1,1,1,0],[1,0,1,0,0],[1,0,0,1,1]],
    'S': [[0,1,1,1,1],[1,0,0,0,0],[0,1,1,1,0],[0,0,0,0,1],[1,1,1,1,0]],
    'T': [[1,1,1,1,1],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
    'U': [[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[1,0,0,0,1],[0,1,1,1,0]],
    'V': [[1,0,0,0,1],[1,0,0,0,1],[0,1,0,1,0],[0,1,0,1,0],[0,0,1,0,0]],
    'W': [[1,0,0,0,1],[1,0,0,0,1],[1,0,1,0,1],[1,1,0,1,1],[1,0,0,0,1]],
    'X': [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,1,0,1,0],[1,0,0,0,1]],
    'Y': [[1,0,0,0,1],[0,1,0,1,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0]],
    'Z': [[1,1,1,1,1],[0,0,0,1,0],[0,0,1,0,0],[0,1,0,0,0],[1,1,1,1,1]],
    '!': [[0,0,1,0,0],[0,0,1,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,1,0,0]],
    '-': [[0,0,0,0,0],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[0,0,0,0,0]],
    ' ': [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]],
    ':': [[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0],[0,0,1,0,0],[0,0,0,0,0]],
    '?': [[0,1,1,1,0],[1,0,0,0,1],[0,0,1,1,0],[0,0,0,0,0],[0,0,1,0,0]],
}


def draw_pixel_text(surface, text, x, y, color, scale=2):
    """Dibuja texto usando la fuente píxel personalizada."""
    cx = x
    for ch in text.upper():
        if ch not in PIXEL_FONT:
            cx += (5 + 1) * scale
            continue
        bitmap = PIXEL_FONT[ch]
        for row_i, row in enumerate(bitmap):
            for col_i, bit in enumerate(row):
                if bit:
                    pygame.draw.rect(surface, color,
                                     (cx + col_i * scale,
                                      y  + row_i * scale,
                                      scale, scale))
        cx += (5 + 1) * scale
    return cx


def pixel_text_width(text, scale=2):
    return len(text) * (5 + 1) * scale


def draw_sprite(surface, sprite, cx, cy, color, scale, alpha=255):
    """Dibuja un sprite centrado en (cx, cy)."""
    rows = len(sprite)
    cols = len(sprite[0])
    ox   = cx - cols * scale // 2
    oy   = cy - rows * scale // 2
    for r, row in enumerate(sprite):
        for c, bit in enumerate(row):
            if bit:
                rect = pygame.Rect(ox + c * scale, oy + r * scale, scale, scale)
                if alpha < 255:
                    s = pygame.Surface((scale, scale), pygame.SRCALPHA)
                    s.fill((*color, alpha))
                    surface.blit(s, rect.topleft)
                else:
                    pygame.draw.rect(surface, color, rect)


def draw_pixel_rect(surface, color, rect, border=2):
    """Rectángulo con borde pixelado."""
    pygame.draw.rect(surface, color, rect)
    # Esquinas en sombra para efecto 3D
    shadow = tuple(max(0, c - 40) for c in color)
    highlight = tuple(min(255, c + 60) for c in color)
    x, y, w, h = rect
    # top-left highlight
    pygame.draw.line(surface, highlight, (x, y), (x + w - 1, y), border)
    pygame.draw.line(surface, highlight, (x, y), (x, y + h - 1), border)
    # bottom-right shadow
    pygame.draw.line(surface, shadow, (x, y + h - 1), (x + w - 1, y + h - 1), border)
    pygame.draw.line(surface, shadow, (x + w - 1, y), (x + w - 1, y + h - 1), border)


class Star:
    def __init__(self):
        self.reset(random.randint(0, HEIGHT))

    def reset(self, y=0):
        self.x     = random.randint(0, WIDTH)
        self.y     = float(y)
        self.speed = random.uniform(0.3, 1.2)
        self.size  = random.choice([1, 1, 1, 2])
        self.alpha = random.randint(60, 200)

    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.reset()

    def draw(self, surface):
        s = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        s.fill((*COL_STAR, self.alpha))
        surface.blit(s, (int(self.x), int(self.y)))


class AnimMark:
    """Marca que aparece pixel a pixel."""
    def __init__(self, mark, cx, cy, color):
        self.mark     = mark
        self.cx       = cx
        self.cy       = cy
        self.color    = color
        self.scale    = 8
        self.sprite   = SPRITE_X if mark == "X" else SPRITE_O
        self.pixels   = [(r, c)
                         for r, row in enumerate(self.sprite)
                         for c, bit in enumerate(row) if bit]
        random.shuffle(self.pixels)
        self.revealed = 0
        self.timer    = 0
        self.done     = False

    def update(self):
        if self.revealed < len(self.pixels):
            self.timer += 1
            if self.timer % 2 == 0:
                self.revealed += 2
        else:
            self.done = True

    def draw(self, surface, win_flash=False):
        sc    = self.scale
        rows  = len(self.sprite)
        cols  = len(self.sprite[0])
        ox    = self.cx - cols * sc // 2
        oy    = self.cy - rows * sc // 2
        color = COL_WIN if win_flash else self.color

        revealed_set = set(self.pixels[:self.revealed])
        for r, row in enumerate(self.sprite):
            for c, bit in enumerate(row):
                if bit and (r, c) in revealed_set:
                    # Sombra
                    pygame.draw.rect(surface, COL_SHADOW,
                                     (ox + c*sc + 2, oy + r*sc + 2, sc, sc))
                    pygame.draw.rect(surface, color,
                                     (ox + c*sc, oy + r*sc, sc, sc))


class TicTacToePixel:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("TIC-TAC-TOE  PIXEL QUEST")
        self.clock  = pygame.time.Clock()

        self.board       = [[None]*3 for _ in range(3)]
        self.human       = "X"
        self.game_over   = False
        self.ai_thinking = False
        self.marks       = {}
        self.status_msg  = "YOUR TURN - PLAYER X"
        self.status_col  = COL_X
        self.win_cells   = []
        self.win_flash   = 0
        self.hover_cell  = None
        self.frame       = 0

        self.stars = [Star() for _ in range(80)]

        # Tiles animados de fondo
        self.tile_offset = 0.0

    # ── Loop ──────────────────────────────────────────────────────────────────
    def run(self):
        while True:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._draw()

    # ── Eventos ───────────────────────────────────────────────────────────────
    def _handle_events(self):
        mouse = pygame.mouse.get_pos()
        self.hover_cell = self._cell_at(mouse)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self._btn_rect().collidepoint(mouse):
                    self._restart(); return
                cell = self._cell_at(mouse)
                if cell and not self.game_over and not self.ai_thinking:
                    row, col = cell
                    if self.board[row][col] is None and players(self.board) == self.human:
                        self._place(row, col)

    def _cell_rect(self, row, col):
        x = GRID_X + col * CELL
        y = GRID_Y + row * CELL
        return pygame.Rect(x + 4, y + 4, CELL - 8, CELL - 8)

    def _cell_at(self, pos):
        for r in range(3):
            for c in range(3):
                if self._cell_rect(r, c).collidepoint(pos):
                    return (r, c)
        return None

    def _btn_rect(self):
        return pygame.Rect(WIDTH//2 - 90, HEIGHT - 58, 180, 32)

    # ── Lógica ────────────────────────────────────────────────────────────────
    def _place(self, row, col):
        self.board = result(self.board, (col, row))
        val   = self.board[row][col]
        color = COL_X if val == "X" else COL_O
        rect  = self._cell_rect(row, col)
        self.marks[(row, col)] = AnimMark(val, rect.centerx, rect.centery, color)
        if self._check_end(): return
        self.status_msg = "AI THINKING..."
        self.status_col = COL_DIM
        self.ai_thinking = True
        threading.Thread(target=self._ai_thread, daemon=True).start()

    def _ai_thread(self):
        time.sleep(0.6)
        move = ai_play(self.board)
        if move is not None:
            col, row = move
            self.board = result(self.board, move)
            rect = self._cell_rect(row, col)
            self.marks[(row, col)] = AnimMark(
                self.board[row][col], rect.centerx, rect.centery, COL_O)
        self.ai_thinking = False
        if not self._check_end():
            self.status_msg = "YOUR TURN - PLAYER X"
            self.status_col = COL_X

    def _check_end(self):
        if not terminal(self.board): return False
        self.game_over = True
        w = winner(self.board)
        self.win_cells = w if w else []
        score = utility(self.board)
        if score == 1:
            self.status_msg = "YOU WIN!"
            self.status_col = COL_WIN
        elif score == -1:
            self.status_msg = "AI WINS!"
            self.status_col = COL_O
        else:
            self.status_msg = "DRAW - GG!"
            self.status_col = COL_TEXT
        return True

    def _restart(self):
        self.board       = [[None]*3 for _ in range(3)]
        self.game_over   = False
        self.ai_thinking = False
        self.marks       = {}
        self.win_cells   = []
        self.win_flash   = 0
        self.status_msg  = "YOUR TURN - PLAYER X"
        self.status_col  = COL_X

    # ── Update ────────────────────────────────────────────────────────────────
    def _update(self):
        self.frame += 1
        self.tile_offset = (self.tile_offset + 0.3) % 32
        for s in self.stars: s.update()
        for m in list(self.marks.values()): m.update()
        if self.win_cells:
            self.win_flash = (self.win_flash + 1) % 40

    # ── Draw ──────────────────────────────────────────────────────────────────
    def _draw(self):
        self.screen.fill(BG)
        self._draw_starfield()
        self._draw_tile_bg()
        self._draw_header()
        self._draw_grid()
        self._draw_marks()
        self._draw_win_highlight()
        self._draw_hover()
        self._draw_status()
        self._draw_button()
        pygame.display.flip()

    def _draw_starfield(self):
        for s in self.stars: s.draw(self.screen)

    def _draw_tile_bg(self):
        """Fondo con patrón de tiles retro animado."""
        tile = 32
        off  = int(self.tile_offset)
        s    = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for tx in range(-1, WIDTH // tile + 2):
            for ty in range(-1, HEIGHT // tile + 2):
                x = tx * tile - off
                y = ty * tile - off
                if (tx + ty) % 2 == 0:
                    pygame.draw.rect(s, (255, 255, 255, 4),
                                     (x, y, tile, tile))
        self.screen.blit(s, (0, 0))

    def _draw_header(self):
        # Caja de título con borde píxel
        title_rect = pygame.Rect(GRID_X, 12, CELL * 3, 50)
        pygame.draw.rect(self.screen, COL_BTN, title_rect)
        draw_pixel_rect(self.screen, COL_BTN, title_rect, 3)

        # "TIC-TAC-TOE" centrado
        text   = "TIC-TAC-TOE"
        scale  = 2
        tw     = pixel_text_width(text, scale)
        tx     = WIDTH // 2 - tw // 2
        # Sombra
        draw_pixel_text(self.screen, text, tx + 2, 20 + 2, COL_SHADOW, scale)
        draw_pixel_text(self.screen, text, tx, 20, COL_TEXT, scale)

        # Subtítulo parpadeante
        if self.frame % 60 < 45:
            sub   = "PIXEL QUEST"
            sw    = pixel_text_width(sub, 1)
            draw_pixel_text(self.screen, sub,
                            WIDTH // 2 - sw // 2, 38, COL_DIM, 1)

    def _draw_grid(self):
        # Fondo del tablero
        board_rect = pygame.Rect(GRID_X - 4, GRID_Y - 4, CELL * 3 + 8, CELL * 3 + 8)
        pygame.draw.rect(self.screen, COL_BTN, board_rect)
        draw_pixel_rect(self.screen, COL_BORDER, board_rect, 3)

        for row in range(3):
            for col in range(3):
                r = self._cell_rect(row, col)
                # Alternancia de color
                shade = BG2 if (row + col) % 2 == 0 else BG
                pygame.draw.rect(self.screen, shade, r)
                # Borde interior
                pygame.draw.rect(self.screen, GRID_DARK, r, 2)

    def _draw_marks(self):
        flash = bool(self.win_cells) and self.win_flash < 20
        for (row, col), mark in list(self.marks.items()):
            is_win = (row, col) in self.win_cells
            mark.draw(self.screen, win_flash=(is_win and flash))

    def _draw_win_highlight(self):
        if not self.win_cells: return
        alpha = int(abs(math.sin(self.win_flash / 40 * math.pi)) * 100)
        for (row, col) in self.win_cells:
            r = self._cell_rect(row, col)
            s = pygame.Surface((r.width, r.height), pygame.SRCALPHA)
            s.fill((*COL_WIN, alpha))
            self.screen.blit(s, r.topleft)
            pygame.draw.rect(self.screen, COL_WIN, r, 3)

    def _draw_hover(self):
        if not self.hover_cell or self.game_over or self.ai_thinking: return
        row, col = self.hover_cell
        if self.board[row][col] is not None: return
        if players(self.board) != self.human: return
        r = self._cell_rect(row, col)
        # Preview fantasma del sprite X
        pulse = int(abs(math.sin(self.frame / 20)) * 60) + 30
        draw_sprite(self.screen, SPRITE_X,
                    r.centerx, r.centery, COL_X, 6, alpha=pulse)
        pygame.draw.rect(self.screen, (*COL_X, 120), r, 2)

    def _draw_status(self):
        y    = GRID_Y + CELL * 3 + 16
        # Caja de status
        box  = pygame.Rect(GRID_X, y, CELL * 3, 36)
        pygame.draw.rect(self.screen, COL_BTN, box)
        draw_pixel_rect(self.screen, GRID_DARK, box, 2)

        scale = 2
        tw    = pixel_text_width(self.status_msg, scale)
        tx    = WIDTH // 2 - tw // 2
        # Sombra
        draw_pixel_text(self.screen, self.status_msg,
                        tx + 1, y + 13, COL_SHADOW, scale)
        draw_pixel_text(self.screen, self.status_msg,
                        tx, y + 12, self.status_col, scale)

    def _draw_button(self):
        r     = self._btn_rect()
        mouse = pygame.mouse.get_pos()
        hover = r.collidepoint(mouse)
        color = COL_BTN_HL if hover else COL_BTN
        pygame.draw.rect(self.screen, color, r)
        draw_pixel_rect(self.screen, COL_BORDER if hover else GRID_DARK, r, 2)

        label = "NEW GAME"
        scale = 2
        tw    = pixel_text_width(label, scale)
        tx    = r.centerx - tw // 2
        ty    = r.centery - 5 * scale // 2
        draw_pixel_text(self.screen, label, tx + 1, ty + 1, COL_SHADOW, scale)
        draw_pixel_text(self.screen, label, tx, ty,
                        COL_TEXT if hover else COL_DIM, scale)


if __name__ == "__main__":
    game = TicTacToePixel()
    game.run()