import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

if 'width' not in st.session_state:
    st.session_state.width = 20
if 'height' not in st.session_state:
    st.session_state.height = 10
if 'paddle_height' not in st.session_state:
    st.session_state.paddle_height = 3
if 'paddle1_y' not in st.session_state:
    st.session_state.paddle1_y = (st.session_state.height - st.session_state.paddle_height) // 2
if 'paddle2_y' not in st.session_state:
    st.session_state.paddle2_y = (st.session_state.height - st.session_state.paddle_height) // 2
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = st.session_state.width // 2
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = st.session_state.height // 2
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if 'score1' not in st.session_state:
    st.session_state.score1 = 0
if 'score2' not in st.session_state:
    st.session_state.score2 = 0
if 'move_dir' not in st.session_state:
    st.session_state.move_dir = 0

if st.button("⬆️", key="up_btn"):
    st.session_state.move_dir = -1
if st.button("⬇️", key="down_btn"):
    st.session_state.move_dir = 1
if st.button("🔄 Restart", key="restart_btn"):
    st.session_state.paddle1_y = (st.session_state.height - st.session_state.paddle_height) // 2
    st.session_state.paddle2_y = (st.session_state.height - st.session_state.paddle_height) // 2
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.score1 = 0
    st.session_state.score2 = 0
    st.session_state.move_dir = 0
    st.rerun()

new_p1 = st.session_state.paddle1_y + st.session_state.move_dir
st.session_state.paddle1_y = max(0, min(st.session_state.height - st.session_state.paddle_height, new_p1))
st.session_state.move_dir = 0

center_ai = st.session_state.paddle2_y + st.session_state.paddle_height // 2
if center_ai < st.session_state.ball_y:
    st.session_state.paddle2_y = min(st.session_state.height - st.session_state.paddle_height, st.session_state.paddle2_y + 1)
elif center_ai > st.session_state.ball_y:
    st.session_state.paddle2_y = max(0, st.session_state.paddle2_y - 1)

st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.height - 1:
    st.session_state.ball_dy *= -1

if st.session_state.ball_dx < 0 and st.session_state.ball_x == 1:
    if st.session_state.paddle1_y <= st.session_state.ball_y < st.session_state.paddle1_y + st.session_state.paddle_height:
        st.session_state.ball_dx = 1
        st.session_state.ball_dy = random.choice([-1, 0, 1])
if st.session_state.ball_dx > 0 and st.session_state.ball_x == st.session_state.width - 2:
    if st.session_state.paddle2_y <= st.session_state.ball_y < st.session_state.paddle2_y + st.session_state.paddle_height:
        st.session_state.ball_dx = -1
        st.session_state.ball_dy = random.choice([-1, 0, 1])

if st.session_state.ball_x < 0:
    st.session_state.score2 += 1
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if st.session_state.ball_x >= st.session_state.width:
    st.session_state.score1 += 1
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 0, 1])

grid = [["⬜" for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
for i in range(st.session_state.paddle_height):
    grid[st.session_state.paddle1_y + i][0] = "🟦"
    grid[st.session_state.paddle2_y + i][st.session_state.width - 1] = "🟦"
if 0 <= st.session_state.ball_y < st.session_state.height and 0 <= st.session_state.ball_x < st.session_state.width:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "⚪"
board = "\n".join("".join(row) for row in grid)

st.markdown(f"**Player 1:** {st.session_state.score1}  **Player 2:** {st.session_state.score2}")
st.code(board, language="text")