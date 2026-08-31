import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.move_left = False
    st.session_state.move_right = False
    st.session_state.move_down = False
    st.session_state.rotate = False
    shapes = [
        [(0,1),(1,1),(2,1),(3,1)],
        [(1,0),(2,0),(1,1),(2,1)],
        [(1,0),(0,1),(1,1),(2,1)],
        [(1,0),(2,0),(0,1),(1,1)],
        [(0,0),(1,0),(1,1),(2,1)],
        [(0,0),(0,1),(1,1),(2,1)],
        [(2,0),(0,1),(1,1),(2,1)]
    ]
    colors = ["⬛","🟥","🟦","🟩","🟨","🟪","🟧","🟫"]
    st.session_state.shapes = shapes
    st.session_state.colors = colors
    def spawn_piece():
        shape = random.choice(st.session_state.shapes)
        color = random.randint(1, len(st.session_state.colors)-1)
        piece = {"shape": shape, "x": 3, "y": 0, "color": color}
        return piece
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
    for (sx, sy) in shape:
        x = piece["x"] + sx + dx
        y = piece["y"] + sy + dy
        if x < 0 or x >= 10 or y < 0 or y >= 20:
            return False
        if st.session_state.board[y][x] != 0:
            return False
    return True

def rotate(shape):
    return [(3 - y, x) for (x, y) in shape]

if not st.session_state.game_over:
    if st.session_state.move_left:
        if can_place(st.session_state.current_piece, dx=-1):
            st.session_state.current_piece["x"] -= 1
        st.session_state.move_left = False
    i