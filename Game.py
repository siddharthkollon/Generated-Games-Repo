import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ----------------------------------------------------------------------
# Auto‑refresh (game loop)
# ----------------------------------------------------------------------
st_autorefresh(interval=200, key="game_loop_ticker")

# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------
WIDTH = 10
HEIGHT = 20
EMPTY = 0
FILLED = 1

# ----------------------------------------------------------------------
# Tetromino definitions (rotations as list of (x, y) offsets)
# ----------------------------------------------------------------------
PIECES = [
    # I
    [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)]
    ],
    # O
    [
        [(1, 0), (2, 0), (1, 1), (2, 1)]
    ],
    # T
    [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)]
    ],
    # S
    [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)]
    ],
    # Z
    [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)]
    ],
    # J
    [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)]
    ],
    # L
    [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ]
]

# ----------------------------------------------------------------------
# Session state initialization
# ----------------------------------------------------------------------
if "board" not in st.session_state:
    st.session_state.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]

if "current_piece" not in st.session_state:
    st.session_state.current_piece = None

if "piece_rot" not in st.session_state:
    st.session_state.piece_rot = 0

if "piece_pos" not in st.session_state:
    st.session_state.piece_pos = [0, 0]

if "score" not in st.session_state:
    st.session_state.score = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "command" not in st.session_state:
    st.session_state.command = None

# ----------------------------------------------------------------------
# Helper functions
# ----------------------------------------------------------------------
def valid_position(piece_idx, rot_idx, pos):
    shape = PIECES[piece_idx][rot_idx]
    for x_off, y_off in shape:
        x = pos[0] + x_off
        y = pos[1] + y_off
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return False
        if st.session_state.board[y][x] == FILLED:
            return False
    return True


def spawn_piece():
    st.session_state.current_piece = random.randint(0, len(PIECES) - 1)
    st.session_state.piece_rot = 0
    st.session_state.piece_pos = [WIDTH // 2 - 2, 0]
    # If spawn position already collides → game over
    if not valid_position(st.session_state.current_piece,
                          st.session_state.piece_rot,
                          st.session_state.piece_pos):
        st.session_state.game_over = True


def lock_piece():
    idx = st.session_state.current_piece
    rot = st.session_state.piece_rot
    pos = st.session_state.piece_pos
    for x_off, y_off in PIECES[idx][rot]:
        x = pos[0] + x_off
        y = pos[1] + y_off
        if 0 <= y < HEIGHT and 0 <= x < WIDTH:
            st.session_state.board[y][x] = FILLED


def clear_lines():
    new_board = []
    lines_cleared = 0
    for row in st.session_state.board:
        if all(cell == FILLED for cell in row):
            lines_cleared += 1
        else:
            new_board.append(row)
    for _ in range(lines_cleared):
        new_board.insert(0, [EMPTY for _ in range(WIDTH)])
    st.session_state.board = new_board
    st.session_state.score += lines_cleared * 100


def try_move(dx, dy):
    new_pos = [st.session_state.piece_pos[0] + dx,
               st.session_state.piece_pos[1] + dy]
    if valid_position(st.session_state.current_piece,
                      st.session_state.piece_rot,
                      new_pos):
        st.session_state.piece_pos = new_pos
        return True
    return False


def try_rotate():
    piece_idx = st.session_state.current_piece
    next_rot = (st.session_state.piece_rot + 1) % len(PIECES[piece_idx])
    if valid_position(piece_idx, next_rot, st.session_state.piece_pos):
        st.session_state.piece_rot = next_rot
        return True
    return False


def reset_game():
    st.session_state.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.command = None
    spawn_piece()


# ----------------------------------------------------------------------
# UI – control buttons
# ----------------------------------------------------------------------
col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 2])

with col1:
    if st.button("←", key="btn_left"):
        st.session_state.command = "LEFT"
with col2:
    if st.button("→", key="btn_right"):
        st.session_state.command = "RIGHT"
with col3:
    if st.button("↓", key="btn_down"):
        st.session_state.command = "DOWN"
with col4:
    if st.button("⤾", key="btn_rotate"):
        st.session_state.command = "ROTATE"
with col5:
    if st.button("🔄 Restart", key="btn_restart"):
        reset_game()
        st.rerun()

# ----------------------------------------------------------------------
# Game logic – executed every refresh
# ----------------------------------------------------------------------
if not st.session_state.game_over:
    # Spawn first piece if needed
    if st.session_state.current_piece is None:
        spawn_piece()

    # Process user command
    cmd = st.session_state.command
    if cmd == "LEFT":
        try_move(-1, 0)
    elif cmd == "RIGHT":
        try_move(1, 0)
    elif cmd == "DOWN":
        try_move(0, 1)
    elif cmd == "ROTATE":
        try_rotate()
    # Reset command after handling
    st.session_state.command = None

    # Automatic descent
    moved = try_move(0, 1)
    if not moved:
        # Piece cannot fall → lock and spawn next
        lock_piece()
        clear_lines()
        spawn_piece()

# ----------------------------------------------------------------------
# Rendering the board
# ----------------------------------------------------------------------
def render_board():
    # Base visual board (empty = ⬛, filled = 🟦)
    visual = [["⬛" if cell == EMPTY else "🟦" for cell in row]
              for row in st.session_state.board]

    # Overlay active piece (use 🟥)
    if not st.session_state.game_over and st.session_state.current_piece is not None:
        idx = st.session_state.current_piece
        rot = st.session_state.piece_rot
        pos = st.session_state.piece_pos
        for x_off, y_off in PIECES[idx][rot]:
            x = pos[0] + x_off
            y = pos[1] + y_off
            if 0 <= y < HEIGHT and 0 <= x < WIDTH:
                visual[y][x] = "🟥"

    board_str = "\n".join("".join(row) for row in visual)
    st.code(board_str, language="text")

st.subheader("Score: " + str(st.session_state.score))
if st.session_state.game_over:
    st.error("💀 Game Over! Press Restart to play again.")
else:
    render_board()