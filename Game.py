import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import copy
st_autorefresh(interval=200, key="refresh")
WIDTH = 10
HEIGHT = 20
EMPTY = "⬜"
if "board" not in st.session_state:
    st.session_state.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
if "shapes" not in st.session_state:
    st.session_state.shapes = [
        {"color": "🟦", "rotations": [[(0,1),(1,1),(2,1),(3,1)],[(2,0),(2,1),(2,2),(2,3)],[(0,2),(1,2),(2,2),(3,2)],[(1,0),(1,1),(1,2),(1,3)]]},
        {"color": "🟨", "rotations": [[(1,0),(2,0),(1,1),(2,1)]]*4},
        {"color": "🟪", "rotations": [[(1,0),(0,1),(1,1),(2,1)],[(1,0),(1,1),(2,1),(1,2)],[(0,1),(1,1),(2,1),(1,2)],[(1,0),(0,1),(1,1),(1,2)]]},
        {"color": "🟩", "rotations": [[(1,0),(2,0),(0,1),(1,1)],[(1,0),(1,1),(2,1),(2,2)],[(1,1),(2,1),(0,2),(1,2)],[(0,0),(0,1),(1,1),(1,2)]]},
        {"color": "🟥", "rotations": [[(0,0),(1,0),(1,1),(2,1)],[(2,0),(1,1),(2,1),(1,2)],[(0,1),(1,1),(1,2),(2,2)],[(1,0),(0,1),(1,1),(0,2)]]},
        {"color": "🟧", "rotations": [[(0,0),(0,1),(1,1),(2,1)],[(1,0),(2,0),(1,1),(1,2)],[(0,1),(1,1),(2,1),(2,2)],[(1,0),(1,1),(0,2),(1,2)]]},
        {"color": "🟫", "rotations": [[(2,0),(0,1),(1,1),(2,1)],[(1,0),(1,1),(1,2),(2,2)],[(0,1),(1,1),(2,1),(0,2)],[(0,0),(1,0),(1,1),(1,2)]]}
    ]
if "current_shape" not in st.session_state:
    st.session_state.current_shape = random.randint(0, len(st.session_state.shapes) - 1)
if "rotation" not in st.session_state:
    st.session_state.rotation = 0
if "piece_x" not in st.session_state:
    st.session_state.piece_x = WIDTH // 2 - 2
if "piece_y" not in st.session_state:
    st.session_state.piece_y = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "lines_cleared" not in st.session_state:
    st.session_state.lines_cleared = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "move" not in st.session_state:
    st.session_state.move = "NONE"
def can_place(px, py, rot):
    shape = st.session_state.shapes[st.session_state.current_shape]
    for dx, dy in shape["rotations"][rot % len(shape["rotations"])]:
        x = px + dx
        y = py + dy
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            return False
        if st.session_state.board[y][x] != EMPTY:
            return False
    return True
if not st.session_state.game_over:
    if st.session_state.move == "LEFT":
        if can_place(st.session_state.piece_x - 1, st.session_state.piece_y, st.session_state.rotation):
            st.session_state.piece_x -= 1
    if st.session_state.move == "RIGHT":
        if can_place(st.session_state.piece_x + 1, st.session_state.piece_y, st.session_state.rotation):
            st.session_state.piece_x += 1
    if st.session_state.move == "ROTATE":
        if can_place(st.session_state.piece_x, st.session_state.piece_y, st.session_state.rotation + 1):
            st.session_state.rotation = (st.session_state.rotation + 1) % len(st.session_state.shapes[st.session_state.current_shape]["rotations"])
    if st.session_state.move == "DOWN":
        if can_place(st.session_state.piece_x, st.session_state.piece_y + 1, st.session_state.rotation):
            st.session_state.piece_y += 1
    st.session_state.move = "NONE"
    if can_place(st.session_state.piece_x, st.session_state.piece_y + 1, st.session_state.rotation):
        st.session_state.piece_y += 1
    else:
        shape = st.session_state.shapes[st.session_state.current_shape]
        color = shape["color"]
        for dx, dy in shape["rotations"][st.session_state.rotation % len(shape["rotations"])]:
            x = st.session_state.piece_x + dx
            y = st.session_state.piece_y + dy
            st.session_state.board[y][x] = color
        new_board = []
        lines_removed = 0
        for row in st.session_state.board:
            if EMPTY not in row:
                lines_removed += 1
            else:
                new_board.append(row)
        for _ in range(lines_removed):
            new_board.insert(0, [EMPTY for _ in range(WIDTH)])
        st.session_state.board = new_board
        st.session_state.lines_cleared += lines_removed
        st.session_state.score += (lines_removed * 100)
        st.session_state.current_shape = random.randint(0, len(st.session_state.shapes) - 1)
        st.session_state.rotation = 0
        st.session_state.piece_x = WIDTH // 2 - 2
        st.session_state.piece_y = 0
        if not can_place(st.session_state.piece_x, st.session_state.piece_y, st.session_state.rotation):
            st.session_state.game_over = True
st.title("🧱 Tetris")
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("←", key="left_btn"):
        st.session_state.move = "LEFT"
with col2:
    if st.button("→", key="right_btn"):
        st.session_state.move = "RIGHT"
with col3:
    if st.button("⤾", key="rotate_btn"):
        st.session_state.move = "ROTATE"
with col4:
    if st.button("↓", key="down_btn"):
        st.session_state.move = "DOWN"
if st.button("Restart", key="restart_btn"):
    st.session_state.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
    st.session_state.current_shape = random.randint(0, len(st.session_state.shapes) - 1)
    st.session_state.rotation = 0
    st.session_state.piece_x = WIDTH // 2 - 2
    st.session_state.piece_y = 0
    st.session_state.score = 0
    st.session_state.lines_cleared = 0
    st.session_state.game_over = False
    st.session_state.move = "NONE"
    st.rerun()
display_grid = copy.deepcopy(st.session_state.board)
if not st.session_state.game_over:
    shape = st.session_state.shapes[st.session_state.current_shape]
    color = shape["color"]
    for dx, dy in shape["rotations"][st.session_state.rotation % len(shape["rotations"])]:
        x = st.session_state.piece_x + dx
        y = st.session_state.piece_y + dy
        if 0 <= x < WIDTH and 0 <= y < HEIGHT:
            display_grid[y][x] = color
board_str = "\n".join("".join(row) for row in display_grid)
st.code(boar