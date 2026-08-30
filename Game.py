import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
WIDTH = 20
HEIGHT = 15
PADDLE_HEIGHT = 3
if "ball_x" not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 1])
if "paddle_left_y" not in st.session_state:
    st.session_state.paddle_left_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
if "paddle_right_y" not in st.session_state:
    st.session_state.paddle_right_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
if "score_left" not in st.session_state:
    st.session_state.score_left = 0
if "score_right" not in st.session_state:
    st.session_state.score_right = 0
if st.button("Restart Game", key="restart_btn"):
    st.session_state.ball_x = WIDTH // 2
    st.session_state.ball_y = HEIGHT // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
    st.session_state.paddle_left_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    st.session_state.paddle_right_y = HEIGHT // 2 - PADDLE_HEIGHT // 2
    st.session_state.score_left = 0
    st.session_state.score_right = 0
    st.rerun()
new_ball_x = st.session_state.ball_x + st.session_state.ball_dx
new_ball_y = st.session_state.ball_y + st.session_state.ball_dy
if new_ball_y <= 0 or new_ball_y >= HEIGHT - 1:
    st.session_state.ball_dy *= -1
    new_ball_y = st.session_state.ball_y + st.session_state.ball_dy
if new_ball_x < 0:
    st.session_state.score_right += 1
    new_ball_x = WIDTH // 2
    new_ball_y = HEIGHT // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
elif new_ball_x >= WIDTH:
    st.session_state.score_left += 1
    new_ball_x = WIDTH // 2
    new_ball_y = HEIGHT // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
else:
    if new_ball_x == 1 and st.session_state.paddle_left_y <= new_ball_y < st.session_state.paddle_left_y + PADDLE_HEIGHT:
        st.session_state.ball_dx = 1
        new_ball_x = st.session_state.ball_x + st.session_state.ball_dx
    if new_ball_x == WIDTH - 2 and st.session_state.paddle_right_y <= new_ball_y < st.session_state.paddle_right_y + PADDLE_HEIGHT:
        st.session_state.ball_dx = -1
        new_ball_x = st.session_state.ball_x + st.session_state.ball_dx
st.session_state.ball_x = new_ball_x
st.session_state.ball_y = new_ball_y
if st.button("Up", key="up_btn"):
    st.session_state.paddle_move