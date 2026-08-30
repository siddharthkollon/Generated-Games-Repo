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
if 'paddle_y' not in st.session_state:
    st.session_state.paddle_y = (st.session_state.height - st.session_state.paddle_height)//2
if 'ai_paddle_y' not in st.session_state:
    st.session_state.ai_paddle_y = (st.session_state.height - st.session_state.paddle_height)//2
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = st.session_state.width // 2
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = st.session_state.height // 2
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 1])
if 'score_left' not in st.session_state:
    st.session_state.score_left = 0
if 'score_right' not in st.session_state:
    st.session_state.score_right = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
ball_x = st.session_state.ball_x + st.session_state.ball_dx
ball_y = st.session_state.ball_y + st.session_state.ball_dy
if ball_y <= 0 or ball_y >= st.session_state.height - 1:
    st.session_state.ball_dy *= -1
    ball_y = st.session_state.ball_y + st.session_state.ball_dy
if ball_x == 2 and st.session_state.ball_dx < 0:
    if st.session_state.paddle_y <= ball_y < st.session_state.paddle_y + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        ball_x = st.session_state.ball_x + st.session_state.ball_dx
if ball_x == st.session_state.width - 3 and st.session_state.ball_dx > 0:
    if st.session_state.ai_paddle_y <= ball_y < st.session_state.ai_paddle_y + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        ball_x = st.session_state.ball_x + st.session_state.ball_dx
if ball_y > st.session_state.ai_paddle_y + st.session_state.paddle_height // 2 and st.session_state.ai_paddle_y < st.session_state.height - st.session_state.paddle_height:
    st.session_state.ai_paddle_y += 1
elif ball_y < st.session_state.ai_paddle_y + st.session_state.paddle_height // 2 and st.session_state.ai_paddle_y > 0:
    st.session_state.ai_paddle_y -= 1
if ball_x < 0:
    st.session_state.score_right += 1
    ball_x = st.session_state.width // 2
    ball_y = st.session_state.height // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 1])
elif ball_x >= st.session_state.width:
    st.session_state.score_left += 1
    if st.session_state.score_left > st.session_state.high_score:
        st.session_state.high_score = st.session_state.score_left
    ball_x = st.session_state.width // 2
    ball_y = st.session_state.height // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 1])
st.session_state.ball_x = ball_x
st.session_state.ball_y = ball_y
if st.button("⬆️ Up", key="up_btn"):
    st.session_state.paddle_y = max(0, st.session_state.paddle_y - 1)
if st.button("⬇️ Down", key="down_btn"):
    st.session_state.paddle_y = min(st.session_state.height - st.session_state.paddle_height, st.session_state.paddle_y + 1)
if st.button("🔄 Restart", key="restart_btn"):
    st.session_state.score_left = 0
    st.session_state.score_right = 0
    st.session_state.paddle_y = (st.session_state.height - st.session_state.paddle_height)//2
    st.session_state.ai_paddle_y = (st.session_state.height - st.session_state.paddle_height)//2
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
    st.rerun()
grid = [[" " for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
for i in range(st.session_state.paddle_height):
    grid[st.session_state.paddle_y + i]