import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random

st_autorefresh(interval=200, key="game_loop_ticker")

WIDTH = 10
HEIGHT = 20
EMPTY = 0
EMPTY_EMOJI = "⬛"
PIECES = {
    "I": [
        [(0, 1), (1, 1), (2, 1), (3, 1)],
        [(2, 0), (2, 1), (2, 2), (2, 3)],
    ],
    "O": [
        [(1, 0), (2, 0), (1, 1), (2, 1)],
    ],
    "T": [
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (2, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (1, 2)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
    ],
    "S": [
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(1, 0), (1, 1), (2, 1), (2, 2)],
    ],
    "Z": [
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(2, 0), (1, 1), (2, 1), (1, 2)],
    ],
    "J": [
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (2, 0), (1, 1), (1, 2)],
        [(0, 1), (1, 1), (2, 1), (2, 2)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
    ],
    "L": [
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (2, 2)],
        [(0, 1), (1, 1), (2, 1), (0, 2)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
    ],
}
COLOR_MAP = {
    "I": "🟦",
    "O": "🟨",
    "T": "🟪",
    "S": "🟩",
    "Z": "🟥",
    "J": "🟧",
    "L": "🟫",
}
if "board" not in st.session_state:
    st.session_state.board = [[EMPTY for _ in range(WIDTH)] for _ in range(HEIGHT)]
if "piece_type" not in st.session_state:
    st.session_state.piece_type = None
if "piece_rotation" not in st.session_state:
    st.session_state.piece_rotation = 0
if "piece_x" not in st.session_state:
    st.session_state.piece_x = 0
if "piece_y" not in st.session_state:
    st.session_state.piece_y = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "move_left" not in st.session_state:
    st.session_state.move_left = False
if "move_right" not in st.session_state:
    st.session_state.move_right = False
if "rotate" not in st.session_state:
    st.session_state.rotate = False
if "drop" not in st.session_state:
    st.session_state.drop = False

def spawn_piece():
    st.session_state.piece_type = random.choice(list(PIECES.keys()))
    st.session_state.piece_rotation = 0
    shape = PIECES[st.session_state.piece_type][0]
    min_x = min(x for x, y in shape)
    max_x = max(x for x, y in shape)
    st.session_stat