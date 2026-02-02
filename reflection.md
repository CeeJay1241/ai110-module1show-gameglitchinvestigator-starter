# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").

--- The game appeared to look fine at first, and then I started playing...
    1 The hints were backwards. I expected the hint to  try to get me to make a guess closer to the secret number, instead it was taking me further away.
    2 I couldn't restart the game. I had to reload the page. Everytime I clicked on "New Game", instead of the game restarting, nothing would happen 
    3 When attempt left is 1, the game ends
    4 "Easy" has less attempts than "Normal"
    5 The range is supposed to reduce the easier you set the game to be, however the it remains the same. The prompt doesn't change either.
    6. Hard has an easier range (1-50), than normal
    5 Developer debug info is visible; it shouldn't be.
    7 The scoring system is wrong. Even when I get it on the first try, I don't get the full score.
    8 When the game restarts, the answer bar doesn't clear.
    9. When I change the difficulty, the game doesn't restart.
    
## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
Agent

- Give one example of an AI suggestion you accepted and why.
When I said the scoring was wrong, Agent initially suggested a simple fix to the formula. But when I clarified "each guess should carry equal points, and if I use up all my guesses I'd have a score of zero," Agent redesigned the entire scoring logic to:
Calculate cost per attempt: 100 / attempt_limit
Only deduct for wrong attempts, not total attempts
Win on attempt 1 = 100 points; attempt 5 = 100 minus penalties

- Give one example of an AI suggestion you changed or rejected and why.
Rejected: Just add st.rerun() everywhere
Agent suggested calling st.rerun() after every guess to fix the attempts counter. But that broke hints—they'd disappear because reruns wipe transient UI. Instead, I stored hints in session state so they'd persist. The lesson: sometimes you need smarter state management, not just brute-force reruns.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
I tested manually in the Streamlit app by playing the game repeatedly. For each fix, I'd verify the specific behavior: I changed difficulties and confirmed the game restarted with the right range, I made guesses and watched the attempts counter, I checked if hints matched the actual guess direction, and I played to completion to verify scoring. If the issue stopped happening, the bug was fixed.
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
I manually tested the scoring system by winning on my first guess and checking if I got 100 points—before the fix I got 80. Then I made 5 guesses to win on an Easy level and verified the score was 100 - (4 wrong attempts × 12.5) = 50 points. This proved the fix worked: score now depends only on wrong attempts, not total attempts. Later, I ran pytest tests that Agent created, which confirmed all the edge cases (Hard difficulty, all wrong attempts, etc.) worked correctly.
- Did AI help you design or understand any tests? How?
Yes. After fixing all the bugs, I asked Agent to generate pytest cases targeting the specific bugs we fixed. Agent created 16 comprehensive tests organized by category: hint fixes, range fixes, scoring fixes, and attempt fixes. This helped me verify every change was working correctly without manually testing each scenario.
---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
I kept guessing numbers and the secret seemed to change every time I clicked something—it was infuriating! I eventually realized Streamlit was re-running the entire code every time I interacted with the app, and that included the line that picks a random number. So literally every button click, every text input, would regenerate a new secret. The game was impossible to play because I'd be chasing a moving target.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
I'd say: "Every time you interact with the app—click a button, type something—Streamlit reruns the whole script from the top. It's like hitting 'refresh' on a webpage every single interaction. Session state is like a save file that survives these refreshes. Without it, variables reset every rerun. With it, you can remember important stuff between refreshes—like 'the secret is 50' or 'the player guessed 3 times already.'"
- What change did you make that finally gave the game a stable secret number?
I added a simple check before generating the secret: if "secret" not in st.session_state: followed by creating it. The first time the app runs, it generates and saves the secret. Every rerun after that, it skips generation and just uses the saved one. Only when I explicitly click "New Game" or change difficulty does it generate a new secret. That one condition made the entire game actually playable.


---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
I'm going to start by actually playing or using the app/code before diving into fixes. With this project, I played the game first, noticed concrete bugs, and wrote them down that made it so much easier to communicate exactly what was wrong to the AI. In the future, I'll do that for every project: interact with it, break it intentionally, document the issues, then debug systematically. Also, I'll ask the AI to write tests while fixing bugs having pytest cases saved me from re-introducing old bugs and gave me confidence the fixes actually worked.
- What is one thing you would do differently next time you work with AI on a coding task?
I'd ask the AI to explain why the bug exists before suggesting a fix. Early on, the AI would just say "change this line" and I'd do it, but then the same issue would pop up in a different form. When I started asking "why is this happening?" I got better answers and understood the root cause. Next time, I'll push back more and demand the AI explain the underlying problem, not just slap a band-aid on it.
- In one or two sentences, describe how this project changed the way you think about AI generated code.
AI-generated code looks polished and "works" at first glance, but it often has hidden bugs—you have to test it thoroughly and understand the framework yourself. Working with AI as a debugging partner is powerful, but you're still the one responsible for understanding why things break and how to fix them properly.