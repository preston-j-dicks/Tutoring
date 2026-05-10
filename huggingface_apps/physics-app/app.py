# HuggingFace Space: Dr-P/physics-app
# Live URL: https://dr-p-physics-app.hf.space

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
    # Classical Mechanics
    {"q": "A 2 kg block slides 5 m down a frictionless 30° incline. What is its speed at the bottom? (g = 9.8 m/s²)",
     "choices": ["A) 4.95 m/s", "B) 7.00 m/s", "C) 9.90 m/s", "D) 3.13 m/s"],
     "answer": 0, "topic": "Classical Mechanics",
     "explanation": "Height h = 5·sin(30°) = 2.5 m. Using energy: v = √(2gh) = √(2·9.8·2.5) = √49 ≈ 4.95 m/s."},
    {"q": "A 1500 kg car traveling at 20 m/s brakes to a stop over 50 m. What is the braking force?",
     "choices": ["A) 3000 N", "B) 6000 N", "C) 300 N", "D) 600 N"],
     "answer": 1, "topic": "Classical Mechanics",
     "explanation": "v² = v₀² + 2a·d → 0 = 400 + 2a·50 → a = -4 m/s². F = ma = 1500·4 = 6000 N."},
    {"q": "A projectile is launched at 45° with speed 20 m/s. What is its maximum range? (g = 10 m/s²)",
     "choices": ["A) 20 m", "B) 40 m", "C) 28.3 m", "D) 10 m"],
     "answer": 1, "topic": "Classical Mechanics",
     "explanation": "Range R = v₀²·sin(2θ)/g = 400·sin(90°)/10 = 40 m. Maximum range occurs at 45°."},
    {"q": "A 0.5 kg ball on a 1.2 m string moves in a horizontal circle at 3 m/s. What is the centripetal force?",
     "choices": ["A) 1.25 N", "B) 3.75 N", "C) 0.9 N", "D) 7.5 N"],
     "answer": 1, "topic": "Classical Mechanics",
     "explanation": "F_c = mv²/r = 0.5·9/1.2 = 3.75 N."},
    {"q": "A 60 kg person stands on a scale in an elevator accelerating upward at 2 m/s². What does the scale read? (g = 10 m/s²)",
     "choices": ["A) 480 N", "B) 600 N", "C) 720 N", "D) 540 N"],
     "answer": 2, "topic": "Classical Mechanics",
     "explanation": "N = m(g + a) = 60·(10 + 2) = 720 N. Apparent weight increases when accelerating upward."},
    {"q": "Two objects (3 kg and 5 kg) collide and stick together. If the 3 kg object was moving at 8 m/s and the 5 kg was at rest, what is the final velocity?",
     "choices": ["A) 4.8 m/s", "B) 3.0 m/s", "C) 5.0 m/s", "D) 2.4 m/s"],
     "answer": 1, "topic": "Classical Mechanics",
     "explanation": "Conservation of momentum: 3·8 + 0 = 8·v_f → v_f = 24/8 = 3.0 m/s."},
    # Electromagnetism
    {"q": "Two point charges of +3 μC and +5 μC are separated by 0.2 m. What is the electrostatic force between them? (k = 9×10⁹ N·m²/C²)",
     "choices": ["A) 3.375 N", "B) 0.3375 N", "C) 33.75 N", "D) 0.034 N"],
     "answer": 0, "topic": "Electromagnetism",
     "explanation": "F = k·q₁·q₂/r² = 9×10⁹·3×10⁻⁶·5×10⁻⁶/0.04 = 135×10⁻³/0.04 = 3.375 N."},
    {"q": "A wire carries 4 A in a magnetic field of 0.5 T. If the wire is 0.3 m long and perpendicular to B, what is the magnetic force on it?",
     "choices": ["A) 0.6 N", "B) 2.0 N", "C) 6.0 N", "D) 0.06 N"],
     "answer": 0, "topic": "Electromagnetism",
     "explanation": "F = BIL = 0.5·4·0.3 = 0.6 N."},
    {"q": "A capacitor of 10 μF is charged to 100 V. What energy is stored?",
     "choices": ["A) 0.05 J", "B) 0.5 J", "C) 5 J", "D) 0.005 J"],
     "answer": 0, "topic": "Electromagnetism",
     "explanation": "U = ½CV² = ½·10×10⁻⁶·10000 = 0.05 J."},
    {"q": "Faraday's law states that the induced EMF in a loop equals:",
     "choices": ["A) the rate of change of magnetic flux through the loop",
                 "B) the total magnetic field times the loop area",
                 "C) the current times the loop resistance",
                 "D) the magnetic force on the loop's charges"],
     "answer": 0, "topic": "Electromagnetism",
     "explanation": "Faraday's law: ε = -dΦ_B/dt. The induced EMF equals the negative rate of change of magnetic flux."},
    {"q": "A solenoid has 500 turns, length 0.25 m, and radius 0.02 m. What is its inductance? (μ₀ = 4π×10⁻⁷ H/m)",
     "choices": ["A) 12.6 μH", "B) 126 μH", "C) 1.26 mH", "D) 0.126 mH"],
     "answer": 1, "topic": "Electromagnetism",
     "explanation": "L = μ₀·n²·V = μ₀·(N/l)²·A·l = 4π×10⁻⁷·(500/0.25)²·π·(0.02)²·0.25 ≈ 126 μH."},
    {"q": "In an RC circuit with R = 1 kΩ and C = 100 μF, what is the time constant τ?",
     "choices": ["A) 0.01 s", "B) 0.1 s", "C) 1 s", "D) 10 s"],
     "answer": 1, "topic": "Electromagnetism",
     "explanation": "τ = RC = 1000·100×10⁻⁶ = 0.1 s."},
    # Thermodynamics
    {"q": "An ideal gas undergoes an isothermal expansion, doubling its volume. How does the pressure change?",
     "choices": ["A) Doubles", "B) Stays the same", "C) Halves", "D) Quadruples"],
     "answer": 2, "topic": "Thermodynamics",
     "explanation": "At constant temperature, PV = const (Boyle's Law). If V doubles, P halves."},
    {"q": "A Carnot engine operates between 800 K and 300 K. What is its maximum efficiency?",
     "choices": ["A) 37.5%", "B) 62.5%", "C) 37.5%", "D) 52.5%"],
     "answer": 1, "topic": "Thermodynamics",
     "explanation": "η = 1 - T_cold/T_hot = 1 - 300/800 = 0.625 = 62.5%."},
    {"q": "How much heat is required to raise 2 kg of water from 20°C to 100°C? (c_water = 4186 J/kg·K)",
     "choices": ["A) 334,880 J", "B) 167,440 J", "C) 669,760 J", "D) 83,720 J"],
     "answer": 2, "topic": "Thermodynamics",
     "explanation": "Q = mcΔT = 2·4186·80 = 669,760 J."},
    {"q": "The second law of thermodynamics states that in any spontaneous process:",
     "choices": ["A) energy is conserved",
                 "B) entropy of the universe decreases",
                 "C) entropy of the universe increases or stays the same",
                 "D) heat flows from cold to hot"],
     "answer": 2, "topic": "Thermodynamics",
     "explanation": "The Second Law states the total entropy of an isolated system can only increase or remain constant."},
    {"q": "An ideal monatomic gas (n = 1 mol) expands isochorically, absorbing 300 J of heat. What is the change in internal energy?",
     "choices": ["A) 0 J", "B) 300 J", "C) 150 J", "D) 600 J"],
     "answer": 1, "topic": "Thermodynamics",
     "explanation": "At constant volume (isochoric), W = 0. By first law: ΔU = Q - W = 300 - 0 = 300 J."},
    {"q": "Stefan-Boltzmann law gives the power radiated by a blackbody. If temperature doubles, power output changes by factor:",
     "choices": ["A) 2", "B) 4", "C) 8", "D) 16"],
     "answer": 3, "topic": "Thermodynamics",
     "explanation": "P = σT⁴. If T → 2T, then P → σ(2T)⁴ = 16σT⁴. Power increases by factor 16."},
    # Quantum Mechanics
    {"q": "What is the de Broglie wavelength of an electron (m = 9.11×10⁻³¹ kg) moving at 2×10⁶ m/s? (h = 6.626×10⁻³⁴ J·s)",
     "choices": ["A) 3.64×10⁻¹⁰ m", "B) 1.82×10⁻¹⁰ m", "C) 3.64×10⁻⁹ m", "D) 7.28×10⁻¹⁰ m"],
     "answer": 0, "topic": "Quantum Mechanics",
     "explanation": "λ = h/mv = 6.626×10⁻³⁴/(9.11×10⁻³¹·2×10⁶) = 6.626×10⁻³⁴/1.822×10⁻²⁴ ≈ 3.64×10⁻¹⁰ m."},
    {"q": "Heisenberg's uncertainty principle states that Δx·Δp ≥:",
     "choices": ["A) h", "B) h/2", "C) ℏ/2", "D) ℏ"],
     "answer": 2, "topic": "Quantum Mechanics",
     "explanation": "The Heisenberg Uncertainty Principle: Δx·Δp ≥ ℏ/2, where ℏ = h/(2π)."},
    {"q": "The photoelectric effect showed that the kinetic energy of emitted electrons depends on:",
     "choices": ["A) intensity of light only",
                 "B) frequency of light only",
                 "C) both intensity and frequency equally",
                 "D) wavelength squared"],
     "answer": 1, "topic": "Quantum Mechanics",
     "explanation": "KE = hf - φ. Kinetic energy depends on frequency (f), not intensity. Intensity affects the number of emitted electrons."},
    {"q": "A photon has energy 3.0 eV. What is its wavelength? (hc = 1240 eV·nm)",
     "choices": ["A) 413 nm", "B) 620 nm", "C) 248 nm", "D) 310 nm"],
     "answer": 0, "topic": "Quantum Mechanics",
     "explanation": "λ = hc/E = 1240/3.0 ≈ 413 nm (visible violet light)."},
    {"q": "For a hydrogen atom, what is the energy of a photon emitted when an electron falls from n=3 to n=2? (E_n = -13.6/n² eV)",
     "choices": ["A) 1.89 eV", "B) 3.4 eV", "C) 1.51 eV", "D) 0.66 eV"],
     "answer": 0, "topic": "Quantum Mechanics",
     "explanation": "ΔE = E_2 - E_3 = -13.6/4 - (-13.6/9) = -3.4 + 1.51 = 1.89 eV. This is the Hα line (656 nm)."},
    {"q": "The Schrödinger equation in quantum mechanics is analogous to which classical equation?",
     "choices": ["A) Newton's second law F = ma",
                 "B) Maxwell's wave equation",
                 "C) Boltzmann's entropy equation",
                 "D) Hamilton's equations of motion"],
     "answer": 0, "topic": "Quantum Mechanics",
     "explanation": "The Schrödinger equation is QM's equation of motion, playing the role of Newton's second law F = ma in classical mechanics."},
    # Nuclear & Modern Physics
    {"q": "U-238 undergoes alpha decay. What is the daughter nucleus?",
     "choices": ["A) Th-234", "B) Pa-238", "C) Th-238", "D) Ra-234"],
     "answer": 0, "topic": "Nuclear & Modern Physics",
     "explanation": "Alpha decay removes 2 protons and 2 neutrons: ²³⁸U → ²³⁴Th + ⁴He. Daughter is Th-234."},
    {"q": "A radioactive sample has a half-life of 6 hours. What fraction remains after 24 hours?",
     "choices": ["A) 1/2", "B) 1/4", "C) 1/8", "D) 1/16"],
     "answer": 3, "topic": "Nuclear & Modern Physics",
     "explanation": "24 hours = 4 half-lives. Fraction remaining = (1/2)⁴ = 1/16."},
    {"q": "In nuclear fission of U-235, approximately how much energy is released per fission event?",
     "choices": ["A) 2 MeV", "B) 20 MeV", "C) 200 MeV", "D) 2000 MeV"],
     "answer": 2, "topic": "Nuclear & Modern Physics",
     "explanation": "Each U-235 fission releases approximately 200 MeV of energy, mostly as kinetic energy of fission fragments."},
    {"q": "Special relativity predicts that a 1 kg object moving at 0.6c has kinetic energy (γ = 1.25, m₀c² = 9×10¹⁶ J):",
     "choices": ["A) 2.25×10¹⁶ J", "B) 1.62×10¹⁶ J", "C) 1.125×10¹⁶ J", "D) 3.24×10¹⁶ J"],
     "answer": 0, "topic": "Nuclear & Modern Physics",
     "explanation": "KE = (γ-1)m₀c² = (1.25-1)·9×10¹⁶ = 0.25·9×10¹⁶ = 2.25×10¹⁶ J."},
    {"q": "The binding energy per nucleon is highest for which element?",
     "choices": ["A) Hydrogen", "B) Uranium-235", "C) Iron-56", "D) Carbon-12"],
     "answer": 2, "topic": "Nuclear & Modern Physics",
     "explanation": "Iron-56 has the highest binding energy per nucleon (~8.8 MeV/nucleon), making it the most stable nucleus."},
    {"q": "Beta-minus decay involves the emission of:",
     "choices": ["A) a proton and neutrino",
                 "B) an electron and antineutrino",
                 "C) a positron and neutrino",
                 "D) an alpha particle"],
     "answer": 1, "topic": "Nuclear & Modern Physics",
     "explanation": "β⁻ decay: n → p + e⁻ + ν̄_e. A neutron converts to a proton, emitting an electron and an electron antineutrino."},
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

with gr.Blocks(css=CSS, title="FissionLab Physics Practice — Dr. Preston PhD") as demo:
    session_state = gr.State(new_session())

    gr.Markdown("# FissionLab Physics Practice App — Dr. Preston PhD")
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

    # Wire up first question on load
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
