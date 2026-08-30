import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

if "board_width" not in st.session_state:
    st.session_state.board_width = 30
if "board_height" not in st.session_state:
    st.session_state.board_height = 20
if "paddle_height" not in st.session_state:
    st.session_state.paddle_height = 4
if "paddle1_y" not in st.session_state:
    st.session_state.paddle1_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
if "paddle2_y" not in st.session_state:
    st.session_state.paddle2_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
if "ball_x" not in st.session_state:
    st.session_state.ball_x = st.session_state.board_width // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = st.session_state.board_height // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "score1" not in st.session_state:
    st.session_state.score1 = 0
if "score2" not in st.session_state:
    st.session_state.score2 = 0
if "paddle1_move" not in st.session_state:
    st.session_state.paddle1_move = None

if st.button("⬆️ Up", key="up_btn"):
    st.session_state.paddle1_move = "UP"
if st.button("⬇️ Down", key="down_btn"):
    st.session_state.paddle1_move = "DOWN"
if st.button("🔄 Restart Game", key="restart_btn"):
    st.session_state.paddle1_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
    st.session_state.paddle2_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
    st.session_state.ball_x = st.session_state.board_width // 2
    st.session_state.ball_y = st.session_state.board_height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.score1 = 0
    st.session_state.score2 = 0
    st.session_state.paddle1_move = None
    st.rerun()

if st.session_state.paddle1_move == "UP":
    st.session_state.paddle1_y = max(0, st.session_state.paddle1_y - 1)
elif st.session_state.paddle1_move == "DOWN":
    st.session_state.paddle1_y = min(st.session_state.board_height - st.session_state.paddle_height, st.session_state.paddle1_y + 1)
st.session_state.paddle1_move = None

st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.board_height - 1:
    st.session_state.ball_dy *= -1

if st.session_state.ball_x == 1:
    if st.session_state.paddle1_y <= st.session_state.ball_y < st.session_state.paddle1_y + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        st.session_state.ball_dy = random.choice([-1, 0, 1])
    else:
        st.session_state.score2 += 1
        st.session_state.ball_x = st.session_state.board_width // 2
        st.session_state.ball_y = st.session_state.board_height // 2
        st.session_state.ball_dx = 1
        st.session_state.ball_dy = random.choice([-1, 0, 1])

if st.session_state.ball_x == st.session_state.board_width - 2:
    if st.session_state.paddle2_y <= st.session_state.ball_y < st.session_state.paddle2_y + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        st.session_state.ball_dy = random.choice([-1, 0, 1])
    else:
        st.session_state.score1 += 1
        st.session_state.ball_x = st.session_state.board_width // 2
        st.session_state.ball_y = st.session_state.board_height // 2
        st.session_state.ball_dx = -1
        st.session_state.ball_dy = random.choice([-1, 0, 1])

if st.session_state.ball_dy == 0:
    st.session_state.ball_dy = random.choice([-1, 1])

if st.session_state.ball_y < st.session_state.paddle2_y + st.session_state.paddle_height // 2:
    st.session_state.paddle2_y = max(0, st.session_state.paddle2_y - 1)
elif st.session_state.ball_y > st.session_state.paddle2_y + st.session_state.paddle_height // 2:
    st.session_state.paddle2_y = min(st.session_state.board_height - st.session_state.paddle_height, st.session_state.paddle2_y + 1)

grid = [["⬜" for _ in range(st.session_state.board_width)] for _ in range(st.session_state.board_height)]

for i in range(st.session_state.paddle_height):
    py1 = st.session_state.paddle1_y + i
    if 0 <= py1 < st.session_state.board_height:
        grid[py1][0] = "🟦"
    py2 = st.session_state.paddle2_y + i
    if 0 <= py2 < st.session_state.board_height:
        grid[py2][st.session_state.board_width - 1] = "🟥"

if 0 <= st.session_state.ball_y < st.session_state.board_height and 0 <= st.session_state.ball_x < st.session_state.board_width:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "⚫"

board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")
st.write(f"Score - Player: {st.session_state.score1}  Computer: {st.session_state.score2}")