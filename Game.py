import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
ROWS = 15
COLS = 30
PADDLE_SIZE = 4
if 'ball_x' not in st.session_state:
    st.session_state.ball_x = COLS // 2
if 'ball_y' not in st.session_state:
    st.session_state.ball_y = ROWS // 2
if 'ball_dx' not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if 'ball_dy' not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 1])
if 'paddle_left_y' not in st.session_state:
    st.session_state.paddle_left_y = ROWS // 2 - PADDLE_SIZE // 2
if 'paddle_right_y' not in st.session_state:
    st.session_state.paddle_right_y = ROWS // 2 - PADDLE_SIZE // 2
if 'score_left' not in st.session_state:
    st.session_state.score_left = 0
if 'score_right' not in st.session_state:
    st.session_state.score_right = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if not st.session_state.game_over:
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= ROWS - 1:
        st.session_state.ball_dy *= -1
        st.session_state.ball_y = max(0, min(ROWS - 1, st.session_state.ball_y))
    if st.session_state.ball_x == 1:
        left_range = range(st.session_state.paddle_left_y, st.session_state.paddle_left_y + PADDLE_SIZE)
        if st.session_state.ball_y in left_range:
            st.session_state.ball_dx = 1
        else:
            st.session_state.score_right += 1
            st.session_state.game_over = True
    if st.session_state.ball_x == COLS - 2:
        right_range = range(st.session_state.paddle_right_y, st.session_state.paddle_right_y + PADDLE_SIZE)
        if st.session_state.ball_y in right_range:
            st.session_state.ball_dx = -1
        else:
            st.session_state.score_left += 1
            st.session_state.game_over = True
    if st.session_state.ball_y > st.session_state.paddle_right_y + PADDLE_SIZE // 2 and st.session_state.paddle_right_y + PADDLE_SIZE < ROWS:
        st.session_state.paddle_right_y += 1
    elif st.session_state.ball_y < st.session_state.paddle_right_y + PADDLE_SIZE // 2 and st.session_state.paddle_right_y > 0:
        st.session_state.paddle_right_y -= 1
if st.button("⬆️", key="btn_up"):
    st.session_state.paddle_left_y = max(0, st.session_state.paddle_left_y - 1)
if st.button("⬇️", key="btn_down"):
    st.session_state.paddle_left_y = min(ROWS - PADDLE_SIZE, st.session_state.paddle_left_y + 1)
if st.button("Restart", key="btn_restart"):
    st.session_state.ball_x = COLS // 2
    st.session_state.ball_y = ROWS // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
    st.session_state.paddle_left_y = ROWS // 2 - PADDLE_SIZE // 2
    st.session_state.paddle_right_y = ROWS // 2 - PADDLE_SIZE // 2
    st.session_state.score_left = 0
    st.session_state.score_right = 0
    st.session_state.game_over = False
    st.rerun()
st.subheader(f"Score  Left: {st.session_state.score_left}  |  Right: {st.session_state.score_right}")
grid = [["⬜" for _ in range(COLS)] for _ in range(ROWS)]
for i in range(PADDLE_SIZE):
    y_left = st.session_state.paddle_left_y + i
    if 0 <= y_left < ROWS:
        grid[y_left][0] = "🟦"