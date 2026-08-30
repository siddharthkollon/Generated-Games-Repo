import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=150, key="game_loop_ticker")

WIDTH = 20
HEIGHT = 15
PADDLE_SIZE = 3
LEFT_X = 1
RIGHT_X = WIDTH - 2

if "ball_x" not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "paddle_left_y" not in st.session_state:
    st.session_state.paddle_left_y = HEIGHT // 2 - PADDLE_SIZE // 2
if "paddle_right_y" not in st.session_state:
    st.session_state.paddle_right_y = HEIGHT // 2 - PADDLE_SIZE // 2
if "score_left" not in st.session_state:
    st.session_state.score_left = 0
if "score_right" not in st.session_state:
    st.session_state.score_right = 0

# Move ball
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Top/bottom collision
if st.session_state.ball_y <= 0 or st.session_state.ball_y >= HEIGHT - 1:
    st.session_state.ball_dy *= -1

# Left paddle collision
if st.session_state.ball_dx < 0 and st.session_state.ball_x == LEFT_X + 1:
    if st.session_state.paddle_left_y <= st.session_state.ball_y < st.session_state.paddle_left_y + PADDLE_SIZE:
        st.session_state.ball_dx *= -1
        st.session_state.ball_dy = random.choice([-1, 0, 1])

# Right paddle collision
if st.session_state.ball_dx > 0 and st.session_state.ball_x == RIGHT_X - 1:
    if st.session_state.paddle_right_y <= st.session_state.ball_y < st.session_state.paddle_right_y + PADDLE_SIZE:
        st.session_state.ball_dx *= -1
        st.session_state.ball_dy = random.choice([-1, 0, 1])

# Scoring
if st.session_state.ball_x < 0:
    st.session_state.score_right += 1
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if st.session_state.ball_x >= WIDTH:
    st.session_state.score_left += 1
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 0, 1])

# Player input
if st.button("⬆️", key="up_btn"):
    st.session_state.paddle_left_y = max(0, st.session_state.paddle_left_y - 1)
if st.button("⬇️", key="down_btn"):
    st.session_state.paddle_left_y = min(HEIGHT - PADDLE_SIZE, st.session_state.paddle_left_y + 1)

# Simple AI for right paddle
if st.session_state.ball_y > st.session_state.paddle_right_y + PADDLE_SIZE // 2:
    st.session_state.paddle_right_y = min(HEIGHT - PADDLE_SIZE, st.session_state.paddle_right_y + 1)
elif st.session_state.ball_y < st.session_state.paddle_right_y + PADDLE_SIZE // 2:
    st.session_state.paddle_right_y = max(0, st.session_state.paddle_right_y - 1)

# Build grid
grid = [["⬜" for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Insert left paddle
for i in range(PADDLE_SIZE):
    y = st.session_state.paddle_left_y + i
    if 0 <= y < HEIGHT:
        grid[y][LEFT_X] = "🟦"

# Insert right paddle
for i in range(PADDLE_SIZE):
    y = st.session_state.paddle_right_y + i
    if 0 <= y < HEIGHT:
        grid[y][RIGHT_X] = "🟦"

# Insert ball
if 0 <= st.session_state.ball_y < HEIGHT and 0 <= st.session_state.ball_x < WIDTH:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "⚪"

board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")

st.write(f"**Score**   Player: {st.session_state.score_left}   Computer: {st.session_state.score_right}")

if st.button("Restart Game", key="restart_btn"):
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.paddle_left_y = HEIGHT // 2 - PADDLE_SIZE // 2
    st.session_state.paddle_right_y = HEIGHT // 2 - PADDLE_SIZE // 2
    st.session_state.score_left = 0
    st.session_state.score_right = 0
    st.rerun()