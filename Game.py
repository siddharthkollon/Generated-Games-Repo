import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Refresh the app to create a game loop
st_autorefresh(interval=200, key="game_loop_ticker")

# Game dimensions
WIDTH = 20
HEIGHT = 10
PADDLE_HEIGHT = 3
LEFT_PADDLE_X = 0
RIGHT_PADDLE_X = WIDTH - 1

# ----------------------------------------------------------------------
# Session state initialization (each key separately)
# ----------------------------------------------------------------------
if "ball_x" not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "paddle_left_y" not in st.session_state:
    st.session_state.paddle_left_y = (HEIGHT - PADDLE_HEIGHT) // 2
if "paddle_right_y" not in st.session_state:
    st.session_state.paddle_right_y = (HEIGHT - PADDLE_HEIGHT) // 2
if "score_left" not in st.session_state:
    st.session_state.score_left = 0
if "score_right" not in st.session_state:
    st.session_state.score_right = 0

# ----------------------------------------------------------------------
# Physics update (runs every tick unconditionally)
# ----------------------------------------------------------------------
# Move ball
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Top / bottom wall bounce
if st.session_state.ball_y <= 0 or st.session_state.ball_y >= HEIGHT - 1:
    st.session_state.ball_dy *= -1
    # Keep ball inside bounds
    st.session_state.ball_y = max(0, min(HEIGHT - 1, st.session_state.ball_y))

# Left paddle collision
left_paddle_range = range(
    st.session_state.paddle_left_y,
    st.session_state.paddle_left_y + PADDLE_HEIGHT,
)
if (
    st.session_state.ball_dx < 0
    and st.session_state.ball_x == LEFT_PADDLE_X + 1
    and st.session_state.ball_y in left_paddle_range
):
    st.session_state.ball_dx = 1
    # Add a little vertical variation based on hit position
    offset = st.session_state.ball_y - st.session_state.paddle_left_y - PADDLE_HEIGHT // 2
    st.session_state.ball_dy = max(-1, min(1, offset))

# Right paddle collision
right_paddle_range = range(
    st.session_state.paddle_right_y,
    st.session_state.paddle_right_y + PADDLE_HEIGHT,
)
if (
    st.session_state.ball_dx > 0
    and st.session_state.ball_x == RIGHT_PADDLE_X - 1
    and st.session_state.ball_y in right_paddle_range
):
    st.session_state.ball_dx = -1
    offset = st.session_state.ball_y - st.session_state.paddle_right_y - PADDLE_HEIGHT // 2
    st.session_state.ball_dy = max(-1, min(1, offset))

# Scoring
if st.session_state.ball_x < 0:
    st.session_state.score_right += 1
    # Reset ball to center moving right
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 0, 1])
elif st.session_state.ball_x >= WIDTH:
    st.session_state.score_left += 1
    # Reset ball to center moving left
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 0, 1])

# ----------------------------------------------------------------------
# User input handling (buttons only modify paddle position)
# ----------------------------------------------------------------------
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    if st.button("⬆️", key="left_up"):
        st.session_state.paddle_left_y = max(
            0, st.session_state.paddle_left_y - 1
        )
    if st.button("⬇️", key="left_down"):
        st.session_state.paddle_left_y = min(
            HEIGHT - PADDLE_HEIGHT, st.session_state.paddle_left_y + 1
        )

with col3:
    if st.button("🔄 Restart", key="restart_game"):
        # Reset all game variables
        st.session_state.ball_x = WIDTH // 2
        st.session_state.ball_y = HEIGHT // 2
        st.session_state.ball_dx = random.choice([-1, 1])
        st.session_state.ball_dy = random.choice([-1, 0, 1])
        st.session_state.paddle_left_y = (HEIGHT - PADDLE_HEIGHT) // 2
        st.session_state.paddle_right_y = (HEIGHT - PADDLE_HEIGHT) // 2
        st.session_state.score_left = 0
        st.session_state.score_right = 0
        st.rerun()

# ----------------------------------------------------------------------
# Simple AI for right paddle (follows the ball)
# ----------------------------------------------------------------------
target_y = st.session_state.ball_y - PADDLE_HEIGHT // 2
st.session_state.paddle_right_y = max(
    0, min(HEIGHT - PADDLE_HEIGHT, target_y)
)

# ----------------------------------------------------------------------
# Render the playfield
# ----------------------------------------------------------------------
grid = [["⬜" for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Place left paddle
for i in range(PADDLE_HEIGHT):
    y = st.session_state.paddle_left_y + i
    grid[y][LEFT_PADDLE_X] = "🟦"

# Place right paddle
for i in range(PADDLE_HEIGHT):
    y = st.session_state.paddle_right_y + i
    grid[y][RIGHT_PADDLE_X] = "🟦"

# Place ball
if 0 <= st.session_state.ball_y < HEIGHT and 0 <= st.session_state.ball_x < WIDTH:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "🏓"

board_string = "\n".join("".join(row) for row in grid)

# Display board and scores
st.subheader("Ping Pong")
st.code(board_string, language="text")
st.metric(label="Player", value=st.session_state.score_left, delta=None)
st.metric(label="Computer", value=st.session_state.score_right, delta=None)