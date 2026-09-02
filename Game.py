import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop")
if 'grid_width' not in st.session_state:
    st.session_state.grid_width = 15
if 'grid_height' not in st.session_state:
    st.session_state.grid_height = 15
if 'player_x' not in st.session_state:
    st.session_state.player_x = st.session_state.grid_width // 2
if 'player_y' not in st.session_state:
    st.session_state.player_y = st.session_state.grid_height // 2
if 'food_x' not in st.session_state:
    st.session_state.food_x = random.randint(0, st.session_state.grid_width - 1)
if 'food_y' not in st.session_state:
    st.session_state.food_y = random.randint(0, st.session_state.grid_height - 1)
if 'direction' not in st.session_state:
    st.session_state.direction = "UP"
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
def reset_game():
    st.session_state.player_x = st.session_state.grid_width // 2
    st.session_state.player_y = st.session_state.grid_height // 2
    st.session_state.food_x = random.randint(0, st.session_state.grid_width - 1)
    st.session_state.food_y = random.randint(0, st.session_state.grid_height - 1)
    st.session_state.direction = "UP"
    st.session_state.score = 0
    st.session_state.game_over = False
    st.rerun()
st.button("Restart", on_click=reset_game, key="btn_restart")
if not st.session_state.game_over:
    if st.button("Up", key="btn_up"):
        st.session_state.direction = "UP"
    if st.button("Down", key="btn_down"):
        st.session_state.direction = "DOWN"
    if st.button("Left", key="btn_left"):
        st.session_state.direction = "LEFT"
    if st.button("Right", key="btn_right"):
        st.session_state.direction = "RIGHT"
    dx = 0
    dy = 0
    if st.session_state.direction == "UP":
        dy = -1
    elif st.session_state.direction == "DOWN":
        dy = 1
    elif st.session_state.direction == "LEFT":
        dx = -1
    elif st.session_state.direction == "RIGHT":
        dx = 1
    new_x = st.session_state.player_x + dx
    new_y = st.session_state.player_y + dy
    if 0 <= new_x < st.session_state.grid_width and 0 <= new_y < st.session_state.grid_height:
        st.session_state.player_x = new_x
        st.session_state.player_y = new_y
    else:
        st.session_state.game_over = True
    if st.session_state.player_x == st.session_state.food_x and st.session_state.player_y == st.session_state.food_y:
        st.session_state.score += 1
        while True:
            new_fx = random.randint(0, st.session_state.grid_width - 1)
            new_fy = random.randint(0, st.session_state.grid_height - 1)
            if new_fx != st.session_state.player_x or new_fy != st.session_state.player_y:
                st.session_state.food_x = new_fx
                st.session_state.food_y = new_fy
                break
grid = [["⬜" for _ in range(st.session_state.grid_width)] for _ in range(st.session_state.grid_height)]
if 0 <= st.session_state.player_y < st.session_state.grid_height and 0 <= st.session_state.player_x < st.session_state.grid_width:
    grid[st.session_state.player_y][st.session_state.player_x] = "😀"
if 0 <= st.session_state.food_y < st.session_state.grid_height and 0 <= st.session_state.food_x < st.session_state.grid_width:
    grid[st.session_state.food_y][st.session_state.food_x] = "⭐"
board = "\n".join("".join(row) for row in grid)
st.code(board, language="text")
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.write("Game Over! Press Restart to play again.")