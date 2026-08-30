import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

width = 10
height = 20

pieces = {
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
    st.session_state.board = [[0] * width for _ in range(height)]
if "current_piece" not in st.session_state:
    st.session_state.current_piece = random.choice(list(pieces.keys()))
if "rotation" not in st.session_state:
    st.session_state.rotation = 0
if "piece_row" not in st.session_state:
    st.session_state.piece_row = 0
if "piece_col" not in st.session_state:
    st.session_state.piece_col = width // 2 - 2
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "action" not in st.session_state:
    st.session_state.action = None

def get_cells():
    shape = pieces[st.session_state.current_piece]
    rotation = st.session_state.rotation % len(shape)
    return shape[rotation]

def can_place(row_offset, col_offset, cells):
    for r, c in cells:
        nr = row_offset + r
        nc = col_offset + c
        if nr < 0 or nr >= height or nc < 0 or nc >= width:
            return False
        if st.session_state.board[nr][nc]:
            return False
    return True

def lock_piece():
    cells = get_cells()
    for r, c in cells:
        nr = st.session_state.piece_row + r
        nc = st.session_state.piece_col + c
        if 0 <= nr < height and 0 <= nc < width:
            st.session_state.board[nr][nc] = 1

def clear_lines():
    new_board = [row for row in st.session_state.board if any(cell == 0 for cell in row)]
    cleared = height - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, [0] * width)
    st.session_state.board = new_board
    st.session_state.score += cleared * 100

def spawn_piece():
    st.session_state.current_piece = random.choice(list(pieces.keys()))
    st.session_state.rotation = 0
    st.session_state.piece_row = 0
    st.session_state.piece_col = width // 2 - 2
    if not can_place(st.session_state.piece_row, st.session_state.piece_col, get_cells()):
        st.session_state.game_over = True

if st.session_state.action == "LEFT":
    if not st.session_state.game_over:
        if can_place(st.session_state.piece_row, st.session_state.piece_col - 1, get_cells()):
            st.session_state.piece_col -= 1
if st.session_state.action == "RIGHT":
    if not st.session_state.game_over:
        if can_place(st.session_state.piece_row, st.session_state.piece_col + 1, get_cells()):
            st.session_state.piece_col += 1
if st.session_state.action == "DOWN":
    if not st.session_state.game_over:
        if can_place(st.session_state.piece_row + 1, st.session_state.piece_col, get_cells()):
            st.session_state.piece_row += 1
if st.session_state.action == "ROTATE":
    if not st.session_state.game_over:
        next_rot = (st.session_state.rotation + 1) % len(pieces[st.session_state.current_piece])
        cells = pieces[st.session_state.current_piece][next_rot]
        if can_place(st.session_state.piece_row, st.session_state.piece_col, cells):
            st.session_state.rotation = next_rot
st.session_state.action = None

if not st.session_state.game_over:
    if can_place(st.session_state.piece_row + 1, st.session_state.piece_col, get_cells()):
        st.session_state.piece_row += 1
    else:
        lock_piece()