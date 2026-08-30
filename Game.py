import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

WIDTH = 20
HEIGHT = 15
PADDLE_SIZE = 4
EMPTY_EMOJI = "⬛"
PADDLE_EMOJI = "🟦"
BALL_EMOJI = "⚪"
SPEED_FACTOR = 2

if "ball_x" not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "paddle1_y" not in st.session_state:
    st.session_state.paddle1_y = (HEIGHT - PADDLE_SIZE) // 2
if "paddle2_y" not in st.session_state:
    st.session_state.paddle2_y = (HEIGHT - PADDLE_SIZE) // 2
if "score1" not in st.session_state:
    st.session_state.score1 = 0
if "score2" not in st.session_state:
    st.session_state.score2 = 0
if "p1_move" not in st.session_state:
    st.session_state.p1_move = 0
if "p2_move" not in st.session_state:
    st.session_state.p2_move = 0
if "tick" not in st.session_state:
    st.session_state.tick = 0

def reset_ball():
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])

st.session_state.tick += 1

if st.session_state.tick % SPEED_FACTOR == 0:
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= HEIGHT - 1:
        st.session_state.ball_dy *= -1
    if st.session_state.ball_x == 1:
        if st.session_state.paddle1_y <= st.session_state.ball_y < st.session_state.paddle1_y + PADDLE_SIZE:
            st.session_state.ball_dx *= -1
    if st.session_state.ball_x == WIDTH - 2:
        if st.session_state.paddle2_y <= st.session_state.ball_y < st.session_state.paddle2_y + PADDLE_SIZE:
            st.session_state.ball_dx *= -1
    if st.session_state.ball_x < 0:
        st.session_state.score2 += 1
        reset_ball()
    if st.session_state.ball_x >= WIDTH:
        st.session_state.score1 += 1
        reset_ball()

new_p1_y = st.session_state.paddle1_y + st.session_state.p1_move
st.session_state.paddle1_y = max(0, min(HEIGHT - PADDLE_SIZE, new_p1_y))
new_p2_y = st.session_state.paddle2_y + st.session_state.p2_move
st.session_state.paddle2_y = max(0, min(HEIGHT - PADDLE_SIZE, new_p2_y))
st.session_state.p1_move = 0
st.session_state.p2_move = 0

if st.button("↑ P1", key="p1_up"):
    st.session_state.p1_move = -1
if st.button("↓ P1", key="p1_down"):
    st.session_state.p1_move = 1
if st.button("↑ P2", key="p2_up"):
    st.session_state.p2_move = -1
if st.button("↓ P2", key="p2_down"):
    st.session_state.p2_move = 1
if st.button("Restart Game", key="restart"):
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.paddle1_y = (HEIGHT - PADDLE_SIZE) // 2
    st.session_state.paddle2_y = (HEIGHT - PADDLE_SIZE) // 2
    st.session_state.score1 = 0
    st.session_state.score2 = 0
    st.session_state.tick = 0
    st.rerun()

grid = [[EMPTY_EMOJI for _ in range(WIDTH)] for _ in range(HEIGHT)]
for i in range(PADDLE_SIZE):
    grid[st.session_state.paddle1_y + i][0] = PADDLE_EMOJI
    grid[st.session_state.paddle2_y + i][WIDTH - 1] = PADDLE_EMOJI
if 0 <= st.session_state.ball_y < HEIGHT and 0 <= st.session_state.ball_x < WIDTH:
    grid[st.session_state.ball_y][st.session_state.ball_x] = BALL_EMOJI
board = "\n".join("".join(row) for row in grid)
st.code(board, language="text")
st.write(f"Score — Player 1: {st.session_state.score1} | Player 2: {st.session_state.score2}")