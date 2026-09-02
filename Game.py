import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop")
if "width" not in st.session_state:
    st.session_state.width = 20
if "height" not in st.session_state:
    st.session_state.height = 12
if "ground_y" not in st.session_state:
    st.session_state.ground_y = st.session_state.height - 2
if "mario_x" not in st.session_state:
    st.session_state.mario_x = 2
if "mario_y" not in st.session_state:
    st.session_state.mario_y = st.session_state.ground_y
if "mario_vy" not in st.session_state:
    st.session_state.mario_vy = 0
if "jumping" not in st.session_state:
    st.session_state.jumping = False
if "obstacles" not in st.session_state:
    st.session_state.obstacles = []
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if not st.session_state.game_over:
    new_obstacles = []
    for x in st.session_state.obstacles:
        nx = x - 1
        if nx >= 0:
            new_obstacles.append(nx)
    st.session_state.obstacles = new_obstacles
    if random.random() < 0.2:
        if st.session_state.width - 1 not in st.session_state.obstacles:
            st.session_state.obstacles.append(st.session_state.width - 1)
    if st.session_state.jumping:
        st.session_state.mario_y += st.session_state.mario_vy
        st.session_state.mario_vy += 1
        if st.session_state.mario_y >= st.session_state.ground_y:
            st.session_state.mario_y = st.session_state.ground_y
            st.session_state.jumping = False
    for ox in st.session_state.obstacles:
        if ox == st.session_state.mario_x and st.session_state.mario_y == st.session_state.ground_y:
            st.session_state.game_over = True
    st.session_state.score += 1
if st.button("Jump", key="jump_btn"):
    if not st.session_state.game_over and not st.session_state.jumping and st.session_state.mario_y == st.session_state.ground_y:
        st.session_state.mario_vy = -2
        st.session_state.jumping = True
if st.button("Restart Game", key="restart_btn"):
    st.session_state.mario_y = st.session_state.ground_y
    st.session_state.mario_vy = 0
    st.session_state.jumping = False
    st.session_state.obstacles = []
    st.session_state.score = 0
    st.session_state.game_over = False
    st.rerun()
grid = [[" " for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
for x in range(st.session_state.width):
    grid[st.session_state.ground_y][x] = "🟩"
if 0 <= st.session_state.mario_y < st.session_state.height and 0 <= st.session_state.mario_x < st.session_state.width:
    grid[st.session_state.mario_y][st.session_state.mario_x] = "🧑"
for ox in st.session_state.obstacles:
    if 0 <= st.session_state.ground_y < st.session_state.height and 0 <= ox < st.session_state.width:
        grid[st.session_state.ground_y][ox] = "🌵"
board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")
st.write("Score:", st.session_state.score)
if st.session_state.game_over:
    st.write("Game Over! Press Restart to play again.")