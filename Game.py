import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
if "ball_x" not in st.session_state:
    st.session_state.ball_x = 10
if "ball_y" not in st.session_state:
    st.session_state.ball_y = 7
if "ball_dx" not in st.session_state:
    st.session_state.ball_dx = 1
if "ball_dy" not in st.session_state:
    st.session_state.ball_dy = 1
if "player_y" not in st.session_state:
    st.session_state.player_y = 6
if "ai_y" not in st.session_state:
    st.session_state.ai_y = 6
if "score_player" not in st.session_state:
    st.session_state.score_player = 0
if "score_ai" not in st.session_state:
    st.session_state.score_ai = 0
if "player_dir" not in st.session_state:
    st.session_state.player_dir = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if st.button("⬆️ Up", key="up_button"):
    st.session_state.player_dir = -1
if st.button("⬇️ Down", key="down_button"):
    st.session_state.player_dir = 1
if st.button("🔄 Restart", key="restart_button"):
    st.session_state.ball_x = 10
    st.session_state.ball_y = 7
    st.session_state.ball_dx = 1
    st.session_state.ball_dy = 1
    st.session_state.player_y = 6
    st.session_state.ai_y = 6
    st.session_state.score_player = 0
    st.session_state.score_ai = 0
    st.session_state.game_over = False
    st.session_state.player_dir = 0
    st.rerun()
BOARD_WIDTH = 20
BOARD_HEIGHT = 15
if not st.session_state.game_over:
    new_player_y = st.session_state.player_y + st.session_state.player_dir
    st.session_state.player_y = max(0, min(BOARD_HEIGHT - 3, new_player_y))
    st.session_state.player_dir = 0
    if st.session_state.ai_y + 1 < st.session_state.ball_y:
        st.session_state.ai_y += 1
    elif st.session_state.ai_y > st.session_state.ball_y:
        st.session_state.ai_y -= 1
    st.session_state.ai_y = max(0, min(BOARD_HEIGHT - 3, st.session_state.ai_y))
    st.session_state.ball_x += st.session_state.ball_dx
    st.session_state.ball_y += st.session_state.ball_dy
    if st.session_state.ball_y <= 0 or st.session_state.ball_y >= BOARD_HEIGHT - 1:
        st.session_state.ball_dy *= -1
    if st.session_state.ball_x <= 1:
        if st.session_state.player_y <= st.session_state.ball_y <= st.session_state.player_y + 2:
            st.session_state.ball_dx = 1
        else:
            st.session_state.score_ai += 1
            st.session_state.ball_x = BOARD_WIDTH // 2
            st.session_state.ball_y = BOARD_HEIGHT // 2
            st.session_state.ball_dx = 1
            st.session_state.ball_dy = random.choice([-1, 1])
    if st.session_state.ball_x >= BOARD_WIDTH - 2:
        if st.session_state.ai_y <= st.session_state.ball_y <= st.session_state.ai_y + 2:
            st.session_state.ball_dx = -1
        else:
            st.session_state.score_player += 1
            st.session_state.ball_x = BOARD_WIDTH // 2
            st.session_state.ball_y = BOARD_HEIGHT // 2
            st.session_state.ball_dx = -1
            st.session_state.ball_dy = random.choice([-1, 1])
    if st.session_state.score_player >= 5 or st.session_state.score_ai >= 5:
        st.session_state.game_over = True
grid = [["⬜" for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
for i in range(3):
    if 0 <= st.session_state.player_y + i < BOARD_HEIGHT:
        grid[st.session_state.player_y + i][1] = "🟦"
    if 0 <= st.session_state.ai_y + i < BOARD_HEIGHT:
        grid[st.session_state.ai_y + i][BOARD_WIDTH - 2] = "🟦"
if 0 <= st.session_state.ball_y < BOARD_HEIGHT and 0 <= st.session_state.ball_x < BOARD_WIDTH:
    grid[st.session_state.ball_y][st.session_state.ball_x] = "⚪"
board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")
st.write(f"Player: {st.session_state.score_player}  AI: {st.session_state.score_ai}")
if st.session_state.game_over:
    if st.session_state.score_player > st.session_state.score_ai:
        st.subheader("🏆 You Win!")
    else:
        st.subheader("🤖 AI Wins!")