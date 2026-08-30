import random
import streamlit as st

if "player_score" not in st.session_state:
    st.session_state.player_score = 0
if "computer_score" not in st.session_state:
    st.session_state.computer_score = 0
if "round_result" not in st.session_state:
    st.session_state.round_result = ""
if "player_choice" not in st.session_state:
    st.session_state.player_choice = ""
if "computer_choice" not in st.session_state:
    st.session_state.computer_choice = ""

def decide_winner(player, computer):
    if player == computer:
        return "Tie"
    if (player == "Rock" and computer == "Scissors") or \
       (player == "Paper" and computer == "Rock") or \
       (player == "Scissors" and computer == "Paper"):
        return "Player"
    return "Computer"

def play_round(choice):
    st.session_state.player_choice = choice
    st.session_state.computer_choice = random.choice(["Rock", "Paper", "Scissors"])
    winner = decide_winner(st.session_state.player_choice, st.session_state.computer_choice)
    if winner == "Player":
        st.session_state.player_score += 1
        st.session_state.round_result = "You win!"
    elif winner == "Computer":
        st.session_state.computer_score += 1
        st.session_state.round_result = "Computer wins!"
    else:
        st.session_state.round_result = "It's a tie!"

def reset_game():
    st.session_state.player_score = 0
    st.session_state.computer_score = 0
    st.session_state.round_result = ""
    st.session_state.player_choice = ""
    st.session_state.computer_choice = ""
    st.rerun()

st.title("Rock Paper Scissors")
st.subheader("Score")
st.write(f"**You:** {st.session_state.player_score}  **Computer:** {st.session_state.computer_score}")

col1, col2, col3 = st.columns(3)
with col1:
    st.button("Rock", on_click=play_round, args=("Rock",), key="btn_rock")
with col2:
    st.button("Paper", on_click=play_round, args=("Paper",), key="btn_paper")
with col3:
    st.button("Scissors", on_click=play_round, args=("Scissors",), key="btn_scissors")

if st.session_state.round_result:
    st.subheader("Result")
    st.write(f"You chose **{st.session_state.player_choice}**, computer chose **{st.session_state.computer_choice}**.")
    st.success(st.session_state.round_result)

st.button("Restart Game", on_click=reset_game, key="btn_restart")