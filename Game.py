import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
if "width" not in st.session_state:
    st.session_state.width = 20
if "height" not in st.session_state:
    st.session_state.height = 15
if "paddle_height" not in st.session_state:
    st.session_state.paddle_height = 3
if "player_y" not in st.session_state:
    st.session_state.player_y = (st.session_state.height - st.session_state.paddle_height) // 2
if "ai_y" not in st.session_state:
    st.session_state.ai_y = (st.session_state.height - st.session_state.paddle_height) // 2
if "ball_x" not in st.session_state:
    st.session_state.ball_x = st.session_state.width // 2
if "ball_y" not in st.session_state:
    st.session_state.ball_y = st.session_state.height // 2
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = random.choice([-1, 1])
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = random.choice([-1, 0, 1])
if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "player_move" not in st.session_state:
    st.session_state.player_move = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "tick_counter" not in st.session_state:
    st.session_state.tick_counter = 0
if not st.session_state.game_over:
    new_player_y = st.session_state.player_y + st.session_state.player_move
    st.session_state.player_y = max(0, min(st.session_state.height - st.session_state.paddle_height, new_player_y))
    st.session_state.player_move = 0
    ai_target = st.session_state.ball_y - st.session_state.paddle_height // 2
    if st.session_state.ai_y < ai_target:
        st.session_state.ai_y = min(st.session_state.ai_y + 1, st.session_state.height - st.session_state.paddle_height)
    elif st.session_state.ai_y > ai_target:
        st.session_state.ai_y = max(st.session_state.ai_y - 1, 0)
    st.session_state.tick_counter += 1
    if st.session_state.tick_counter % 2 == 0:
        st.session_state.ball_x += st.session_state.ball_dx
        st.session_state.ball_y += st.session_state.ball_dy
        if st.session_state.ball_y <= 0 or st.session_state.ball_y >= st.session_state.height - 1:
            st.session_state.ball_dy *= -1
        player_paddle_x = 1
        ai_paddle_x = st.session_state.width - 2
        if st.session_state.ball_dx < 0 and st.session_state.ball_x == player_paddle_x + 1:
            if st.session_state.player_y <= st.session_state.ball_y < st.session_state.player_y + st.session_state.paddle_height:
                st.session_state.ball_dx = 1
                st.session_state.ball_dy = random.choice([-1, 0, 1])
        if st.session_state.ball_dx > 0 and st.session_state.ball_x == ai_paddle_x - 1:
            if st.session_state.ai_y <= st.session_state.ball_y < st.session_state.ai_y + st.session_state.paddle_height:
                st.session_state.ball_dx = -1
                st.session_state.ball_dy = random.choice([-1, 0, 1])
        if st.session_state.ball_x < 0:
            st.session_state.ai_score += 1
            st.session_state.ball_x = st.session_state.width // 2
            st.session_state.ball_y = st.session_state.height // 2
            st.session_state.ball_dx = 1
            st.session_state.ball_dy = random.choice([-1, 0, 1])
        if st.session_state.ball_x > st.session_state.width - 1:
            st.session_state.player_score += 1
            st.session_state.ball_x = st.session_state.width // 2
            st.session_state.ball_y = st.session_state.height // 2
            st.session_state.ball_dx = -1
            st.session_state.ball_dy = random.choice([-1, 0, 1])
        if st.session_state.player_score >= 5 or st.session_state.ai_score >= 5:
            st.session_state.game_over = True
grid = [["⬜" for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
for i in range(st.session_state.paddle_height):
    py = st.session_state.player_y + i
    if 0 <= py < st.session_state.height:
        grid[py][1] = "🟦"
    ay = st.session_state.ai_y + i
    if 0 <= ay < st.session_state.height:
        grid[ay][st.session_state.width - 2] = "🟦"
if 0 <= st.session_state.ball_y < st.session_state.height and 0 <= st.session_state.ball_x < st.session_state.width:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "🔴"
board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")
st.write(f"Player: {st.session_state.player_score} AI: {st.session_state.ai_score}")
if st.session_state.game_over:
    winner = "Player" if st.session_state.player_score > st.session_state.ai_score else "AI"
    st.write(f"Game Over! {winner} wins.")
if st.button("⬆️ Up", key="up_btn"):
    st.session_state.player_move = -1
if st.button("⬇️ Down", key="down_btn"):
    st.session_state.player_move = 1
if st.button("🔄 Restart", key="restart_btn"):
    st.session_state.player_y = (st.session_state.height - st.session_state.paddle_height) // 2
    st.session_state.ai_y = (st.session_state.height - st.session_state.paddle_height) // 2
    st.session_state.ball_x = st.session_state.width // 2
    st.session_state.ball_y = st.session_state.height // 2
    st.session_state.ball_dx = random.choice([-1, 1])
    st.session_state.ball_dy = random.choice([-1, 0, 1])
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.game_over = False
    st.session_state.player_move = 0
    st.session_state.tick_counter = 0
    st.rerun()