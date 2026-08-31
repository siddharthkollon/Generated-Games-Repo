import streamlit as st
from streamlit_autorefresh import st_autorefresh
import random
import copy
st_autorefresh(interval=200, key="game_loop_ticker")
if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(10)] for _ in range(20)]
if 'shape_id' not in st.session_state:
    st.session_state.shape_id = 0
if 'rotation' not in st.session_state:
    st.session_state.rotation = 0
if 'pos_x' not in st.session_state:
    st.session_state.pos_x = 3
if 'pos_y' not in st.session_state:
    st.session_state.pos_y = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'move_left' not in st.session_state:
    st.session_state.move_left = False
if 'move_right' not in st.session_state:
    st.session_state.move_right = False
if 'rotate' not in st.session_state:
    st.session_state.rotate = False
if 'fast_drop' not in st.session_state:
    st.session_state.fast_drop = False
if 'tick' not in st.session_state: