import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

if "board_width" not in st.session_state:
    st.session_state.board_width = 20
if "board_height" not in st.session_state:
    st.session_state.board_height = 15
if "paddle_height" not in st.session_state:
    st.session_state.paddle_height = 3
if "ball_x" not in st.session_state:
    st.session_state.ball_x = st.session_state.board_width // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = st.session_state.board_height // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 1])
if "paddle_y" not in st.session_state:
    st.session_state.paddle_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
if "ai_paddle_y" not in st.session_state:
    st.session_state.ai_paddle_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
if "score_player" not in st.session_state:
    st.session_state.score_player = 0
if "score_ai" not in st.session_state:
    st.session_state.score_ai = 0
if "paddle_move" not in st.session_state:
    st.session_state.paddle_move = None

# Apply player paddle movement from previous input
if st.session_state.paddle_move == "UP":
    st.session_state.paddle_y = max(0, st.session_state.paddle_y - 1)
elif st.session_state.paddle_move == "DOWN":
    st.session_state.paddle_y = min(
        st.session_state.board_height - st.session_state.paddle_height,
        st.session_state.paddle_y + 1,
    )
st.session_state.paddle_move = None

# Simple AI paddle movement
if st.session_state.ball_y < st.session_state.ai_paddle_y:
    st.session_state.ai_paddle_y = max(0, st.session_state.ai_paddle_y - 1)
elif st.session_state.ball_y > st.session_state.ai_paddle_y + st.session_state.paddle_height - 1:
    st.session_state.ai_paddle_y = min(
        st.session_state.board_height - st.session_state.paddle_height,
        st.session_state.ai_paddle_y + 1,
    )

# Update ball position
st.session_state.ball_x += st.session_state.ball_dx
st.session_state.ball_y += st.session_state.ball_dy

# Bounce off top/bottom walls
if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.board_height - 1:
    st.session_state.ball_dy *= -1
    st.session_state.ball_y = max(0, min(st.session_state.board_height - 1, st.session_state.ball_y))

# Left paddle collision
if st.session_state.ball_dx < 0 and st.session_state.ball_x == 2:
    if st.session_state.paddle_y <= st.session_state.ball_y < st.session_state.paddle_y + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        st.session_state.ball_x = 2

# Right paddle collision
if st.session_state.ball_dx > 0 and st.session_state.ball_x == st.session_state.board_width - 3:
    if st.session_state.ai_paddle_y <= st.session_state.ball_y < st.session_state.ai_paddle_y + st.session_state.paddle_height:
        st.session_state.ball_dx *= -1
        st.session_state.ball_x = st.session_state.board_width - 3

# Scoring
if st.session_state.ball_x < 0:
    st.session_state.score_ai += 1
    st.session_state.ball_x = st.session_state.board_width // 2
    st.session_state.ball_y = st.session_state.board_height // 2
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = random.choice([-1, 1])
elif st.session_state.ball_x >= st.session_state.board_width:
    st.session_state.score_player += 1
    st.session_state.ball_x = st.session_state.board_width // 2
    st.session_state.ball_y = st.session_state.board_height // 2
    st.session_state.ball_dx = -1
    st.session_state.ball_dy = random.choice([-1, 1])

# Render board
grid = [[" "]*st.session_state.board_width for _ in range(st.session_state.board_height)]

for i in range(st.session_state.paddle_height):
    py = st.session_state.paddle_y + i
    if 0 <= py < st.session_state.board_height:
        grid[py][1] = "🟦"
    ay = st.session_state.ai_paddle_y + i
    if 0 <= ay < st.session_state.board_height:
        grid[ay][st.session_state.board_width - 2] = "🟦"

bx = st.session_state.ball_x
by = st.session_state.ball_y
if 0 <= by < st.session_state.board_height and 0 <= bx < st.session_state.board_width:
    grid[by][bx] = "⚪"

board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")

st.write(f"**Player:** {st.session_state.score_player}  **AI:** {st.session_state.score_ai}")

if st.button("Up ▲", key="up_btn"):
    st.session_state.paddle_move = "UP"
if st.button("Down ▼", key="down_btn"):
    st.session_state.paddle_move = "DOWN"
if st.button("Restart Game", key="restart_btn"):
    st.session_state.ball_x = st.session_state.board_width // 2
    st.session_state.ball_y = st.session_state.board_height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 1])
    st.session_state.paddle_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
    st.session_state.ai_paddle_y = (st.session_state.board_height - st.session_state.paddle_height) // 2
    st.session_state.score_player = 0
    st.session_state.score_ai = 0
    st.session_state.paddle_move = None
    st.rerun()