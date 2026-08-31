import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
st_autorefresh(interval=200, key="game_loop_ticker")
if 'board' not in st.session_state:
    st.session_state.board = [["⬛" for _ in range(10)] for _ in range(20)]
if 'piece' not in st.session_state:
    st.session_state.piece = None
if 'piece_x' not in st.session_state:
    st.session_state.piece_x = 3
if 'piece_y' not in st.session_state:
    st.session_state.piece_y = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'move' not in st.session_state:
    st.session_state.move = None
if 'rotate' not in st.session_state:
    st.session_state.rotate = False
def get_shapes():
    return [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[0, 1, 0], [1, 1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 0], [0, 1, 1]],
        [[1, 0, 0], [1, 1, 1]],
        [[0, 0, 1], [1, 1, 1]],
    ]
def rotate_clockwise(matrix):
    return [list(row) for row in zip(*matrix[::-1])]
def check_collision(board, piece, x, y):
    for r, row in enumerate(piece):
        for c, val in enumerate(row):
            if val:
                bx = x + c
                by = y + r
                if bx < 0 or bx >= len(board[0]) or by < 0 or by >= len(board):
                    return True
                if board[by][bx] != "⬛":
                    return True
    return False
def merge_piece(board, piece, x, y):
    for r, row in enumerate(piece):
        for c, val in enumerate(row):
            if val:
                board[y + r][x + c] = "🟦"
def clear_lines(board):
    new_board = [row for row in board if any(cell == "⬛" for cell in row)]
    cleared = len(board) - len(new_board)
    for _ in range(cleared):
        new_board.insert(0, ["⬛" for _ in range(10)])
    return new_board, cleared
def spawn_piece():
    shapes = get_shapes()
    piece = random.choice(shapes)
    st.session_state.piece = piece
    st.session_state.piece_x = (len(st.session_state.board[0]) - len(piece[0])) // 2
    st.session_state.piece_y = 0
    if check_collision(st.session_state.board, piece, st.session_state.piece_x, st.session_state.piece_y):
        st.session_state.game_over = True
if st.session_state.piece is None and not st.session_state.game_over:
    spawn_piece()
if not st.session_state.game_over:
    if st.session_state.move == "LEFT":
        nx = st.session_state.piece_x - 1
        if not check_collision(st.session_state.board, st.session_state.piece, nx, st.session_state.piece_y):
            st.session_state.piece_x = nx
    elif st.session_state.move == "RIGHT":
        nx = st.session_state.piece_x + 1
        if not check_collision(st.session_state.board, st.session_state.piece, nx, st.session_state.piece_y):
            st.session_state.piece_x = nx
    if st.session_state.rotate:
        rotated = rotate_clockwise(st.session_state.piece)
        if not check_collision(st.session_state.board, rotated, st.session_state.piece_x, st.session_state.piece_y):
            st.session_state.piece = rotated
    st.session_state.move = None
    st.session_state.rotate = False
    ny = st.session_state.piece_y + 1
    if not check_collision(st.session_state.board, st.session_state.piece, st.session_state.piece_x, ny):
        st.session_state.piece_y = ny
    else:
        merge_piece(st.session_state.board, st.session_state.piece, st.session_state.piece_x, st.session_state.piece_y)
        st.session_state.board, lines = clear_lines(st.session_state.board)
        st.session_state.score += lines * 100
        spawn_piece()
st.title("Tetris")
st.write(f"Score: {st.session_state.score}")
if st.session_state.game_over:
    st.error("Game Over")
else:
    display = [row[:] for row in st.session_state.board]
    piece = st.session_state.piece
    for r, row in enumerate(piece):
        for c, val in enumerate(row):
            if val:
                y = st.session_state.piece_y + r
                x = st.session_state.piece_x + c
                if 0 <= y < 20 and 0 <= x < 10:
                    display[y][x] = "🟦"
    board_str = "\n".join("".join(cell for cell in row) for row in display)
    st.code(board_str, language="text")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("←", key="left_btn"):
            st.session_state.move = "LEFT"
    with col2:
        if st.button("⟳", key="rotate_btn"):
            st.session_state.rotate = True
    with col3:
        if st.button("→", key="right_btn"):
            st.session_state.move = "RIGHT"
if st.button("Restart", key="restart_btn"):
    st.session_state.board = [["⬛" for _ in range(10)] for _ in range(20)]
    st.session_state.piece = None
    st.session_state.piece_x = 3
    st.session_state.piece_y = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.move = None
    st.session_state.rotate = False
    st.rerun()