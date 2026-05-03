# HuggingFace Space: Dr-P/satact-app
# Live URL: https://dr-p-satact-app.hf.space

import re
import requests
import random
import gradio as gr

PORTAL_VERIFY_URL = "https://web-production-202b9.up.railway.app/api/verify"
TOKEN_PATTERN = re.compile(r"^FLAB-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", re.IGNORECASE)
FREE_Q_LIMIT = 10

def verify_token(token: str) -> bool:
    token = token.strip().upper()
    if not TOKEN_PATTERN.match(token):
        return False
    try:
        r = requests.post(PORTAL_VERIFY_URL, json={"token": token}, timeout=5)
        if r.status_code == 200 and r.json().get("valid"):
            return True
    except Exception:
        pass
    return False

QUESTIONS = [
    # Heart of Algebra
    {"q": "If 3x + 7 = 22, what is the value of 6x - 4?",
     "choices": ["A) 26", "B) 30", "C) 10", "D) 15"],
     "answer": 0, "topic": "Heart of Algebra",
     "explanation": "3x + 7 = 22 → 3x = 15 → x = 5. Then 6(5) - 4 = 30 - 4 = 26."},
    {"q": "A line passes through (2, 5) and has slope 3. Which equation represents this line?",
     "choices": ["A) y = 3x - 1", "B) y = 3x + 1", "C) y = 3x + 5", "D) y = 3x - 5"],
     "answer": 0, "topic": "Heart of Algebra",
     "explanation": "y - 5 = 3(x - 2) → y = 3x - 6 + 5 → y = 3x - 1."},
    {"q": "If |2x - 6| = 10, what are the two solutions for x?",
     "choices": ["A) x = 8 or x = -2", "B) x = 8 or x = 2", "C) x = 10 or x = -2", "D) x = 6 or x = -6"],
     "answer": 0, "topic": "Heart of Algebra",
     "explanation": "2x - 6 = 10 → x = 8; or 2x - 6 = -10 → x = -2. Solutions: x = 8 or x = -2."},
    {"q": "A system of equations: 2x + y = 10 and x - y = 2. What is x + y?",
     "choices": ["A) 6", "B) 8", "C) 4", "D) 10"],
     "answer": 0, "topic": "Heart of Algebra",
     "explanation": "Adding the equations: 3x = 12 → x = 4. Substituting into x - y = 2: y = 2. So x + y = 4 + 2 = 6."},
    {"q": "Which inequality is equivalent to -3x + 6 > 12?",
     "choices": ["A) x > -2", "B) x < -2", "C) x > 2", "D) x < 2"],
     "answer": 1, "topic": "Heart of Algebra",
     "explanation": "-3x > 6 → x < -2. Remember: dividing by a negative flips the inequality sign."},
    {"q": "A store sells apples for $1.50 each and oranges for $0.75 each. Maria spends $9.00 buying 8 fruits total. How many apples did she buy?",
     "choices": ["A) 2", "B) 4", "C) 6", "D) 3"],
     "answer": 1, "topic": "Heart of Algebra",
     "explanation": "Let a = apples. 1.50a + 0.75(8-a) = 9.00 → 0.75a + 6 = 9 → 0.75a = 3 → a = 4."},
    # Passport to Advanced Math
    {"q": "Which of the following is equivalent to (x² - 9)/(x - 3) for x ≠ 3?",
     "choices": ["A) x + 3", "B) x - 3", "C) x² + 3", "D) (x-3)²"],
     "answer": 0, "topic": "Passport to Advanced Math",
     "explanation": "x² - 9 = (x-3)(x+3). So (x²-9)/(x-3) = (x+3) for x ≠ 3."},
    {"q": "If f(x) = 2x² - 3x + 1, what is f(-2)?",
     "choices": ["A) 15", "B) 7", "C) 11", "D) 3"],
     "answer": 0, "topic": "Passport to Advanced Math",
     "explanation": "f(-2) = 2(4) - 3(-2) + 1 = 8 + 6 + 1 = 15."},
    {"q": "Solve for x: x² - 5x + 6 = 0",
     "choices": ["A) x = 2 or x = 3", "B) x = -2 or x = -3", "C) x = 1 or x = 6", "D) x = 2 or x = -3"],
     "answer": 0, "topic": "Passport to Advanced Math",
     "explanation": "Factor: (x-2)(x-3) = 0. Solutions: x = 2 or x = 3."},
    {"q": "The graph of y = (x - 4)² + 3 has its vertex at:",
     "choices": ["A) (-4, 3)", "B) (4, 3)", "C) (4, -3)", "D) (-4, -3)"],
     "answer": 1, "topic": "Passport to Advanced Math",
     "explanation": "Vertex form y = (x-h)² + k has vertex at (h, k). Here h = 4, k = 3, so vertex is (4, 3)."},
    {"q": "If 2^(x+1) = 32, what is x?",
     "choices": ["A) 4", "B) 5", "C) 6", "D) 3"],
     "answer": 0, "topic": "Passport to Advanced Math",
     "explanation": "2^(x+1) = 32 = 2^5. So x + 1 = 5, thus x = 4."},
    {"q": "What is the sum of the solutions to x² - 7x + 10 = 0?",
     "choices": ["A) 7", "B) 10", "C) -7", "D) -10"],
     "answer": 0, "topic": "Passport to Advanced Math",
     "explanation": "By Vieta's formulas, sum of roots = -b/a = 7/1 = 7. (Roots are x=2 and x=5, sum=7.)"},
    # Problem Solving & Data Analysis
    {"q": "A data set has values: 4, 7, 7, 9, 13. What is the median?",
     "choices": ["A) 7", "B) 8", "C) 9", "D) 7.5"],
     "answer": 0, "topic": "Problem Solving & Data Analysis",
     "explanation": "Ordered: 4, 7, 7, 9, 13. Middle value (3rd of 5) = 7."},
    {"q": "A car travels 240 miles in 4 hours. At the same rate, how far will it travel in 6.5 hours?",
     "choices": ["A) 360 miles", "B) 390 miles", "C) 340 miles", "D) 420 miles"],
     "answer": 1, "topic": "Problem Solving & Data Analysis",
     "explanation": "Rate = 240/4 = 60 mph. Distance = 60 × 6.5 = 390 miles."},
    {"q": "A shirt originally costs $80 and is discounted 25%, then taxed 8%. What is the final price?",
     "choices": ["A) $62.00", "B) $64.80", "C) $66.00", "D) $60.00"],
     "answer": 1, "topic": "Problem Solving & Data Analysis",
     "explanation": "After 25% off: $80 × 0.75 = $60. After 8% tax: $60 × 1.08 = $64.80."},
    {"q": "In a class of 30 students, 18 play soccer and 12 play basketball. 6 play both. How many play neither?",
     "choices": ["A) 0", "B) 6", "C) 12", "D) 4"],
     "answer": 1, "topic": "Problem Solving & Data Analysis",
     "explanation": "By inclusion-exclusion: n(soccer ∪ basketball) = 18 + 12 - 6 = 24. Neither = 30 - 24 = 6."},
    {"q": "A scatter plot shows a correlation coefficient of r = -0.85. This indicates:",
     "choices": ["A) Strong positive correlation",
                 "B) Weak negative correlation",
                 "C) Strong negative correlation",
                 "D) No correlation"],
     "answer": 2, "topic": "Problem Solving & Data Analysis",
     "explanation": "|r| = 0.85 is close to 1, indicating strong correlation. Negative r means as one variable increases, the other decreases."},
    {"q": "A population grows from 5,000 to 6,500 in one year. What is the percent increase?",
     "choices": ["A) 13%", "B) 23%", "C) 30%", "D) 20%"],
     "answer": 2, "topic": "Problem Solving & Data Analysis",
     "explanation": "% increase = (6500 - 5000)/5000 × 100 = 1500/5000 × 100 = 30%."},
    # Geometry & Trigonometry
    {"q": "A circle has diameter 10 cm. What is the area? (Use π ≈ 3.14)",
     "choices": ["A) 31.4 cm²", "B) 78.5 cm²", "C) 314 cm²", "D) 62.8 cm²"],
     "answer": 1, "topic": "Geometry & Trigonometry",
     "explanation": "Radius r = 5 cm. Area = πr² = 3.14 × 25 = 78.5 cm²."},
    {"q": "In a right triangle with legs 5 and 12, what is the length of the hypotenuse?",
     "choices": ["A) 13", "B) 15", "C) 17", "D) 11"],
     "answer": 0, "topic": "Geometry & Trigonometry",
     "explanation": "By Pythagorean theorem: c² = 5² + 12² = 25 + 144 = 169. c = 13."},
    {"q": "What is sin(30°)?",
     "choices": ["A) √3/2", "B) 1/2", "C) √2/2", "D) 1"],
     "answer": 1, "topic": "Geometry & Trigonometry",
     "explanation": "sin(30°) = 1/2. Key values: sin(30°)=1/2, sin(45°)=√2/2, sin(60°)=√3/2."},
    {"q": "Two parallel lines are cut by a transversal. If one interior angle is 65°, what is the co-interior (same-side interior) angle?",
     "choices": ["A) 65°", "B) 115°", "C) 125°", "D) 25°"],
     "answer": 1, "topic": "Geometry & Trigonometry",
     "explanation": "Co-interior (same-side interior) angles are supplementary: they add to 180°. So 180° - 65° = 115°."},
    {"q": "A rectangular prism has dimensions 4 cm × 6 cm × 3 cm. What is its surface area?",
     "choices": ["A) 108 cm²", "B) 72 cm²", "C) 144 cm²", "D) 54 cm²"],
     "answer": 0, "topic": "Geometry & Trigonometry",
     "explanation": "SA = 2(lw + lh + wh) = 2(24 + 12 + 18) = 2(54) = 108 cm²."},
    {"q": "In triangle ABC, angle A = 40°, angle B = 75°. What is angle C?",
     "choices": ["A) 65°", "B) 75°", "C) 55°", "D) 45°"],
     "answer": 0, "topic": "Geometry & Trigonometry",
     "explanation": "Sum of interior angles = 180°. C = 180° - 40° - 75° = 65°."},
    # Reading & Writing Strategy
    {"q": "In SAT Reading, the author's primary purpose in a passage is best identified by examining:",
     "choices": ["A) The first sentence only",
                 "B) The overall argument and recurring themes across the passage",
                 "C) The longest paragraph",
                 "D) Any statistics mentioned"],
     "answer": 1, "topic": "Reading & Writing Strategy",
     "explanation": "Author's purpose requires understanding the whole passage — its central claim, recurring ideas, and how evidence is used throughout."},
    {"q": "Which sentence uses the correct punctuation for a parenthetical phrase?",
     "choices": ["A) The experiment, which took three days was a success.",
                 "B) The experiment, which took three days, was a success.",
                 "C) The experiment which took three days, was a success.",
                 "D) The experiment which took three days was a success."],
     "answer": 1, "topic": "Reading & Writing Strategy",
     "explanation": "A nonrestrictive (parenthetical) clause is set off by commas on both sides: 'The experiment, which took three days, was a success.'"},
    {"q": "A student wants to add a sentence that introduces evidence for the claim 'Exercise improves cognition.' Which is the BEST supporting sentence?",
     "choices": ["A) Many people enjoy exercising outdoors.",
                 "B) A 2023 meta-analysis found aerobic exercise increases hippocampal volume by 2% in adults.",
                 "C) Exercise has been popular throughout human history.",
                 "D) Some researchers disagree about the benefits of exercise."],
     "answer": 1, "topic": "Reading & Writing Strategy",
     "explanation": "Specific, cited evidence (meta-analysis with a quantitative finding) directly supports the claim. General or vague statements do not."},
    {"q": "Which transition word best connects these sentences: 'The drug reduced symptoms in 80% of patients. ___, it had significant side effects.'",
     "choices": ["A) Furthermore", "B) Therefore", "C) However", "D) Similarly"],
     "answer": 2, "topic": "Reading & Writing Strategy",
     "explanation": "'However' signals a contrast — the benefit vs. the side effects. 'Furthermore' adds information; 'Therefore' shows consequence; 'Similarly' shows likeness."},
    {"q": "In ACT English, when should you use a semicolon?",
     "choices": ["A) Before a coordinating conjunction in a compound sentence",
                 "B) Between two independent clauses without a conjunction",
                 "C) After an introductory clause",
                 "D) Before a list of items"],
     "answer": 1, "topic": "Reading & Writing Strategy",
     "explanation": "A semicolon joins two independent clauses without a coordinating conjunction: 'She studied hard; she aced the test.'"},
    {"q": "A passage states: 'Sales increased 15% after the campaign.' The author then adds 'correlation does not imply causation.' This addition serves to:",
     "choices": ["A) Undermine the passage's entire argument",
                 "B) Qualify the claim by acknowledging alternative explanations",
                 "C) Provide additional statistical support",
                 "D) Shift the topic to a different subject"],
     "answer": 1, "topic": "Reading & Writing Strategy",
     "explanation": "Acknowledging that correlation ≠ causation qualifies (limits) the claim rather than refuting it, showing intellectual honesty about alternative explanations."},
]

