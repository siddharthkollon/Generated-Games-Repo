import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import copy

st_autorefresh(interval=200, key="game_loop_ticker")

if 'board_width' not in st.session_state:
    st.session_state.board_width = 10
if 'board_height' not in st.session_state:
    st.session_state.board_height = 20
if 'board' not in st.session_state:
    st.session_state.board = [["⬜"] * st.session_state.board_width for _ in range(st.session_state.board_height)]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'pending_action' not in st.session_state:
    st.session_state.pending_action = None
if 'current_piece' not in st.session_state:
    st.session_state.current_piece = None
if 'piece_coords' not in st.session_state:
    st.session_state.piece_coords = []
if 'piece_color' not in st.session_state:
    st.session_state.piece_color = "🟥"

def generate_piece():
    shapes = {
        "I": [(0, -1), (0, 0), (0, 1), (0, 2)],
        "O": [(0, 0), (1, 0), (0, 1), (1, 1)],
        "T": [(-1, 0), (0, 0), (1, 0), (0, 1)],
        "S": [(0, 0), (1, 0), (-1, 1), (0, 1)],
        "Z": [(-1, 0), (0, 0), (0, 1), (1, 1)],
        "J": [(-1, -1), (-1, 0), (0, 0), (1, 0)],
        "L": [(1, -1), (-1, 0), (0, 0), (1, 0)]
    }
    colors = {
        "I": "🟦",
        "O": "🟨",
        "T": "🟪",
        "S": "🟩",
        "Z": "🟥",
        "J": "🟧",
        "L": "🟫"
    }
    piece = random.choice(list(shapes.keys()))
    st.session_state.current_piece = piece
    st.session_state.piece_color = colors[piece]
    shape = shapes[piece]
    offset_x = st.session_state.board_width // 2
    offset_y = 0
    st.session_state.piece_coords = [(x + offset_x, y + offset_y) for x, y in shape]

def can_move(coords):
    for x, y in coords:
        if x < 0 or x >= st.session_state.board_width or y < 0 or y >= st.session_state.board_height:
            return False
        if st.session_state.board[y][x] != "⬜":
            return False
    return True

def lock_piece():
    for x, y in st.session_state.piece_coords:
        if 0 <= y < st.session_state.board_height and 0 <= x < st.session_state.board_width:
            st.session_state.board[y][x] = st.session_state.piece_color

def clear_lines():
    new_board = []
    lines = 0
    for row in st.session_state.board:
        if all(cell != "⬜" for cell in row):
            lines += 1
        else:
            new_board.append(row)
    for _ in range(lines):
        new_board.insert(0, ["⬜"] * st.session_state.board_width)
    st.session_state.board = new_board
    st.session_state.score += lines * 100

def rotate_piece():
    if not st.session_state.piece_coords or len(st.session_state.piece_coords) < 2:
        return
    if st.session_state.current_piece == "O":
        return
    pivot = st.session_state.piece_coords[1]
    new_coords = []
    for x, y in st.session_state.piece_coords:
        dx = x - pivot[0]
        dy = y - pivot[1]
        nx = -dy + pivot[0]
        ny = dx + pivot[1]
        new_coords.append((nx, ny))
    if can_move(new_coords):
        st.session_state.piece_coords = new_coords

if st.session_state.current_piece is None:
    generate_piece()

if not st.session_state.game_over:
    if st.session_state.pending_action == "LEFT":
        moved = [(x - 1, y) for x, y in st.session_state.piece_coords]
        if can_move(moved):
            st.session_state.piece_coords = moved
    elif st.session_state.pending_action == "RIGHT":
        moved = [(x + 1, y) for x, y in st.session_state.piece_coords]
        if can_move(moved):
            st.session_state.piece_coords = moved
    elif st.session_state.pending_action == "ROTATE":
        rotate_piece()
    elif st.session_state.pending_action == "DOWN":
        moved = [(x, y + 1) for x, y in st.session_state.piece_coords]
        if can_move(moved):
            st.session_state.piece_coords = moved
    st.session_state.pending_action = None
    down = [(x, y + 1) for x, y in st.session_state.piece_coords]
    if can_move(down):
        st.session_state.piece_coords = down
    else:
        lock_piece()
        clear_lines()
        generate_piece()
        if not can_move(st.session_state.piece_coords):
            st.session_state.game_over = True

st.title("🟦 Tetris")
st.write(f"Score: {st.session_state.score}")

c1, c2, c3, c4 = st.columns(4)
with c1:
    if st.button("←", key="btn_left"):
        st.session_state.pending_action = "LEFT"
with c2:
    if st.button("→", key="btn_right"):
        st.session_state.pending_action = "RIGHT"
with c3:
    if st.button("⤾", key="btn_rotate"):
        st.session_state.pending_action = "ROTATE"
with c4:
    if st.button("↓", key="btn_down"):
        st.session_state.pending_action = "DOWN"

if st.session_state.game_over:
    st.subheader("Game Over")
    if st.button("Restart", key="btn_restart"):
        st.session_state.board = [["⬜"] * st.session_state.board_width for _ in range(st.session_state.board_height)]
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.current_piece = None
        st.session_state.piece_coords = []
        generate_piece()
        st.rerun()
else:
    display = copy.deepcopy(st.session_state.board)
    for x, y in st.session_state.piece_coords:
        if 0 <= y < st.session_state.board_height and 0 <= x < st.session_state.board_width:
            display[y][x] = st.session_state.piece_color
    board_str = "\n".join("".join(row) for row in display)
    st.code(board_str, language="text")