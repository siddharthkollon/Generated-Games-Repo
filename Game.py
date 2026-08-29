import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# ----------------------------------------------------------------------
# Auto‑refresh ticker – first line of execution
# ----------------------------------------------------------------------
st_autorefresh(interval=200, key="game_loop_ticker")

# ----------------------------------------------------------------------
# Session state initialization (one block per key)
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# Physics – runs on every tick before UI handling
# ----------------------------------------------------------------------
# Move ball
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Bounce off top / bottom walls
if st.session_state.ball_y <= 0:
    st.session_state.ball_y = 0
    st.session_state.ball_dy *= -1
elif st.session_state.ball_y >= st.session_state.grid_height - 1:
    st.session_state.ball_y = st.session_state.grid_height - 1
    st.session_state.ball_dy *= -1

# Paddle X positions (fixed)
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

# Scoring and ball reset
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

# ----------------------------------------------------------------------
# User controls – only modify simple state variables
# ----------------------------------------------------------------------
col_left, col_mid, col_right = st.columns([1, 2, 1])

with col_left:
    if st.button("⬆️", key="left_up"):
        st.session_state.paddle_left_y = max(
            0, st.session_state.paddle_left_y - 1
        )
    if st.button("⬇️", key="left_down"):
        st.session_state.paddle_left_y = min(
            st.session_state.grid_height - st.session_state.paddle_size,
            st.session_state.paddle_left_y + 1,
        )

with col_mid:
    st.metric("Left Player", st.session_state.score_left, key="metric_left")
    st.metric("Right Player", st.session_state.score_right, key="metric_right")
    if st.button("Restart Game", key="restart_btn"):
        st.session_state.score_left = 0
        st.session_state.score_right = 0
        st.session_state.ball_x = st.session_state.grid_width // 2
        st.session_state.ball_y = st.session_state.grid_height // 2
        st.session_state.ball_dx = random.choice([-1, 1])
        st.session_state.ball_dy = random.choice([-1, 0, 1])
        st.session_state.paddle_left_y = (st.session_state.grid_height - st.session_state.paddle_size) // 2
        st.session_state.paddle_right_y = (st.session_state.grid_height - st.session_state.paddle_size) // 2
        st.rerun()

with col_right:
    if st.button("⬆️", key="right_up"):
        st.session_state.paddle_right_y = max(
            0, st.session_state.paddle_right_y - 1
        )
    if st.button("⬇️", key="right_down"):
        st.session_state.paddle_right_y = min(
            st.session_state.grid_height - st.session_state.paddle_size,
            st.session_state.paddle_right_y + 1,
        )

# ----------------------------------------------------------------------
# Render playfield
# ----------------------------------------------------------------------
# Base empty grid
grid = [["⬜" for _ in range(st.session_state.grid_width)] for _ in range(st.session_state.grid_height)]

# Left paddle (🟦)
for i in range(st.session_state.paddle_size):
    y = st.session_state.paddle_left_y + i
    if 0 <= y < st.session_state.grid_height:
        grid[y][left_paddle_x] = "🟦"

# Right paddle (🟥)
for i in range(st.session_state.paddle_size):
    y = st.session_state.paddle_right_y + i
    if 0 <= y < st.session_state.grid_height:
        grid[y][right_paddle_x] = "🟥"

# Ball (🏓)
if (
    0 <= st.session_state.ball_y < st.session_state.grid_height
    and 0 <= st.session_state.ball_x < st.session_state.grid_width
):
    grid[st.session_state.ball_y][st.session_state.ball_x] = "🏓"

# Convert to string for display
board_str = "\n".join("".join(row) for row in grid)
st.code(board_str, language="text")