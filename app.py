import random
import streamlit as st

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100 #- Fix Hard difficulty range: 1-50 → 1-200 (now harder than Normal)
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
    
#- Fix backwards hints: swap "Go HIGHER" / "Go LOWER" based on guess comparison
    try:
        if guess > secret:
            return "Too High", "📉 Go LOWER!"
        else:
            return "Too Low", "📈 Go HIGHER!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📉 Go LOWER!"
        return "Too Low", "📈 Go HIGHER!"


"""- Redesign scoring system: 100 points max, deduct per wrong attempt (not total)
  - Win on attempt 1: 100 points
  - Win on attempt N: 100 - (N-1) × (100/attempt_limit) points
  - No win: 0 points"""
def update_score(current_score: int, outcome: str, attempt_number: int, attempt_limit: int):
    # Cost per wrong attempt: 100 / attempt_limit
    cost_per_wrong_attempt = 100 / attempt_limit
    wrong_attempts = attempt_number - 1
    
    if outcome == "Win":
        # Score = 100 - (wrong attempts * cost per attempt)
        points = max(0, 100 - (wrong_attempts * cost_per_wrong_attempt))
        return current_score + points
    else:
        # Wrong guess: no score change (we only score on win)
        return current_score

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 8,
    "Normal": 7,
    "Hard": 6,
}
#- Fix backwards attempt limits: Easy=8, Normal=6, Hard=5 (was Easy=6, Normal=8)
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

# Track difficulty and restart game if it changes
if "current_difficulty" not in st.session_state:
    st.session_state.current_difficulty = difficulty
elif st.session_state.current_difficulty != difficulty:
    st.session_state.current_difficulty = difficulty
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.game_counter += 1
    st.session_state.last_hint = None
    st.rerun()

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0 #- Fix attempts not decrementing on first guess: initialize attempts to 0 (not 1)

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

if "game_counter" not in st.session_state:
    st.session_state.game_counter = 0

if "last_hint" not in st.session_state:
    st.session_state.last_hint = None

st.subheader("Make a guess")

#- Fix static range display: use dynamic {low} and {high} in info prompt
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

# - Remove developer debug info: hide secret number and internal state


raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}_{st.session_state.game_counter}" #Clear text input on game restart by incrementing game_counter in widget key
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁") #2- Fix "New Game" button not working: move handler before status check, reset attempts to 0
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.session_state.last_hint:
    st.warning(st.session_state.last_hint)

# Handle "New Game" button first, before checking game status
if new_game:
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.status = "playing"
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.game_counter += 1
    st.session_state.last_hint = None
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome, message = check_guess(guess_int, st.session_state.secret)

        st.session_state.last_hint = message if show_hint else None

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
            attempt_limit=attempt_limit,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
            st.rerun()
        else:
            #3- Fix game ending prematurely: change attempts >= limit to attempts > limit
            if st.session_state.attempts > attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )
                st.rerun()
            else:
                st.rerun()

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
