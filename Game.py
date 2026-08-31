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
    st.session_state.piece_x = WIDTH //