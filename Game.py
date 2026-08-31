import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop")
if "width" not in st.session_state:
    st.session_state.width = 20
if "height" not in st.session_state:
    st.session_state.height = 10
if "paddle_height" not in st.session_state:
    st.session_state.paddle_height = 3
if "paddle_left_y" not in st.session_state:
    st.session_state.paddle_left_y = (st.session_state.height - st.session_state.paddle_height) // 2
if "paddle_right_y" not in st.session_state:
    st.session_state.paddle_right_y = (st.session_state.height - st.session_state.paddle_height) // 2
if "ball_x" not in st.session_state:
    st.session_state.ball_x = st.session_state.width // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = st.session_state.height // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "score_left" not in st.session_state:
    st.session_state.score_left = 0
if "score_right" not in st.session_state:
    st.session_state.score_right = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if not st.session_state.game_over:
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.height - 1:
        st.session_state.ball_dy *= -1
    if st.session_state.ball_dx < 0 and st.session_state.ball_x == 1:
        if st.session_state.paddle_left_y <= st.session_state.ball_y < st.session_state.paddle_left_y + st.session_state.paddle_height:
            st.session_state.ball_dx *= -1
            st.session_state.ball_dy = random.choice([-1, 0, 1])
    if st.session_state.ball_dx > 0 and st.session_state.ball_x == st.session_state.width - 2:
        if st.session_state.paddle_right_y <= st.session_state.ball_y < st.session_state.paddle_right_y + st.session_state.paddle_height:
            st.session_state.ball_dx *= -1
            st.session_state.ball_dy = random.choice([-1, 0, 1])
    if st.session_state.ball_x < 0:
        st.session_state.score_right += 1
        st.session_state.ball_x = st.session_state.width // 2
        st.session_state.ball_y = st.session_state.height // 2
        st.session_state.ball_dx = random.choice([-1, 1])
        st.session_state.ball_dy = random.choice([-1, 0, 1])
    if st.session_state.ball_x > st.session_state.width - 1:
        st.session_state.score_left += 1
        st.session_state.ball_x = st.session_state.width // 2
        st.session_state.ball_y = st.session_state.height // 2
        st.session_state.ball_dx = random.choice([-1, 1])
        st.session_state.ball_dy = random.choice([-1, 0, 1])
    if st.session_state.paddle_right_y + st.session_state.paddle_height // 2 < st.session_state.ball_y:
        st.session_state.paddle_right_y = min(st.session_state.height - st.session_state.paddle_height, st.session_state.paddle_right_y + 1)
    elif st.session_state.paddle_right_y + st.session_state.paddle_height // 2 > st.session_state.ball_y:
        st.session_state.paddle_right_y = max(0, st.session_state.paddle_right_y - 1)
st.title("Ping Pong")
st.write(f"Score Left: {st.session_state.score_left}   Score Right: {st.session_state.score_right}")
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Up", key="left_up"):
        st.session_state.paddle_left_y = max(0, st.session_state.paddle_left_y - 1)
    if st.button("Down", key="left_down"):
        st.session_state.paddle_left_y = min(st.session_state.height - st.session_state.paddle_height, st.session_state.paddle_left_y + 1)
with col2:
    if st.button("Restart", key="restart"):
        st.session_state.score_left = 0
        st.session_state.score_right = 0
        st.session_state.paddle_left_y = (st.session_state.height - st.session_state.paddle_height) // 2
        st.session_state.paddle_right_y = (st.session_state.height - st.session_state.paddle_height) // 2
        st.session_state.ball_x = st.session_state.width // 2
        st.session_state.ball_y = st.session_state.height // 2
        st.session_state.ball_dx = random.choice([-1, 1])
        st.session_state.ball_dy = random.choice([-1, 0, 1])
        st.rerun()
grid = [[" " for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
for i in range(st.session_state.paddle_height):
    grid[st.session_state.paddle_left_y + i][0] = "█"
    grid[st.session_state.paddle_right_y + i][st.session_state.width - 1] = "█"
if 0 <= st.session_state.ball_y < st.session_state.height and 0 <= st.session_state.ball_x < st.session_state.width:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "●"
board = "\n".join("".join(row) for row in grid)
st.code(board, language="text")