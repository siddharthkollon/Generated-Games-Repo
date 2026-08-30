import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
WIDTH = 20
HEIGHT = 12
PADDLE_SIZE = 3
WIN_SCORE = 5
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if 'paddle_y' not in st.session_state:
    st.session_state.paddle_y = (HEIGHT - PADDLE_SIZE) // 2
if 'ai_y' not in s