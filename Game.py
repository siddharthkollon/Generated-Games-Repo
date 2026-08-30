import streamlit as st
from streamlit_autorefresh import st_autorefresh
st_autorefresh(interval=200, key="game_loop")
if 'width' not in st.session_state:
    st.session_state.width = 20
if 'height' not in st.session_state:
    st.session_state.height = 15
if 'player_x' not in st.session_state:
    st.session_state.player_x = 2
if 'player_y' not in st.session_state:
    st.session_state.player_y = 13
if 'vy' not in st.session_state:
    st.session_state.vy = 0
if 'on_ground' not in st.session_state:
    st.session_state.on_ground = False
if 'move' not in st.session_state:
    st.session_state.move = 0
if 'platforms' not in st.session_state:
    st.session_state.platforms = [(x, 14) for x in range(20)] + [(5, 10), (6, 10), (7, 10), (12, 8), (13, 8), (14, 8), (2, 5), (3, 5), (4, 5)]
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'max_x' not in st.session_state:
    st.session_state.max_x = st.session_state.player_x
col1, col2, col3, col4 = st.columns([1, 1, 1, 6])
with col1:
    if st.button("←", key="btn_left"):
        st.session_state.move = -1
with col2:
    if st.button("→", key="btn_right"):
        st.session_state.move = 1
with col3:
    if st.button("⤴", key="btn_jump"):
        if st.session_state.on_ground:
            st.session_state.vy = -2
            st.session_state.on_ground = False
with col4:
    if st.button("Restart", key="btn_restart"):
        st.session_state.player_x = 2
        st.session_state.player_y = 13
        st.session_state.vy = 0
        st.session_state.on_ground = False
        st.session_state.move = 0
        st.session_state.score = 0
        st.session_state.max_x = 2
        st.rerun()
new_x = st.session_state.player_x + st.session_state.move
if new_x < 0:
    new_x = 0
if new_x >= st.session_state.width:
    new_x = st.session_state.width - 1
if (new_x, st.session_state.player_y) in st.session_state.platforms:
    new_x = st.session_state.player_x
st.session_state.player_x = new_x
st.session_state.move = 0
st.session_state.vy = st.session_state.vy + 1
if st.session_state.vy > 2:
    st.session_state.vy = 2
new_y = st.session_state.player_y + st.session_state.vy
landed = False
if new_y >= st.session_state.height - 1:
    new_y = st.session_state.height - 1
    st.session_state.vy = 0
    landed = True
else:
    for px, py in st.session_state.platforms:
        if st.session_state.vy > 0 and st.session_state.player_y < py and new_y >= py and st.session_state.player_x == px:
            new_y = py
            st.session_state.vy = 0
            landed = True
            break
st.session_state.on_ground = landed
st.session_state.player_y = new_y
if st.session_state.player_x > st.session_state.max_x:
    st.session_state.max_x = st.session_state.player_x
    st.session_state.score = st.session_state.max_x
grid = [["⬜" for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
for px, py in st.session_state.platforms:
    if 0 <= py < st.session_state.height and 0 <= px < st.session_state.width:
        grid[py][px] = "🟫"
grid[st.session_state.player_y][st.session_state.player_x] = "🤖"
board = "\n".join("".join(row) for row in grid)
st.code(board, language="text")
st.write(f"Score (furthest right): {st.session_state.score}")