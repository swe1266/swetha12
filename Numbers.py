import streamlit as st
import random
import math
import operator 

# Title for the Game
st.title("🎲 Fun Math-Based Guessing Game!")

# Initialize session state variables
if 'game_active' not in st.session_state:
    st.session_state.game_active = False
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'optimal_attempts' not in st.session_state:
    st.session_state.optimal_attempts = 0
if 'computer_guess' not in st.session_state:
    st.session_state.computer_guess = None
if 'start_range' not in st.session_state:
    st.session_state.start_range = None
if 'end_range' not in st.session_state:
    st.session_state.end_range = None

# Define basic operations for hints
operations = {
    "+": operator.add,
    "-": operator.sub,
    "*": operator.mul,
    "%": operator.mod  # Modulo to give remainder
}

# Function to calculate optimal attempts
def calculate_optimal_attempts(start, end):
    return math.ceil(math.log2(end - start + 1))

# Function to generate a hint
def generate_hint(secret_number, guess):
    op_symbol, op_func = random.choice(list(operations.items()))
    try:
        result = op_func(secret_number, guess)
    except ZeroDivisionError:
        result = op_func(secret_number, guess + 1)  # Handle division by zero for %
    return f"Hint: {secret_number} {op_symbol} {guess} = {result}"

# Function to reset game
def reset_game():
    st.session_state.game_active = False
    st.session_state.secret_number = None
    st.session_state.attempts = 0
    st.session_state.computer_guess = None
    st.session_state.start_range = None
    st.session_state.end_range = None

# Game mode selection and rules
game_mode = st.radio("Choose your game mode:", ["User Guessing", "Computer Guessing"])

if game_mode == "User Guessing":
    st.markdown("""
    ### 📜 Rules for User Guessing Mode:
    1. Set your number range.
    2. The computer will pick a secret number.
    3. Try to guess the number.
    4. After each guess, you'll get a mathematical hint to help you find the number.
    """)
else:
    st.markdown("""
    ### 📜 Rules for Computer Guessing Mode:
    1. Set your number range.
    2. Think of a secret number within this range.
    3. The computer will try to guess it.
    4. Give the computer hints using mathematical operations to help it find your number.
    """)

# Set up range and start game
if not st.session_state.game_active:
    col1, col2 = st.columns(2)
    with col1:
        start = st.number_input("Start number:", value=1)
    with col2:
        end = st.number_input("End number:", value=100)
    
    if st.button("Start Game!"):
        st.session_state.game_active = True
        st.session_state.start_range = start
        st.session_state.end_range = end
        st.session_state.optimal_attempts = calculate_optimal_attempts(start, end)
        
        if game_mode == "User Guessing":
            st.session_state.secret_number = random.randint(start, end)
        else:
            st.session_state.computer_guess = (start + end) // 2  # Start with middle number
        st.rerun()

# User Guessing Mode
if game_mode == "User Guessing" and st.session_state.game_active:
    st.info(f"Try to guess in {st.session_state.optimal_attempts} attempts for a perfect score!")
    
    guess = st.number_input("Enter your guess:", min_value=st.session_state.start_range, max_value=st.session_state.end_range)
    
    if st.button("Submit Guess"):
        st.session_state.attempts += 1
        
        if guess == st.session_state.secret_number:
            st.balloons()
            st.success(f"🎉 You guessed the number in {st.session_state.attempts} attempts!")
        else:
            hint = generate_hint(st.session_state.secret_number, guess)
            st.warning(hint)

# Computer Guessing Mode
if game_mode == "Computer Guessing" and st.session_state.game_active:
    st.write(f"Computer's guess: {st.session_state.computer_guess}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Too Low"):
            st.session_state.attempts += 1
            start = st.session_state.computer_guess + 1
            end = st.session_state.end_range
            st.session_state.computer_guess = (start + end) // 2
            st.session_state.start_range = start
            st.rerun()
    with col2:
        if st.button("Too High"):
            st.session_state.attempts += 1
            start = st.session_state.start_range
            end = st.session_state.computer_guess - 1
            st.session_state.computer_guess = (start + end) // 2
            st.session_state.end_range = end
            st.rerun()
    with col3:
        if st.button("Correct!"):
            st.balloons()
            st.success(f"Computer guessed the number in {st.session_state.attempts + 1} attempts!")

# Reset button
if st.session_state.game_active:
    if st.button("Play Again"):
        reset_game()
        st.rerun()