CSS = """
body, .gradio-container { background: #0a1628 !important; color: #f0ebe0 !important; font-family: 'Georgia', serif; }
h1, h2, h3 { color: #c9a84c !important; }
.gr-button-primary { background: #c9a84c !important; color: #0a1628 !important; font-weight: bold; border: none; }
.gr-button { border: 1px solid #c9a84c !important; color: #c9a84c !important; background: transparent !important; }
.gr-textbox, .gr-radio, .gr-box { background: #0d1f3c !important; color: #f0ebe0 !important; border-color: #c9a84c !important; }
label { color: #f0ebe0 !important; }
.authority { color: #c9a84c; font-size: 0.85em; text-align: center; margin-top: 4px; }
"""

def new_session():
    shuffled = random.sample(QUESTIONS, len(QUESTIONS))
    return {"token_verified": False, "q_idx": 0, "score": 0, "answers": [], "free_used": 0, "questions": shuffled}

def get_question(session):
    qs = session["questions"]
    idx = session["q_idx"]
    if idx >= len(qs):
        return None
    return qs[idx]

def fmt_score(session):
    return f"Score: {session['score']} / {session['q_idx']}" if session["q_idx"] > 0 else "Score: 0 / 0"

def submit_answer(choice_idx, session):
    if choice_idx is None:
        return session, "Please select an answer.", gr.update(), gr.update(visible=False), fmt_score(session)
    q = get_question(session)
    if q is None:
        return session, "Quiz complete!", gr.update(), gr.update(visible=False), fmt_score(session)
    correct = choice_idx == q["answer"]
    if correct:
        session["score"] += 1
    session["q_idx"] += 1
    if not session["token_verified"]:
        session["free_used"] += 1
    session["answers"].append(correct)
    result_icon = "Correct!" if correct else f"Incorrect. Correct answer: {q['choices'][q['answer']]}"
    feedback = f"**{result_icon}**\n\n{q['explanation']}"
    return session, feedback, gr.update(), gr.update(visible=True), fmt_score(session)

def next_question(session):
    if not session["token_verified"] and session["free_used"] >= FREE_Q_LIMIT:
        paywall_msg = (
            "**You have reached the free limit of 10 questions.**\n\n"
            "Unlock unlimited practice with a FissionLab Premium subscription:\n\n"
            "- **Monthly**: [Upgrade Now](https://buy.stripe.com/5kQfZadJAbnQ5OagjU1Fe09)\n"
            "- **Annual**: [Best Value](https://buy.stripe.com/7sY14g20SeA2ccy9Vw1Fe0a)\n\n"
            "Already have a token? Enter it in the **Unlock Premium** tab."
        )
        return session, paywall_msg, gr.update(choices=[], value=None, interactive=False), gr.update(visible=False), fmt_score(session)
    q = get_question(session)
    if q is None:
        total = session["q_idx"]
        score = session["score"]
        return session, f"**Quiz complete! Final score: {score}/{total}**\n\nRefresh the page to start a new quiz.", gr.update(choices=[], value=None, interactive=False), gr.update(visible=False), fmt_score(session)
    return session, "", gr.update(choices=q["choices"], value=None, interactive=True, label=f"Q{session['q_idx']+1}: {q['q']}"), gr.update(visible=False), fmt_score(session)

def verify_token_action(token, session):
    if verify_token(token):
        session["token_verified"] = True
        return session, "**Premium unlocked! Enjoy unlimited practice.**"
    return session, "**Invalid token.** Check your token format (FLAB-XXXX-XXXX-XXXX) or purchase a subscription."

