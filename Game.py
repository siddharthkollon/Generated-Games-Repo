import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="refresh")
if 'grid_width' not in st.session_state:
    st.session_state.grid_width = 15
if 'grid_height' not in st.session_state:
    st.session_state.grid_height = 20
if 'player_x' not in st.session_state:
    st.session_state.player_x = st.session_state.grid_width // 2
if 'bullet_positions' not in st.session_state:
    st.session_state.bullet_positions = []
if 'enemies' not in st.session_state:
    st.session_state.enemies = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'tick_count' not in st.session_state:
    st.session_state.tick_count = 0
if 'direction' not in st.session_state:
    st.session_state.direction = None
if 'shoot' not in st.session_state:
    st.session_state.shoot = False
if not st.session_state.game_over:
    if st.button("⬅️", key="move_left"):
        st.session_state.direction = "LEFT"
    if st.button("➡️", key="move_right"):
        st.session_state.direction = "RIGHT"
    if st.button("🔫", key="shoot"):
        st.session_state.shoot = True
if st.session_state.game_over:
    if st.button("🔄 Restart", key="restart"):
        st.session_state.player_x = st.session_state.grid_width // 2
        st.session_state.bullet_positions = []
        st.session_state.enemies = []
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.tick_count = 0
        st.session_state.direction = None
        st.session_state.shoot = False
        st.rerun()
st.session_state.tick_count += 1
if not st.session_state.game_over:
    if st.session_state.direction == "LEFT":
        st.session_state.player_x = max(0, st.session_state.player_x - 1)
    if st.session_state.direction == "RIGHT":
        st.session_state.player_x = min(st.session_state.grid_width - 1, st.session_state.player_x + 1)
    st.session_state.direction = None
    if st.session_state.shoot:
        st.session_state.bullet_positions.append([st.session_state.player_x, st.session_state.grid_height - 2])
        st.session_state.shoot = False
    new_bullets = []
    for b in st.session_state.bullet_positions:
        b[1] -= 1
        if b[1] >= 0:
            new_bullets.append(b)
    st.session_state.bullet_positions = new_bullets
    new_enemies = []
    for e in st.session_state.enemies:
        e[1] += 1
        if e[1] < st.session_state.grid_height:
            new_enemies.append(e)
    st.session_state.enemies = new_enemies
    hit_bullets = []
    hit_enemies = []
    for bi, b in enumerate(st.session_state.bullet_positions):
        for ei, e in enumerate(st.session_state.enemies):
            if b[0] == e[0] and b[1] == e[1]:
                hit_bullets.append(bi)
                hit_enemies.append(ei)
                st.session_state.score += 1
    st.session_state.bullet_positions = [b for i, b in enumerate(st.session_state.bullet_positions) if i not in hit_bullets]
    st.session_state.enemies = [e for i, e in enumerate(st.session_state.enemies) if i not in hit_enemies]
    if st.session_state.tick_count % 10 == 0:
        spawn_x = random.randint(0, st.session_state.grid_width - 1)
        st.session_state.enemies.append([spawn_x, 0])
    for e in st.session_state.enemies:
        if e[1] == st.session_state.grid_height - 1:
            st.session_state.game_over = True
grid = [["⬛" for _ in range(st.session_state.grid_width)] for _ in range(st.session_state.grid_height)]
if 0 <= st.session_state.player_x < st.session_state.grid_width:
    grid[st.session_state.grid_height - 1][st.session_state.player_x] = "🚀"
for b in st.session_state.bullet_positions:
    if 0 <= b[1] < st.session_state.grid_height and 0 <= b[0] < st.session_state.grid_width:
        grid[b[1]][b[0]] = "🔺"
for e in st.session_state.enemies:
    if 0 <= e[1] < st.session_state.grid_height and 0 <= e[0] < st.session_state.grid_width:
        grid[e[1]][e[0]] = "👾"
board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.write("💥 Game Over! Press Restart to play again.")