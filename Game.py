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
    st.session_state.paddle1_y = (st.session_state.height - st.session_state.paddle_height)//2
if 'paddle2_y' not in st.session_state:
    st.session_state.paddle2_y = (st.session_state.height - st.session_state.paddle_height)//2
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
if 'paddle_move' not in st.session_state:
    st.session_state.paddle_move = 0

if st.button("Up", key="up_btn"):
    st.session_state.paddle_move = -1
if st.button("Down", key="down_btn"):
    st.session_state.paddle_move = 1

new_p1 = st.session_state.paddle1_y + st.session_state.paddle_move
st.session_state.paddle1_y = max(0, min(st.session_state.height - st.session_state.paddle_height, new_p1))
st.session_state.paddle_move = 0

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
    if st.session_state.paddle1_y <= st.session_state.ball_