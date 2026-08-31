import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'move_left' not in st.session_state:
    st.session_state.move_left = False
if 'move_right' not in st.session_state:
    st.session_state.move_right = False
if 'move_down' not in st.session_state:
    st.session_state.move_down = False
if 'rotate' not in st.session_state:
    st.session_state.rotate = False
if 'shapes' not in st.session_state:
    st.session_state.shapes = [
        [(0,1),(1,1),(2,1),(3,1)],
        [(1,0),(2,0),(1,1),(2,1)],
        [(1,0),(0,1),(1,1),(2,1)],
        [(1,0),(2,0),(0,1),(1,1)],
        [(0,0),(1,0),(1,1),(2,1)],
        [(0,0),(0,1),(1,1),(2,1)],
        [(2,0),(0,1),(1,1),(2,1)]
    ]
if 'colors' not in st.session_state:
    st.session_state.colors = ["⬜","🟥","🟦","🟩","🟨","🟪","🟧","🟫"]
def spawn_piece():
    shape = random.choice(st.session_state.shapes)
    color = random.randint(1, len(st.session_state.colors)-1)
    return {"shape": shape, "x": 3, "y": 0, "color": color}
if 'current_piece' not in st.session_state:
    st.session_state.current_piece = spawn_piece()
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("←", key="btn_left"):
        st.session_state.move_left = True
with col2:
    if st.button("↓", key="btn_down"):
        st.session_state.move_down = True
with col3:
    if st.button("→", key="btn_right"):
        st.session_state.move_right = True
with col4:
    if st.button("⤾", key="btn_rotate"):
        st.session_state.rotate = True
if st.button("Restart", key="btn_restart"):
    for k in ["board","score","game_over","move_left","move_right","move_down","rotate","current_piece"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()
def can_place(piece, dx=0, dy=0, new_shape=None):
    shape = new_shape if new_shape is not None else piece["shape"]
    for sx, sy in shape:
        x = piece["x"] + sx + dx
        y = piece["y"] + sy + dy
        if x < 0 or x >= 10 or y < 0 or y >= 20:
            return False
        if st.session_state.board[y][x] != 0:
            return False
    return True
def rotate(shape):
    return [(3 - y, x) for x, y in shape]
if not st.session_state.game_over:
    if st.session_state.move_left:
        if can_place(st.session_state.current_piece, dx=-1):
            st.session_state.current_piece["x"] -= 1
        st.session_state.move_left = False
    if st.session_state.move_right:
        if can_place(st.session_state.current_piece, dx=1):
            st.session_state.current_piece["x"] += 1
        st.session_state.move_right = False
    if st.session_state.rotate:
        new_shape = rotate(st.session_state.current_piece["shape"])
        if can_place(st.session_state.current_piece, new_shape=new_shape):
            st.session_state.current_piece["shape"] = new_shape
        st.session_state.rotate = False
    if st.session_state.move_down:
        if can_place(st.session_state.current_piece, dy=1):
            st.session_state.current_piece["y"] += 1
        st.session_state.move_down = False
    if can_place(st.session_state.current_piece, dy=1):
        st.session_state.current_piece["y"] += 1
    else:
        piece = st.session_state.current_piece
        for sx, sy in piece["shape"]:
            x = piece["x"] + sx
            y = piece["y"] + sy
            st.session_state.board[y][x] = piece["color"]
        cleared = 0
        new_board = []
        for row in st.session_state.board:
            if all(cell != 0 for cell in row):
                cleared += 1
            else:
                new_board.append(row)
        for _ in range(cleared):
            new_board.insert(0, [0 for _ in range(10)])
        st.session_state.board = new_board
        st.session_state.score += cleared * 100
        st.session_state.current_piece = spawn_piece()
        if not can_place(st.session_state.current_piece):
            st.session_state.game_over = True
display_board = [row[:] for row in st.session_state.board]
if not st.session_state.game_over:
    piece = st.session_state.current_piece
    for sx, sy in piece["shape"]:
        x = piece["x"] + sx
        y = piece["y"] + sy
        if 0 <= y < 20 and 0 <= x < 10:
            display_board[y][x] = piece["color"]
board_str = "\n".join("".join(st.session_state.colors[cell] for cell in row) for row in display_board)
st.code(board_str, language="text")
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.write("Game Over! Press Restart to play again.")