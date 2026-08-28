import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Refresh the app to create a game loop
st_autorefresh(interval=200, key="game_loop_ticker")

# ----------------------------------------------------------------------
# Session state initialization (each key separately)
# ----------------------------------------------------------------------
if "width" not in st.session_state:
    st.session_state.width = 20
if "height" not in st.session_state:
    st.session_state.height = 15
if "paddle_height" not in st.session_state:
    st.session_state.paddle_height = 3
if "paddle1_x" not in st.session_state:
    st.session_state.paddle1_x = 1
if "paddle2_x" not in st.session_state:
    st.session_state.paddle2_x = st.session_state.width - 2
if "ball_x" not in st.session_state:
    st.session_state.ball_x = st.session_state.width // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = st.session_state.height // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 1])
if "paddle1_y" not in st.session_state:
    st.session_state.paddle1_y = st.session_state.height // 2 - st.session_state.paddle_height // 2
if "paddle2_y" not in st.session_state:
    st.session_state.paddle2_y = st.session_state.height // 2 - st.session_state.paddle_height // 2
if "score1" not in st.session_state:
    st.session_state.score1 = 0
if "score2" not in st.session_state:
    st.session_state.score2 = 0

# ----------------------------------------------------------------------
# Game physics – runs on every refresh unconditionally
# ----------------------------------------------------------------------
# Move ball
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Vertical wall collision
if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.height - 1:
    st.session_state.ball_dy *= -1
    # Keep ball inside bounds
    st.session_state.ball_y = max(0, min(st.session_state.height - 1, st.session_state.ball_y))

# Left paddle collision
if (
    st.session_state.ball_dx < 0
    and st.session_state.ball_x == st.session_state.paddle1_x + 1
    and st.session_state.paddle1_y
    <= st.session_state.ball_y
    <= st.session_state.paddle1_y + st.session_state.paddle_height - 1
):
    st.session_state.ball_dx *= -1

# Right paddle collision
if (
    st.session_state.ball_dx > 0
    and st.session_state.ball_x == st.session_state.paddle2_x - 1
    and st.session_state.paddle2_y
    <= st.session_state.ball_y
    <= st.session_state.paddle2_y + st.session_state.paddle_height - 1
):
    st.session_state.ball_dx *= -1

# Scoring
if st.session_state.ball_x < 0:
    st.session_state.score2 += 1
    # Reset ball
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
elif st.session_state.ball_x >= st.session_state.width:
    st.session_state.score1 += 1
    # Reset ball
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])

# Simple AI for right paddle – follows the ball slowly
if st.session_state.ball_y > st.session_state.paddle2_y + st.session_state.paddle_height // 2:
    st.session_state.paddle2_y = min(
        st.session_state.height - st.session_state.paddle_height,
        st.session_state.paddle2_y + 1,
    )
elif st.session_state.ball_y < st.session_state.paddle2_y + st.session_state.paddle_height // 2:
    st.session_state.paddle2_y = max(0, st.session_state.paddle2_y - 1)

# ----------------------------------------------------------------------
# UI – display scores and board
# ----------------------------------------------------------------------
st.title("🏓 Streamlit Ping Pong")
col1, col2 = st.columns([1, 1])
col1.metric("Player ⬛", st.session_state.score1, delta=None)
col2.metric("Player 🟥", st.session_state.score2, delta=None)

# Build empty board
grid = [["⬜" for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]

# Insert left paddle
for i in range(st.session_state.paddle_height):
    y = st.session_state.paddle1_y + i
    if 0 <= y < st.session_state.height:
        grid[y][st.session_state.paddle1_x] = "🟦"

# Insert right paddle
for i in range(st.session_state.paddle_height):
    y = st.session_state.paddle2_y + i
    if 0 <= y < st.session_state.height:
        grid[y][st.session_state.paddle2_x] = "🟥"

# Insert ball
i