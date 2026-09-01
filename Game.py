import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
if 'width' not in st.session_state:
    st.session_state.width = 15
if 'height' not in st.session_state:
    st.session_state.height = 15
if 'snake' not in st.session_state:
    st.session_state.snake = [(7, 7), (7, 6), (7, 5)]
if 'direction' not in st.session_state:
    st.session_state.direction = "RIGHT"
if 'food' not in st.session_state:
    while True:
        food_pos = (random.randint(0, st.session_state.height - 1), random.randint(0, st.session_state.width - 1))
        if food_pos not in st.session_state.snake:
            st.session_state.food = food_pos
            break
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'high_score' not in st.session_state:
    st.session_state.high_score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if not st.session_state.game_over:
    head_y, head_x = st.session_state.snake[0]
    if st.session_state.direction == "UP":
        new_head = (head_y - 1, head_x)
    elif st.session_state.direction == "DOWN":
        new_head = (head_y + 1, head_x)
    elif st.session_state.direction == "LEFT":
        new_head = (head_y, head_x - 1)
    else:
        new_head = (head_y, head_x + 1)
    hit_wall = not (0 <= new_head[0] < st.session_state.height and 0 <= new_head[1] < st.session_state.width)
    hit_self = new_head in st.session_state.snake
    if hit_wall or hit_self:
        st.session_state.game_over = True
    else:
        st.session_state.snake.insert(0, new_head)
        if new_head == st.session_state.food:
            st.session_state.score += 1
            if st.session_state.score > st.session_state.high_score:
                st.session_state.high_score = st.session_state.score
            while True:
                new_food = (random.randint(0, st.session_state.height - 1), random.randint(0, st.session_state.width - 1))
                if new_food not in st.session_state.snake:
                    st.session_state.food = new_food
                    break
        else:
            st.session_state.snake.pop()
if st.button("⬆️", key="up_btn"):
    if st.session_state.direction != "DOWN":
        st.session_state.direction = "UP"
if st.button("⬇️", key="down_btn"):
    if st.session_state.direction != "UP":
        st.session_state.direction = "DOWN"
if st.button("⬅️", key="left_btn"):
    if st.session_state.direction != "RIGHT":
        st.session_state.direction = "LEFT"
if st.button("➡️", key="right_btn"):
    if st.session_state.direction != "LEFT":
        st.session_state.direction = "RIGHT"
if st.button("🔄 Restart", key="restart_btn"):
    st.session_state.snake = [(7, 7), (7, 6), (7, 5)]
    st.session_state.direction = "RIGHT"
    st.session_state.score = 0
    st.session_state.game_over = False
    while True:
        food_pos = (random.randint(0, st.session_state.height - 1), random.randint(0, st.session_state.width - 1))
        if food_pos not in st.session_state.snake:
            st.session_state.food = food_pos
            break
    st.rerun()
grid = [["⬜" for _ in range(st.session_state.width)] for _ in range(st.session_state.height)]
if 0 <= st.session_state.food[0] < st.session_state.height and 0 <= st.session_state.food[1] < st.session_state.width:
    grid[st.session_state.food[0]][st.session_state.food[1]] = "🍎"
for idx, segment in enumerate(st.session_state.snake):
    y, x = segment
    if 0 <= y < st.session_state.height and 0 <= x < st.session_state.width:
        grid[y][x] = "🟢" if idx == 0 else "🟩"
board = "\n".join("".join(row) for row in grid)
st.code(board, language="text")
st.write(f"Score: {st.session_state.score} | High Score: {st.session_state.high_score}")
if st.session_state.game_over:
    st.write("💀 Game Over! Press Restart to play again.")