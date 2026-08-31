import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

BOARD_WIDTH = 10
BOARD_HEIGHT = 20
EMPTY = 0

SHAPES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)]
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)]
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)]
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)]
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)]
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)]
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)]
    ]
}

if "board" not in st.session_state:
    st.session_state.board = [[EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
if "current_piece" not in st.session_state:
    st.session_state.current_piece = None
if "piece_x" not in st.session_state:
    st.session_state.piece_x = 0
if "piece_y" not in st.session_state:
    st.session_state.piece_y = 0
if "rotation" not in st.session_state:
    st.session_state.rotation = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "lines_cleared" not in st.session_state:
    st.session_state.lines_cleared = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "move" not in st.session_state:
    st.session_state.move = None

def spawn_piece():
    st.session_state.current_piece = random.choice(list(SHAPES.keys()))
    st.session_state.rotation = 0
    st.session_state.piece_x = BOARD_WIDTH // 2 - 2
    st.session_state.piece_y = 0
    if not can_place(st.session_state.piece_x, st.session_state.piece_y, st.session_state.rotation):
        st.session_state.game_over = True

def get_cells(x, y, rotation):
    shape = SHAPES[st.session_state.current_piece][rotation % len(SHAPES[st.session_state.current_piece])]
    return [(x + cx, y + cy) for cx, cy in shape]

def can_place(x, y, rotation):
    for cx, cy in get_cells(x, y, rotation):
        if cx < 0 or cx >= BOARD_WIDTH or cy < 0 or cy >= BOARD_HEIGHT:
            return False
        if st.session_state.board[cy][cx] != EMPTY:
            return False
    return True

def lock_piece():
    for cx, cy in get_cells(st.session_state.piece_x, st.session_state.piece_y, st.session_state.rotation):
        st.session_state.board[cy][cx] = 1

def clear_lines():
    new_board = [row for row in st.session_state.board if any(cell == EMPTY for cell in row)]
    cleared = BOARD_HEIGHT - len(new_board)
    if cleared > 0:
        for _ in range(cleared):
            new_board.insert(0, [EMPTY for _ in range(BOARD_WIDTH)])
        st.session_state.board = new_board
        st.session_state.lines_cleared += cleared
        st.session_state.score += (cleared ** 2) * 100

if st.session_state.current_piece is None and not st.session_state.game_over:
    spawn_piece()

if not st.session_state.game_over:
    if st.session_state.move == "LEFT":
        if can_place(st.session_state.piece_x - 1, st.session_state.piece_y, st.session_state.rotation):
            st.session_state.piece_x -= 1
    elif st.session_state.move == "RIGHT":
        if can_place(st.session_state.piece_x + 1, st.session_state.piece_y, st.session_state.rotation):
            st.session_state.piece_x += 1
    elif st.session_state.move == "ROTATE":
        new_rot = (st.session_state.rotation + 1) % len(SHAPES[st.session_state.current_piece])
        if can_place(st.session_state.piece_x, st.session_state.piece_y, new_rot):
            st.session_state.rotation = new_rot
    elif st.session_state.move == "DOWN":
        if can_place(st.session_state.piece_x, st.session_state.piece_y + 1, st.session_state.rotation):
            st.session_state.piece_y += 1
    st.session_state.move = None
    if can_place(st.session_state.piece_x, st.session_state.piece_y + 1, st.session_state.rotation):
        st.session_state.piece_y += 1
    else:
        lock_piece()
        clear_lines()
        spawn_piece()

display_board = [[EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
for y in range(BOARD_HEIGHT):
    for x in range(BOARD_WIDTH):
        display_board[y][x] = st.session_state.board[y][x]
if not st.session_state.game_over:
    for cx, cy in get_cells(st.session_state.piece_x, st.session_state.piece_y, st.session_state.rotation):
        if 0 <= cy < BOARD_HEIGHT and 0 <= cx < BOARD_WIDTH:
            display_board[cy][cx] = 1
board_str = "\n".join("".join("🟦" if cell else "⬛" for cell in row) for row in display_board)
st.code(board_str, language="text")
st.write(f"Score: {st.session_state.score}")
st.write(f"Lines cleared: {st.session_state.lines_cleared}")
if st.session_state.game_over:
    st.write("💀 Game Over 💀")
if st.button("←", key="btn_left"):
    st.session_state.move = "LEFT"
if st.button("→", key="btn_right"):
    st.session_state.move = "RIGHT"
if st.button("⤾", key="btn_rotate"):
    st.session_state.move = "ROTATE"
if st.button("↓", key="btn_down"):
    st.session_state.move = "DOWN"
if st.button("Restart", key="btn_restart"):
    st.session_state.board = [[EMPTY for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    st.session_state.current_piece = None
    st.session_state.piece_x = 0
    st.session_state.piece_y = 0
    st.session_state.rotation = 0
    st.session_state.score = 0
    st.session_state.lines_cleared = 0
    st.session_state.game_over = False
    st.session_state.move = None
    st.rerun()