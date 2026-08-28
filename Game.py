import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Refresh the app every 200 ms
st_autorefresh(interval=200, key="game_loop_ticker")

# ---------- Session State Initialization ----------
if "width" not in st.session_state:
    st.session_state.width = 20  # columns

if "height" not in st.session_state:
    st.session_state.height = 12  # rows

if "paddle_height" not in st.session_state:
    st.session_state.paddle_height = 3

if "paddle1_y" not in st.session_state:
    st.session_state.paddle1_y = (st.session_state.height -
                                  st.session_state.paddle_height) // 2

if "paddle2_y" not in st.session_state:
    st.session_state.paddle2_y = (st.session_state.height -
                                  st.session_state.paddle_height) // 2

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

if "paddle1_dir" not in st.session_state:
    st.session_state.paddle1_dir = 0  # -1 up, 1 down, 0 none

# ---------- User Input ----------
if st.button("⬆️ Up", key="up_btn"):
    st.session_state.paddle1_dir = -1

if st.button("⬇️ Down", key="down_btn"):
    st.session_state.paddle1_dir = 1

if st.button("🔄 Restart Game", key="restart_btn"):
    st.session_state.score_left = 0
    st.session_state.score_right = 0
    st.session_state.paddle1_y = (st.session_state.height -
                                  st.session_state.paddle_height) // 2
    st.session_state.paddle2_y = (st.session_state.height -
                                  st.session_state.paddle_height) // 2
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.paddle1_dir = 0
    st.rerun()

# ---------- Game Logic (runs every tick) ----------
# Move left paddle according to last input
if st.session_state.paddle1_dir != 0:
    new_y = st.session_state.paddle1_y + st.session_state.paddle1_dir
    st.session_state.paddle1_y = max(
        0,
        min(st.session_state.height - st.session_state.paddle_height, new_y)
    )
    st.session_state.paddle1_dir = 0  # reset direction

# Simple AI for right paddle
if st.session_state.ball_y > st.session_state.paddle2_y + st.session_state.paddle_height // 2:
    ai_move = 1
elif st.session_state.ball_y < st.session_state.paddle2_y + st.session_state.paddle_height // 2:
    ai_move = -1
else:
    ai_move = 0

if ai_move != 0:
    new_y2 = st.session_state.paddle2_y + ai_move
    st.session_state.paddle2_y = max(
        0,
        min(st.session_state.height - st.session_state.paddle_height, new_y2)
    )

# Move ball
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Collision with top/bottom walls
if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.height - 1:
    st.session_state.ball_dy *= -1
    # Keep ball inside bounds
    st.session_state.ball_y = max(0, min(st.session_state.height - 1, st.session_state.ball_y))

# Collision with left paddle
if st.session_state.ball_dx < 0 and st.session_state.ball_x == 1:
    py = st.session_state.paddle1_y
    if py <= st.session_state.ball_y < py + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        # Add a slight vertical variation based on hit position
        offset = st.session_state.ball_y - (py + st.session_state.paddle_height // 2)
        if offset != 0:
            st.session_state.ball_dy = offset // abs(offset)

# Collision with right paddle
if st.session_state.ball_dx > 0 and st.session_state.ball_x == st.session_state.width - 2:
    py = st.session_state.paddle2_y
    if py <= st.session_state.ball_y < py + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        offset = st.session_state.ball_y - (py + st.session_state.paddle_height // 2)
        if offset != 0:
            st.session_state.ball_dy = offset // abs(offset)

# Scoring
if st.session_state.ball_x < 0:
    st.session_state.score_right += 1
    # Reset ball to center heading right
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 0, 1])

if st.session_state.ball_x >= st.session_state.width:
    st.session_state.score_left += 1
    # Reset ball to center heading left
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 0, 1])

# ---------- Rendering ----------
st.title("🏓 Streamlit Ping Pong")

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.metric("Left Score", st.session_state.score_left)
with col3:
    st.metric("Right Scor