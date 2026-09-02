import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=150, key="game_loop_ticker")
if 'grid_width' not in st.session_state:
    st.session_state.grid_width = 20
if 'grid_height' not in st.session_state:
    st.session_state.grid_height = 15
if 'snake' not in st.session_state:
    start_x = st.session_state.grid_width // 2
    start_y = st.session_state.grid_height // 2
    st.session_state.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
if 'direction' not in st.session_state:
    st.session_state.direction = "RIGHT"
if 'food' not in st.session_state:
    while True:
        fx = random.randint(0, st.session_state.grid_width - 1)
        fy = random.randint(0, st.session_state.grid_height - 1)
        if (fx, fy) not in st.session_state.snake:
            st.session_state.food = (fx, fy)
            break
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if not st.session_state.game_over:
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
    head_x, head_y = st.session_state.snake[0]
    new_head = (head_x + dx, head_y + dy)
    hit_wall = not (0 <= new_head[0] < st.session_state.grid_width and 0 <= new_head[1] < st.session_state.grid_height)
    hit_self = new_head in st.session_state.snake
    if hit_wall or hit_self:
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, new_head)
        if new_head == st.session_state.food:
            st.session_state.score += 1
            while True:
                fx = random.randint(0, st.session_state.grid_width - 1)
                fy = random.randint(0, st.session_state.grid_height - 1)
                if (fx, fy) not in st.session_state.snake:
                    st.session_state.food = (fx, fy)
                    break
        else:
            st.session_state.snake.pop()
grid = [["⬜" for _ in range(st.session_state.grid_width)] for _ in range(st.session_state.grid_height)]
fx, fy = st.session_state.food
grid[fy][fx] = "🍎"
for idx, (x, y) in enumerate(st.session_state.snake):
    if idx == 0:
        grid[y][x] = "🟢"
    else:
        grid[y][x] = "🟩"
board_string = "\n".join("".join(row) for row in grid)
st.code(board_string, language="text")
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.write("Game Over! Press Restart to play again.")
if st.button("Up", key="btn_up"):
    if st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
if st.button("Down", key="btn_down"):
    if st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
if st.button("Left", key="btn_left"):
    if st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
if st.button("Right", key="btn_right"):
    if st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"
if st.button("Restart", key="btn_restart"):
    start_x = st.session_state.grid_width // 2
    start_y = st.session_state.grid_height // 2
    st.session_state.snake = [(start_x, start_y), (start_x - 1, start_y), (start_x - 2, start_y)]
    st.session_state.direction = "RIGHT"
    while True:
        fx = random.randint(0, st.session_state.grid_width - 1)
        fy = random.randint(0, st.session_state.grid_height - 1)
        if (fx, fy) not in st.session_state.snake:
            st.session_state.food = (fx, fy)
            break
    st.session_state.score = 0
    st.session_state.game_over = False
    st.rerun()