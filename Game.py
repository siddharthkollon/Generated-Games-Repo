import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = 15
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = 7
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = 1
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = 1
if 'paddle_left_y' not in st.session_state:
    st.session_state.paddle_left_y = 6
if 'paddle_right_y' not in st.session_state:
    st.session_state.paddle_right_y = 6
if 'score_left' not in st.session_state:
    st.session_state.score_left = 0
if 'score_right' not in st.session_state:
    st.session_state.score_right = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = ""
width = 30
height = 15
paddle_size = 4
if not st.session_state.game_over:
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= height - 1:
        st.session_state.ball_dy *= -1
    if st.session_state.ball_x <= 1:
        if st.session_state.paddle_left_y <= st.session_state.ball_y < st.session_state.paddle_left_y + paddle_size:
            st.session_state.ball_dx *= -1
            st.session_state.ball_x = 1
        else:
            st.session_state.score_right += 1
            st.session_state.ball_x = width // 2
            st.session_state.ball_y = height // 2
            st.session_state.ball_dx = 1
            st.session_state.ball_dy = random.choice([-1, 1])
    if st.session_state.ball_x >= width - 2:
        if st.session_state.paddle_right_y <= st.session_state.ball_y < st.session_state.paddle_right_y + paddle_size:
            st.session_state.ball_dx *= -1
            st.session_state.ball_x = width - 2
        else:
            st.session_state.score_left += 1
            st.session_state.ball_x = width // 2
            st.session_state.ball_y = height // 2
            st.session_state.ball_dx = -1
            st.session_state.ball_dy = random.choice([-1, 1])
    if st.session_state.score_left >= 5:
        st.session_state.game_over = True
        st.session_state.winner = "Left Player"
    if st.session_state.score_right >= 5:
        st.session_state.game_over = True
        st.session_state.winner = "Right Player"
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    if st.button("Up Left", key="up_left"):
        st.session_state.paddle_left_y = max(0, st.session_state.paddle_left_y - 1)
    if st.button("Down Left", key="down_left"):
        st.session_state.paddle_left_y = min(height - paddle_size, st.session_state.paddle_left_y + 1)
with col3:
    if st.button("Up Right", key="up_right"):
        st.session_state.paddle_right_y = max(0, st.session_state.paddle_right_y - 1)
    if st.button("Down Right", key="down_right"):
        st.session_state.paddle_right_y = min(height - paddle_size, st.session_state.paddle_right_y + 1)
grid = [[" " for _ in range(width)] for _ in range(height)]
for y in range(height):
    grid[y][0] = "│"
    grid[y][width - 1] = "│"
for x in range(width):
    grid[0][x] = "─"
    grid[height - 1][x] =