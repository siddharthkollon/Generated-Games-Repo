import streamlit as st
if 'board' not in st.session_state:
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
if 'turn' not in st.session_state:
    st.session_state.turn = "X"
if 'winner' not in st.session_state:
    st.session_state.winner = ""
if 'x_score' not in st.session_state:
    st.session_state.x_score = 0
if 'o_score' not in st.session_state:
    st.session_state.o_score = 0
if 'draw_score' not in st.session_state:
    st.session_state.draw_score = 0
def check_winner(board):
    lines = []
    lines.extend(board)
    lines.extend([[board[r][c] for r in range(3)] for c in range(3)])
    lines.append([board[i][i] for i in range(3)])
    lines.append([board[i][2 - i] for i in range(3)])
    for line in lines:
        if line[0] != "" and line.count(line[0]) == 3:
            return line[0]
    if all(board[r][c] != "" for r in range(3) for c in range(3)):
        return "Draw"
    return ""
def render_board():
    display = [["⬜" if cell == "" else ("❌" if cell == "X" else "⭕") for cell in row] for row in st.session_state.board]
    board_str = "\n".join("".join(row) for row in display)
    st.code(board_str, language="text")
for r in range(3):
    cols = st.columns(3)
    for c in range(3):
        with cols[c]:
            if st.session_state.board[r][c] == "" and st.session_state.winner == "":
                if st.button(" ", key=f"cell_{r}_{c}"):
                    st.session_state.board[r][c] = st.session_state.turn
                    st.session_state.winner = check_winner(st.session_state.board)
                    if st.session_state.winner == "X":
                        st.session_state.x_score += 1
                    elif st.session_state.winner == "O":
                        st.session_state.o_score += 1
                    elif st.session_state.winner == "Draw":
                        st.session_state.draw_score += 1
                    else:
                        st.session_state.turn = "O" if st.session_state.turn == "X" else "X"
render_board()
st.write(f"Turn: {'❌' if st.session_state.turn == 'X' else '⭕'}")
if st.session_state.winner != "":
    if st.session_state.winner == "Draw":
        st.success("It's a draw!")
    else:
        st.success(f"{'❌' if st.session_state.winner == 'X' else '⭕'} wins!")
st.write(f"Score - ❌: {st.session_state.x_score}  ⭕: {st.session_state.o_score}  Draws: {st.session_state.draw_score}")
if st.button("Restart Game", key="restart_button"):
    st.session_state.board = [["" for _ in range(3)] for _ in range(3)]
    st.session_state.turn = "X"
    st.session_state.winner = ""