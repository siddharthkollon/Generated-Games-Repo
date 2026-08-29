import random
import streamlit as st
from streamlit_autorefresh import st_autorefresh

# Refresh interval (150 ms)
st_autorefresh(interval=150, key="game_loop_ticker")

# Game dimensions
WIDTH = 20
HEIGHT = 12
PADDLE_SIZE = 3

# Initialize session state variables
if "ball_x" not in st.session_state:
    st.session_state.ball_x = WIDTH // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = HEIGHT // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "p1_y" not in st.session_state:
    st.session_state.p1_y = HEIGHT // 2 - PADDLE_SIZE // 2
if "p2_y" not in st.session_state:
    st.session_state.p2_y = HEIGHT // 2 - PADDLE_SIZE // 2
if "p1_dir" not in st.session_state:
    st.session_state.p1_dir = 0
if "p2_dir" not in st.session_state:
    st.session_state.p2_dir = 0
if "score1" not in st.session_state:
    st.session_state.score1 = 0
if "score2" not in st.session_state:
    st.session_state.score2 = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False

# Apply paddle movements
if not st.session_state.game_over:
    st.session_state.p1_y = max(
        0, min(HEIGHT - PADDLE_SIZE, st.session_state.p1_y + st.session_state.p1_dir)
    )
    st.session_state.p2_y = max(
        0, min(HEIGHT - PADDLE_SIZE, st.session_state.p2_y + st.session_state.p2_dir)
    )
# Reset movement flags
st.session_state.p1_dir = 0
st.session_state.p2_dir = 0

# Update ball position and handle collisions
if not st.session_state.game_over:
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy

    # Top / bottom wall bounce
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= HEIGHT - 1:
        st.session_state.ball_dy *= -1

    # Left wall (Player 1 side)
    if st.session_state.ball_x <= 0:
        if st.session_state.p1_y <= st.session_state.ball_y < st.session_state.p1_y + PADDLE_SIZE:
            st.session_state.ball_dx = 1
            st.session_state.ball_dy = random.choice([-1, 0, 1])
        else:
            st.session_state.score2 += 1
            st.session_state.ball_x = WIDTH // 2
            st.session_state.ball_y = HEIGHT // 2
            st.session_state.ball_dx = 1
            st.session_state.ball_dy = random.choice([-1, 0, 1])

    # Right wall (Player 2 side)
    if st.session_state.ball_x >= WIDTH - 1:
        if st.session_state.p2_y <= st.session_state.ball_y < st.session_state.p2_y + PADDLE_SIZE:
            st.session_state.ball_dx = -1
            st.session_state.ball_dy = random.choice([-1, 0, 1])
        else:
            st.session_state.score1 += 1
            st.session_state.ball_x = WIDTH // 2
            st.session_state.ball_y = HEIGHT // 2
            st.session_state.ball_dx = -1
            st.session_state.ball_dy = random.choice([-1, 0, 1])

# Win condition (first to 10)
if not st.session_state.game_over:
    if st.session_state.score1 >= 10 or st.session_state.score2 >= 10:
        st.session_state.game_over = True

# UI Controls
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.button("⬆️", key="p1_up", on_click=lambda: st.session_state.update(p1_dir=-1))
    st.button("⬇️", key="p1_down", on_click=lambda: st.session_state.update(p1_dir=1))

with col3:
    st.button("⬆️", key="p2_up", on_click=lambda: st.session_state.update(p2_dir=-1))
    st.button("⬇️", key="p2_down", on_click=lambda: st.session_state.update(p2_dir=1))

# Scoreboard
st.markdown(
    f"**Player 1:** {st.session_state.score1} &nbsp;&nbsp; **Player 2:** {st.session_state.score2}",
    unsafe_allow_html=True,
)

# Render game board
grid = [["⬜" for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Place paddles
for i in range(PADDLE_SIZE):
    grid[st.session_state.p1_y + i][0] = "🟦"
    grid[st.session_state.p2_y + i][WIDTH - 1] = "🟦"

# Place ball (red)
if 0 <= st.session_state.ball_y < HEIGHT and 0 <= st.session_state.ball_x < WIDTH:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "🔴"

board_str = "\n".join("".join(row) for row in grid)
st.code(board_str, language="text")

# Restart button
if st.button("Restart Game", key="restart_btn"):
    for key in [
        "ball_x",
        "ball_y",
        "ball_dx",
        "ball_dy",
        "p1_y",
        "p2_y",
        "p1_dir",
        "p2_dir",
        "score1",
        "score2",
        "game_over",
    ]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

# Game over message
if st.session_state.game_over:
    winner = "Player 1" if st.session_state.score1 > st.session_state.score2 else "Player 2"
    st.success(f"Game Over! {winner} wins!")