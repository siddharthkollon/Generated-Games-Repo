import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

WIDTH = 10
HEIGHT = 20

PIECES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)]
    ],
    "O": [
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ],
    "T": [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (1, 2), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 1)],
        [(0, 1), (1, 0), (1, 1), (2, 1)]
    ],
    "S": [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)]
    ],
    "Z": [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 0)]
    ],
    "J": [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (0, 2), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)]
    ],
    "L": [
        [(0, 2), (1, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (1, 2), (2, 0)],
        [(0, 0), (0, 1), (1, 1), (2, 1)]
    ]
}

if "board" not in st.session_state:
    st.session_state.board = [[0] * WIDTH for _ in range(HEIGHT)]
if "piece" not in st.session_state:
    st.session_state.piece = random.choice(list(PIECES.keys()))
if "rot" not in st.session_state:
    st.session_state.rot = 0
if "row" not in st.session_state:
    st.session_state.row = 0
if "col" not in st.session_state:
    st.session_state.col = WIDTH // 2 - 2
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "action" not in st.session_state:
    st.session_state.action = None

def get_cells():
    shape = PIECES[st.session_state.piece]
    return shape[st.session_state.rot % len(shape)]

def can_place(r_off, c_off, cells):
    for r, c in cells:
        nr = r_off + r
        nc = c_off + c
        if nr < 0 or nr >= HEIGHT or nc < 0 or nc >= WIDTH:
            return False
        if st.session_state.board[nr][nc]:
            return False
    return True

def lock_piece():
    for r, c in get_cells():
        nr = st.session_state.row + r
        nc = st.session_state.col + c
        if 0 <= nr < HEIGHT and 0 <= nc < WIDTH:
            st.session_state.board[nr][nc] = 1

def clear_lines():
    new_board = [row for row in st.session_state.board if any(cell == 0 for cell in row)]
    cleared = HEIGHT - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0] * WIDTH)
    st.session_state.board = new_board
    st.session_state.score += cleared * 100

def spawn_piece():
    st.session_state.piece = random.choice(list(PIECES.keys()))
    st.session_state.rot = 0
    st.session_state.row = 0
    st.session_state.col = WIDTH // 2 - 2
    if not can_place(st.session_state.row, st.session_state.col, get_cells()):
        st.session_state.game_over = True

def set_action(value):
    st.session_state.action = value

def reset_game():
    st.session_state.board = [[0] * WIDTH for _ in range(HEIGHT)]
    st.session_state.piece = random.choice(list(PIECES.keys()))
    st.session_state.rot = 0
    st.session_state.row = 0
    st.session_state.col = WIDTH // 2 - 2
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.action = None
    st.rerun()

if st.session_state.action == "LEFT" and not st.session_state.game_over:
    if can_place(st.session_state.row, st.session_state.col - 1, get_cells()):
        st.session_state.col -= 1
if st.session_state.action == "RIGHT" and not st.session_state.game_over:
    if can_place(st.session_state.row, st.session_state.col + 1, get_cells()):
        st.session_state.col += 1
if st.session_state.action == "DOWN" and not st.session_state.game_over:
    if can_place(st.session_state.row + 1, st.session_state.col, get_cells()):
        st.session_state.row += 1
if st.session_state.action == "ROTATE" and not st.session_state.game_over:
    next_rot = (st.session_state.rot + 1) % len(PIECES[st.session_state.piece])
    cells = PIECES[st.session_state.piece][next_rot]
    if can_place(st.session_state.row, st.session_state.col, cells):
        st.session_state.rot = next_rot
st.session_state.action = None

if not st.session_state.game_over:
    if can_place(st.session_state.row + 1, st.session_state.col, get_cells()):
        st.session_state.row += 1
    else:
        lock_piece()
        clear_lines()
        spawn_piece()

grid = [["⬛" if cell == 0 else "🟥" for cell in row] for row in st.session_state.board]
for r, c in get_cells():
    nr = st.session_state.row + r
    nc = st.session_state.col + c
    if 0 <= nr < HEIGHT and 0 <= nc < WIDTH:
        grid[nr][nc] = "🟦"
board_str = "\n".join("".join(row) for row in grid)

st.title("🧩 Streamlit Tetris")
st.text(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.subheader("💀 Game Over")
else:
    col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])
    with col1:
        st.button("←", on_click=set_action, args=("LEFT",), key="btn_left")
    with col2:
        st.button("↓", on_click=set_action, args=("DOWN",), key="btn_down")
    with col3:
        st.button("↑", on_click=set_action, args=("ROTATE",), key="btn_rotate")
    with col4:
        st.button("→", on_click=set_action, args=("RIGHT",), key="btn_right")
    with col5:
        st.button("🔄 Restart", on_click=reset_game, key="btn_restart")
st.code(board_str, language="text")