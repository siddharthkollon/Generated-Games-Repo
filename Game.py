import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

if 'height' not in st.session_state:
    st.session_state.height = 15
if 'width' not in st.session_state:
    st.session_state.width = 30
if 'paddle_height' not in st.session_state:
    st.session_state.paddle_height = 3
if 'left_paddle_y' not in st.session_state:
    st.session_state.left_paddle_y = (st.session_state.height - st.session_state.paddle_height) // 2
if 'right_paddle_y' not in st.session_state:
    st.session_state.right_paddle_y = (st.session_state.height - st.session_state.paddle_height) // 2
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = st.session_state.width // 2
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = st.session_state.height // 2
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if 'left_score' not in st.session_state:
    st.session_state.left_score = 0
if 'right_score' not in st.session_state:
    st.session_state.right_score = 0
if 'left_move' not in st.session_state:
    st.session_state.left_move = 0

if st.button("⬆️", key="left_up"):
    st.session_state.left_move = -1
if st.button("⬇️", key="left_down"):
    st.session_state.left_move = 1
if st.button("Restart", key="restart"):
    st.session_state.left_score = 0
    st.session_state.right_score = 0
    st.session_state.left_paddle_y = (st.session_state.height - st.session_state.paddle_height) // 2
    st.session_state.right_paddle_y = (st.session_state.height - st.session_state.paddle_height) // 2
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.left_move = 0
    st.rerun()

new_left_y = st.session_state.left_paddle_y + st.session_state.left_move
new_left_y = max(0, min(st.session_state.height - st.session_state.paddle_height, new_left_y))
st.session_state.left_paddle_y = new_left_y
st.session_state.left_move = 0

if st.session_state.ball_y < st.session_state.right_paddle_y:
    st.session_state.right_paddle_y = max(0, st.session_state.right_paddle_y - 1)
elif st.session_state.ball_y > st.session_state.right_paddle_y + st.session_state.paddle_height - 1:
    st.session_state.right_paddle_y = min(st.session_state.height - st.session_state.paddle_height, st.session_state.right_paddle_y + 1)

st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.height - 1:
    st.session_state.ball_dy *= -1

if st.session_state.ball_dx < 0 and st.session_state.ball_x == 2:
    if st.session_state.lef