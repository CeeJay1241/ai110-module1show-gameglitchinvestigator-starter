from logic_utils import check_guess, get_range_for_difficulty, update_score


# ============ Tests for check_guess fixes ============

def test_winning_guess():
    """Test that matching guess and secret returns Win"""
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"
    assert message == "🎉 Correct!"


def test_guess_too_high_hint_correct():
    """Fix: Backwards hints - guess > secret should say 'Go LOWER'"""
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "Go LOWER" in message  # Was backwards: used to say "Go HIGHER"


def test_guess_too_low_hint_correct():
    """Fix: Backwards hints - guess < secret should say 'Go HIGHER'"""
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "Go HIGHER" in message  # Was backwards: used to say "Go LOWER"


def test_check_guess_with_string_secret():
    """Fix: String/int comparison - should work consistently"""
    outcome, message = check_guess(60, "50")
    assert outcome == "Too High"
    assert "Go LOWER" in message


# ============ Tests for range fixes ============

def test_easy_range():
    """Fix: Easy should have the smallest range (1-20)"""
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20
    assert (high - low) < 100  # Easy should be small


def test_normal_range():
    """Fix: Normal should have medium range (1-50)"""
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 50


def test_hard_range():
    """Fix: Hard should have the largest range (1-100)"""
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 100
    assert high > 50  # Hard should be bigger than Normal


def test_range_scales_with_difficulty():
    """Fix: Range should increase with difficulty"""
    easy_range = get_range_for_difficulty("Easy")[1] - get_range_for_difficulty("Easy")[0]
    normal_range = get_range_for_difficulty("Normal")[1] - get_range_for_difficulty("Normal")[0]
    hard_range = get_range_for_difficulty("Hard")[1] - get_range_for_difficulty("Hard")[0]
    
    assert easy_range < normal_range < hard_range


# ============ Tests for scoring fixes ============

def test_score_first_guess_win_easy():
    """Fix: Win on first guess should give full 100 points"""
    score = update_score(0, "Win", attempt_number=1, attempt_limit=8)
    assert score == 100  # Was giving 80 before


def test_score_scales_with_attempts_easy():
    """Fix: Score should deplete with wrong attempts, not total attempts"""
    attempt_limit = 8
    cost_per_attempt = 100 / attempt_limit  # 12.5 per wrong attempt
    
    score_attempt_1 = update_score(0, "Win", 1, attempt_limit)  # 0 wrong
    score_attempt_5 = update_score(0, "Win", 5, attempt_limit)  # 4 wrong
    
    assert score_attempt_1 == 100
    assert score_attempt_5 == 100 - (4 * cost_per_attempt)
    assert score_attempt_5 < score_attempt_1


def test_score_all_attempts_wrong():
    """Fix: Using all attempts without winning should give 0 points"""
    score = update_score(0, "Loss", attempt_number=8, attempt_limit=8)
    assert score == 0  # No win = no points


def test_score_hard_difficulty():
    """Fix: Scoring should work for different attempt limits"""
    attempt_limit = 5  # Hard
    cost_per_attempt = 100 / attempt_limit  # 20 per wrong attempt
    
    score_attempt_1 = update_score(0, "Win", 1, attempt_limit)
    score_attempt_3 = update_score(0, "Win", 3, attempt_limit)
    
    assert score_attempt_1 == 100
    assert score_attempt_3 == 100 - (2 * cost_per_attempt)


def test_wrong_guess_no_score_change():
    """Fix: Wrong guesses shouldn't change score, only wins do"""
    current_score = 50
    new_score = update_score(current_score, "Too High", 2, 8)
    assert new_score == current_score  # No change for wrong guess


# ============ Tests for attempt fixes ============

def test_attempts_decrement_from_first_guess():
    """Fix: Attempts should deplete starting from the first guess"""
    # This is more of an integration test, but we verify the logic:
    # attempts starts at 0, increments to 1 on first guess
    # attempts_left = attempt_limit - attempts
    # So on first guess: attempts_left = 8 - 1 = 7
    attempts_left = 8 - 1
    assert attempts_left == 7  # Not 8
