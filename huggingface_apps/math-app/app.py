# HuggingFace Space: Dr-P/math-app
# Live URL: https://dr-p-math-app.hf.space

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
        r = requests.get(PORTAL_VERIFY_URL, params={"token": token}, timeout=5)
        if r.status_code == 200 and r.json().get("valid"):
            return True
    except Exception:
        pass
    return False

QUESTIONS = [
    # Limits & Derivatives
    {"q": "What is lim(x→2) of (x² - 4)/(x - 2)?",
     "choices": ["A) 0", "B) 2", "C) 4", "D) Undefined"],
     "answer": 2, "topic": "Limits & Derivatives",
     "explanation": "Factor: (x²-4)/(x-2) = (x+2)(x-2)/(x-2) = x+2. As x→2: limit = 2+2 = 4."},
    {"q": "What is the derivative of f(x) = 3x⁴ - 5x² + 7?",
     "choices": ["A) 12x³ - 10x", "B) 12x³ - 10x + 7", "C) 3x³ - 5x", "D) 12x⁴ - 10x²"],
     "answer": 0, "topic": "Limits & Derivatives",
     "explanation": "Power rule: d/dx(3x⁴) = 12x³, d/dx(-5x²) = -10x, d/dx(7) = 0. So f'(x) = 12x³ - 10x."},
    {"q": "What is the derivative of f(x) = sin(3x)?",
     "choices": ["A) cos(3x)", "B) 3cos(3x)", "C) -3cos(3x)", "D) -cos(3x)"],
     "answer": 1, "topic": "Limits & Derivatives",
     "explanation": "By chain rule: d/dx[sin(u)] = cos(u)·u'. Here u = 3x, u' = 3. So f'(x) = 3cos(3x)."},
    {"q": "Find the critical points of f(x) = x³ - 6x² + 9x + 2.",
     "choices": ["A) x = 1 and x = 3", "B) x = 0 and x = 2", "C) x = 2 and x = 4", "D) x = 3 only"],
     "answer": 0, "topic": "Limits & Derivatives",
     "explanation": "f'(x) = 3x² - 12x + 9 = 3(x² - 4x + 3) = 3(x-1)(x-3) = 0. Critical points: x = 1 and x = 3."},
    {"q": "Using the product rule, what is d/dx[x²·eˣ]?",
     "choices": ["A) 2x·eˣ", "B) x²·eˣ + 2x·eˣ", "C) 2x + eˣ", "D) x²·eˣ"],
     "answer": 1, "topic": "Limits & Derivatives",
     "explanation": "Product rule: (uv)' = u'v + uv'. Here u=x², v=eˣ, u'=2x, v'=eˣ. Result: 2x·eˣ + x²·eˣ."},
    {"q": "What does L'Hôpital's rule apply to?",
     "choices": ["A) Any limit involving a fraction",
                 "B) Limits of the form 0/0 or ∞/∞",
                 "C) Limits at infinity only",
                 "D) Limits involving trig functions only"],
     "answer": 1, "topic": "Limits & Derivatives",
     "explanation": "L'Hôpital's rule applies to indeterminate forms 0/0 or ±∞/±∞. Take the derivative of numerator and denominator separately."},
    # Integration
    {"q": "What is ∫(4x³ - 6x + 2) dx?",
     "choices": ["A) x⁴ - 3x² + 2x + C", "B) 12x² - 6 + C", "C) 4x⁴ - 6x² + 2x + C", "D) x⁴ - 3x² + C"],
     "answer": 0, "topic": "Integration",
     "explanation": "Integrate term by term: ∫4x³dx = x⁴, ∫-6x dx = -3x², ∫2 dx = 2x. Result: x⁴ - 3x² + 2x + C."},
    {"q": "Evaluate ∫₀² (3x²) dx.",
     "choices": ["A) 6", "B) 8", "C) 12", "D) 4"],
     "answer": 1, "topic": "Integration",
     "explanation": "∫3x² dx = x³. Evaluate from 0 to 2: [x³]₀² = 8 - 0 = 8."},
    {"q": "Use substitution to find ∫ 2x·(x² + 1)⁴ dx.",
     "choices": ["A) (x²+1)⁵/5 + C", "B) (x²+1)⁵ + C", "C) 2x(x²+1)⁵/5 + C", "D) (x²+1)⁴/2 + C"],
     "answer": 0, "topic": "Integration",
     "explanation": "Let u = x²+1, du = 2x dx. Integral becomes ∫u⁴ du = u⁵/5 + C = (x²+1)⁵/5 + C."},
    {"q": "Integration by parts: ∫x·eˣ dx = ?",
     "choices": ["A) x·eˣ - eˣ + C", "B) x·eˣ + eˣ + C", "C) eˣ/2 + C", "D) x²·eˣ/2 + C"],
     "answer": 0, "topic": "Integration",
     "explanation": "IBP: ∫u dv = uv - ∫v du. Let u=x, dv=eˣdx → du=dx, v=eˣ. Result: x·eˣ - ∫eˣdx = x·eˣ - eˣ + C."},
    {"q": "The area between y = x² and y = x over [0,1] equals:",
     "choices": ["A) 1/6", "B) 1/3", "C) 1/2", "D) 1/4"],
     "answer": 0, "topic": "Integration",
     "explanation": "Area = ∫₀¹(x - x²)dx = [x²/2 - x³/3]₀¹ = 1/2 - 1/3 = 1/6."},
    {"q": "What is ∫ (1/x) dx for x > 0?",
     "choices": ["A) 1/x² + C", "B) ln|x| + C", "C) -1/x² + C", "D) x·ln(x) + C"],
     "answer": 1, "topic": "Integration",
     "explanation": "∫(1/x)dx = ln|x| + C. This is a fundamental integral result."},
    # Multivariable Calculus
    {"q": "For f(x,y) = x²y + 3y², what is the partial derivative ∂f/∂x?",
     "choices": ["A) 2xy + 6y", "B) 2xy", "C) x² + 6y", "D) 2x"],
     "answer": 1, "topic": "Multivariable Calculus",
     "explanation": "∂f/∂x treats y as constant: ∂/∂x(x²y) = 2xy, ∂/∂x(3y²) = 0. So ∂f/∂x = 2xy."},
    {"q": "The gradient ∇f of f(x,y) = 3x² + 2xy - y² at point (1,1) is:",
     "choices": ["A) (8, 0)", "B) (6, 0)", "C) (8, -1)", "D) (6, 2)"],
     "answer": 0, "topic": "Multivariable Calculus",
     "explanation": "∂f/∂x = 6x+2y = 8, ∂f/∂y = 2x-2y = 0 at (1,1). Gradient = (8, 0)."},
    {"q": "The gradient vector always points in the direction of:",
     "choices": ["A) Maximum decrease of the function",
                 "B) Maximum increase of the function",
                 "C) Zero change (level curves)",
                 "D) The nearest local minimum"],
     "answer": 1, "topic": "Multivariable Calculus",
     "explanation": "The gradient ∇f points in the direction of the steepest ascent (maximum increase). The negative gradient points toward steepest descent."},
    {"q": "Evaluate the double integral ∫₀¹∫₀² xy dy dx.",
     "choices": ["A) 1", "B) 2", "C) 1/2", "D) 4"],
     "answer": 0, "topic": "Multivariable Calculus",
     "explanation": "Inner: ∫₀²xy dy = x[y²/2]₀² = 2x. Outer: ∫₀¹2x dx = [x²]₀¹ = 1."},
    {"q": "The Jacobian of the transformation x = r·cos(θ), y = r·sin(θ) is:",
     "choices": ["A) 1", "B) r", "C) r²", "D) cos(θ)sin(θ)"],
     "answer": 1, "topic": "Multivariable Calculus",
     "explanation": "The Jacobian |∂(x,y)/∂(r,θ)| = r. This is why the area element in polar coordinates is r dr dθ."},
    # Linear Algebra
    {"q": "What is the determinant of the matrix [[3, 1], [2, 4]]?",
     "choices": ["A) 10", "B) 14", "C) 5", "D) 11"],
     "answer": 0, "topic": "Linear Algebra",
     "explanation": "det([[a,b],[c,d]]) = ad - bc = 3·4 - 1·2 = 12 - 2 = 10."},
    {"q": "A matrix A is invertible if and only if:",
     "choices": ["A) It is square",
                 "B) Its determinant is non-zero",
                 "C) All its entries are positive",
                 "D) It is symmetric"],
     "answer": 1, "topic": "Linear Algebra",
     "explanation": "A square matrix A is invertible (non-singular) if and only if det(A) ≠ 0."},
    {"q": "The eigenvalues of [[2, 1], [0, 3]] are:",
     "choices": ["A) 2 and 3", "B) 1 and 3", "C) 2 and 1", "D) 0 and 2"],
     "answer": 0, "topic": "Linear Algebra",
     "explanation": "For an upper/lower triangular matrix, eigenvalues are the diagonal entries: λ₁ = 2, λ₂ = 3."},
    {"q": "The rank of matrix [[1,2,3],[2,4,6],[0,1,2]] is:",
     "choices": ["A) 3", "B) 2", "C) 1", "D) 0"],
     "answer": 1, "topic": "Linear Algebra",
     "explanation": "Row 2 = 2×Row 1 (linearly dependent). After row reduction, we get 2 linearly independent rows. Rank = 2."},
    {"q": "The dot product of vectors u = [3, -1, 2] and v = [1, 4, 0] is:",
     "choices": ["A) -1", "B) 3", "C) 1", "D) 7"],
     "answer": 0, "topic": "Linear Algebra",
     "explanation": "u·v = 3(1) + (-1)(4) + 2(0) = 3 - 4 + 0 = -1."},
    {"q": "Which of the following is NOT a property of linear transformations?",
     "choices": ["A) T(u + v) = T(u) + T(v)",
                 "B) T(cu) = cT(u)",
                 "C) T(uv) = T(u)·T(v) for any u, v",
                 "D) T(0) = 0"],
     "answer": 2, "topic": "Linear Algebra",
     "explanation": "Linear transformations satisfy additivity and scalar multiplication, but T(uv) = T(u)·T(v) is NOT required. That property defines ring homomorphisms."},
    # Differential Equations
    {"q": "What is the general solution to dy/dx = 3y?",
     "choices": ["A) y = Ce^(3x)", "B) y = Ce^(x/3)", "C) y = 3Ce^x", "D) y = e^(3x) + C"],
     "answer": 0, "topic": "Differential Equations",
     "explanation": "Separable: dy/y = 3dx → ln|y| = 3x + C₁ → y = Ce^(3x)."},
    {"q": "The order of the differential equation y'' + 3y' - 2y = sin(x) is:",
     "choices": ["A) 1", "B) 2", "C) 3", "D) 0"],
     "answer": 1, "topic": "Differential Equations",
     "explanation": "The order is the highest derivative present. y'' is the second derivative, so order = 2."},
    {"q": "For the ODE dy/dx = -ky (exponential decay), if y(0) = 100 and y(1) = 50, what is k?",
     "choices": ["A) ln(2)", "B) 0.5", "C) 2", "D) -ln(2)"],
     "answer": 0, "topic": "Differential Equations",
     "explanation": "Solution: y = 100·e^(-kt). At t=1: 50 = 100·e^(-k) → e^(-k) = 0.5 → k = ln(2) ≈ 0.693."},
    {"q": "The characteristic equation of y'' - 5y' + 6y = 0 is:",
     "choices": ["A) r² - 5r + 6 = 0", "B) r² + 5r + 6 = 0", "C) r² - 5r - 6 = 0", "D) r + 6 = 0"],
     "answer": 0, "topic": "Differential Equations",
     "explanation": "For ay'' + by' + cy = 0, substitute y = e^(rx): ar² + br + c = 0. Here: r² - 5r + 6 = 0."},
    {"q": "Solve the separable ODE: (dy/dx) = x/y, with y(0) = 2.",
     "choices": ["A) y = √(x² + 4)", "B) y = x² + 2", "C) y = x + 2", "D) y = e^(x²/2)"],
     "answer": 0, "topic": "Differential Equations",
     "explanation": "Separate: y dy = x dx → y²/2 = x²/2 + C. At y(0)=2: 2 = C. So y² = x² + 4 → y = √(x²+4)."},
    {"q": "Euler's method approximates ODEs numerically. For dy/dx = f(x,y), the step formula is:",
     "choices": ["A) y_{n+1} = y_n + h·f(x_n, y_n)",
                 "B) y_{n+1} = y_n - h·f(x_n, y_n)",
                 "C) y_{n+1} = y_n + h²·f(x_n, y_n)",
                 "D) y_{n+1} = y_n·f(x_n, y_n)"],
     "answer": 0, "topic": "Differential Equations",
     "explanation": "Euler's method: y_{n+1} = y_n + h·f(x_n, y_n), where h is the step size. First-order accurate method."},
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

with gr.Blocks(css=CSS, title="FissionLab Math Practice — Dr. Preston PhD") as demo:
    session_state = gr.State(new_session())

    gr.Markdown("# FissionLab Math Practice App — Dr. Preston PhD")
    gr.Markdown(
        "<div class='authority'>Dr. Preston — PhD Nuclear Engineering · Physics Educator & AI/ML Instructor</div>"
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
