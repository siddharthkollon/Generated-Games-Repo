import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Refresh the app every 200 ms
st_autorefresh(interval=200, key="game_loop_ticker")

# ---------- State Initialization ----------
if "grid_width" not in st.session_state:
    st.session_state.grid_width = 40
if "grid_height" not in st.session_state:
    st.session_state.grid_height = 20
if "paddle_size" not in st.session_state:
    st.session_state.paddle_size = 4

if "ball_x" not in st.session_state:
    st.session_state.ball_x = st.session_state.grid_width // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = st.session_state.grid_height // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])

if "paddle_left_y" not in st.session_state:
    st.session_state.paddle_left_y = (st.session_state.grid_height - st.session_state.paddle_size) // 2
if "paddle_right_y" not in st.session_state:
    st.session_state.paddle_right_y = (st.session_state.grid_height - st.session_state.paddle_size) // 2

if "score_left" not in st.session_state:
    st.session_state.score_left = 0
if "score_right" not in st.session_state:
    st.session_state.score_right = 0

# ---------- Physics (runs every tick) ----------
# Move ball
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Bounce off top/bottom walls
if st.session_state.ball_y <= 0:
    st.session_state.ball_y = 0
    st.session_state.ball_dy *= -1
elif st.session_state.ball_y >= st.session_state.grid_height - 1:
    st.session_state.ball_y = st.session_state.grid_height - 1
    st.session_state.ball_dy *= -1

# Paddle positions
left_paddle_x = 1
right_paddle_x = st.session_state.grid_width - 2

# Collision with left paddle
if (
    st.session_state.ball_dx < 0
    and st.session_state.ball_x == left_paddle_x + 1
    and st.session_state.paddle_left_y
    <= st.session_state.ball_y
    < st.session_state.paddle_left_y + st.session_state.paddle_size
):
    st.session_state.ball_dx *= -1
    offset = st.session_state.ball_y - st.session_state.paddle_left_y
    if offset == 0:
        st.session_state.ball_dy = -1
    elif offset == st.session_state.paddle_size - 1:
        st.session_state.ball_dy = 1
    else:
        st.session_state.ball_dy = 0

# Collision with right paddle
if (
    st.session_state.ball_dx > 0
    and st.session_state.ball_x == right_paddle_x - 1
    and st.session_state.paddle_right_y
    <= st.session_state.ball_y
    < st.session_state.paddle_right_y + st.session_state.paddle_size
):
    st.session_state.ball_dx *= -1
    offset = st.session_state.ball_y - st.session_state.paddle_right_y
    if offset == 0:
        st.session_state.ball_dy = -1
    elif offset == st.session_state.paddle_size - 1:
        st.session_state.ball_dy = 1
    else:
        st.session_state.ball_dy = 0

# Scoring
if st.session_state.ball_x < 0:
    st.session_state.score_right += 1
    st.session_state.ball_x = st.session_state.grid_width // 2
    st.session_state.ball_y = st.session_state.grid_height // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 0, 1])
elif st.session_state.ball_x >= st.session_state.grid_width:
    st.session_state.score_left += 1
    st.session_state.ball_x = st.session_state.grid_width // 2
    st.session_state.ball_y = st.session_state.grid_height // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 0, 1])

# Simpl