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
if 'bullets' not in st.session_state:
    st.session_state.bullets = []
if 'enemies' not in st.session_state:
    st.session_state.enemies = []
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'tick' not in st.session_state:
    st.session_state.tick = 0
if 'move_dir' not in st.session_state:
    st.session_state.move_dir = None
if 'fire' not in st.session_state:
    st.session_state.fire = False
if not st.session_state.game_over:
    if st.button("⬅️", key="btn_left"):
        st.session_state.move_dir = "LEFT"
    if st.button("➡️", key="btn_right"):
        st.session_state.move_dir = "RIGHT"
    if st.button("🔫", key="btn_fire"):
        st.session_state.fire = True
if st.session_state.game_over:
    if st.button("🔄 Restart", key="btn_restart"):
        st.session_state.player_x = st.session_state.grid_width // 2
        st.session_state.bullets = []
        st.session_state.enemies = []
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.tick = 0
        st.session_state.move_dir = None
        st.session_state.fire = False
        st.rerun()
st.session_state.tick += 1
if not st.session_state.game_over:
    if st.session_state.move_dir == "LEFT":
        st.session_state.player_x = max(0, st.session_state.player_x - 1)
    if st.session_state.move_dir == "RIGHT":
        st.session_state.player_x = min(st.session_state.grid_width - 1, st.session_state.player_x + 1)
    st.session_state.move_dir = None
    if st.session_state.fire:
        st.session_state.bullets.append([st.session_state.player_x, st.session_state.grid_height - 2])
        st.session_state.fire = False
    new_bullets = []
    for b in st.session_state.bullets:
        b[1] -= 1
        if b[1] >= 0:
            new_bullets.append(b)
    st.session_state.bullets = new_bullets
    new_enemies = []
    for e in st.session_state.enemies:
        e[1] += 1
        if e[1] < st.session_state.grid_height:
            new_enemies.append(e)
    st.session_state.enemies = new_enemies
    hit_bullet_idxs = set()
    hit_enemy_idxs = set()
    for bi, b in enumerate(st.session_state.bullets):
        for ei, e in enumerate(st.session_state.enemies):
            if b[0] == e[0] and b[1] == e[1]:
                hit_bullet_idxs.add(bi)
                hit_enemy_idxs.add(ei)
                st.session_state.score += 1
    st.session_state.bullets = [b for i, b in enumerate(st.session_state.bullets) if i not in hit_bullet_idxs]
    st.session_state.enemies = [e for i, e in enumerate(st.session_state.enemies) if i not in hit_enemy_idxs]
    if st.session_state.tick % 10 == 0:
        spawn_x = random.randint(0, st.session_state.grid_width - 1)
        st.session_state.enemies.append([spawn_x, 0])
    for e in st.session_state.enemies:
        if e[1] == st.session_state.grid_height - 1:
            st.session_state.game_over = True
grid = [["⬛" for _ in range(st.session_state.grid_width)] for _ in range(st.session_state.grid_height)]
if 0 <= st.session_state.player_x < st.session_state.grid_width:
    grid[st.session_state.grid_height - 1][st.session_state.player_x] = "🚀"
for b in st.session_state.bullets:
    if 0 <= b[1] < st.session_state.grid_height and 0 <= b[0] < st.session_state.grid_width:
        grid[b[1]][b[0]] = "🔺"
for e in st.session_state.enemies:
    if 0 <= e[1] < st.session_state.grid_height and 0 <= e[0] < st.session_state.grid_width:
        grid[e[1]][e[0]] = "👾"
board = "\n".join("".join(row) for row in grid)
st.code(board, language="text")
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.write("💥 Game Over! Press Restart to play again.")