with gr.Blocks(css=CSS, title="FissionLab SAT/ACT Practice — Dr. Preston PhD") as demo:
    session_state = gr.State(new_session())

    gr.Markdown("# FissionLab SAT/ACT Practice App — Dr. Preston PhD")
    gr.Markdown(
        "<div class='authority'>Dr. Preston — PhD Nuclear Engineering AFIT · B.A. Physics UC Berkeley · USAF Captain · LLNL/LBNL</div>"
    )

    with gr.Tabs():
        with gr.Tab("Practice Quiz"):
            score_display = gr.Markdown("Score: 0 / 0")
            q_radio = gr.Radio(choices=[], label="Loading first question...", interactive=True)
            with gr.Row():
                submit_btn = gr.Button("Submit Answer", variant="primary")
                next_btn = gr.Button("Next Question", visible=False)
            feedback_box = gr.Markdown("")

        with gr.Tab("Unlock Premium"):
            gr.Markdown("## Unlock Unlimited Practice")
            gr.Markdown(
                "The free tier includes **10 questions**. Upgrade for unlimited access to all topics, "
                "detailed explanations, and score tracking.\n\n"
                "### Subscribe\n"
                "- **Monthly Plan**: [Upgrade Now](https://buy.stripe.com/5kQfZadJAbnQ5OagjU1Fe09)\n"
                "- **Annual Plan (Best Value)**: [Upgrade Now](https://buy.stripe.com/7sY14g20SeA2ccy9Vw1Fe0a)\n\n"
                "### Already have a token?\n"
            )
            token_input = gr.Textbox(label="Enter your token (FLAB-XXXX-XXXX-XXXX)", placeholder="FLAB-XXXX-XXXX-XXXX")
            verify_btn = gr.Button("Verify Token", variant="primary")
            verify_status = gr.Markdown("")

    demo.load(next_question, inputs=[session_state],
              outputs=[session_state, feedback_box, q_radio, next_btn, score_display])

    submit_btn.click(submit_answer, inputs=[q_radio, session_state],
                     outputs=[session_state, feedback_box, q_radio, next_btn, score_display])
    next_btn.click(next_question, inputs=[session_state],
                   outputs=[session_state, feedback_box, q_radio, next_btn, score_display])
    verify_btn.click(verify_token_action, inputs=[token_input, session_state],
                     outputs=[session_state, verify_status])

if __name__ == "__main__":
    demo.launch()
