"""
FissionLab Physics Practice App v3.0 — Dr. Preston PhD
SP211 Calculus-Based Mechanics + SP212 Electromagnetism — USNA Validation Prep
Purcell E&M aligned · 10 questions at a time · 20-question diagnostic · Solutions at end
"""
import io, base64, random, re
from datetime import date
import requests
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['mathtext.fontset'] = 'cm'
import gradio as gr

# ── Auth ─────────────────────────────────────────────────────────────────────
PORTAL  = "https://web-production-202b9.up.railway.app/api/verify"
PATTERN = re.compile(r"^FLAB-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", re.IGNORECASE)

def verify_token(token: str) -> bool:
    t = token.strip().upper()
    if not PATTERN.match(t): return False
    try:
        r = requests.get(PORTAL, params={"token": t}, timeout=5)
        return r.status_code == 200 and r.json().get("valid", False)
    except Exception:
        return False

# ── Styling ───────────────────────────────────────────────────────────────────
DARK = {"figure.facecolor":"#0b1a2e","axes.facecolor":"#112240","axes.edgecolor":"#8fa8c8",
        "axes.labelcolor":"#e8eaf0","xtick.color":"#8fa8c8","ytick.color":"#8fa8c8",
        "text.color":"#e8eaf0","grid.color":"#1e3a5f","grid.alpha":0.4}

CSS = """
.gradio-container{background:#0b1a2e!important;color:#e8eaf0!important;font-family:'Segoe UI',system-ui,sans-serif}
h1,h2,h3{color:#f4c542!important;font-family:Georgia,serif}
.gr-button-primary,.primary{background:#f4c542!important;color:#0b1a2e!important;font-weight:700!important;border:none!important}
.gr-button,.secondary{border:1px solid rgba(201,168,76,0.4)!important;color:#f4c542!important;background:rgba(201,168,76,0.08)!important}
.gr-box,.gr-form,.gr-panel,.block{background:#112240!important;border-color:#1e3a5f!important}
label,p,span{color:#e8eaf0!important}
.q-block{background:rgba(17,34,64,0.9);border:1px solid rgba(201,168,76,0.2);border-radius:10px;padding:16px 20px;margin:10px 0}
.q-label{color:#f4c542;font-weight:700;font-size:0.82rem;letter-spacing:0.05em;text-transform:uppercase;margin-bottom:6px}
.q-tag{color:rgba(232,234,240,0.4);font-size:0.72rem;margin-top:6px}
.correct-box{background:rgba(40,200,100,0.1);border-left:3px solid #28c864;padding:12px 16px;border-radius:0 8px 8px 0;margin:6px 0}
.wrong-box{background:rgba(255,80,80,0.08);border-left:3px solid #ff5050;padding:12px 16px;border-radius:0 8px 8px 0;margin:6px 0}
.solution-text{background:rgba(20,40,80,0.6);border:1px solid rgba(100,150,255,0.2);border-radius:8px;padding:12px 16px;margin-top:8px;font-size:0.88rem;color:rgba(232,234,240,0.85)}
.score-banner{text-align:center;padding:28px;background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.25);border-radius:12px;margin-bottom:20px}
.warn-banner{background:rgba(255,100,50,0.1);border:1px solid rgba(255,100,50,0.3);border-radius:8px;padding:12px 16px;margin-bottom:12px;color:rgba(255,160,100,0.9)}
footer{display:none!important}
"""

DIVIDER = "<hr style='border:none;border-top:1px solid rgba(201,168,76,0.2);margin:18px 0'>"

# ── Formula image renderer ────────────────────────────────────────────────────
def fimg(latex: str, fs: int = 14) -> str:
    try:
        fig, ax = plt.subplots(figsize=(7.5, 0.7))
        fig.patch.set_facecolor('#0d1f3c')
        ax.set_facecolor('#0d1f3c')
        ax.axis('off')
        ax.text(0.5, 0.5, r'$' + latex + r'$', transform=ax.transAxes,
                ha='center', va='center', fontsize=fs, color='#f0ebe0')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=130, bbox_inches='tight',
                    facecolor='#0d1f3c', edgecolor='none')
        buf.seek(0); plt.close(fig)
        data = base64.b64encode(buf.read()).decode()
        return f'<img src="data:image/png;base64,{data}" style="display:block;margin:10px auto;max-width:92%;border-radius:6px">'
    except Exception:
        return f'<code style="color:#c9a84c">{latex}</code>'

_FM = {
    # Mechanics
    'kinematics': r'v = v_0 + at;\quad x = x_0 + v_0 t + \tfrac{1}{2}at^2;\quad v^2 = v_0^2 + 2a\Delta x',
    'range':      r'R = \dfrac{v_0^2\sin(2\theta)}{g}',
    'newton2':    r'\sum \mathbf{F} = m\mathbf{a}',
    'work_energy':r'W_{net} = \Delta K = K_f - K_i',
    'energy_cons':r'K_i + U_i = K_f + U_f \quad\text{(no friction)}',
    'momentum':   r'\mathbf{J} = \Delta\mathbf{p} = \int \mathbf{F}\,dt',
    'torque':     r'\sum \tau = I\alpha',
    'ang_mom':    r'\mathbf{L} = I\boldsymbol{\omega};\quad \tau_{net} = \dfrac{d\mathbf{L}}{dt}',
    'shm':        r'x(t) = A\cos(\omega t + \phi);\quad \omega = \sqrt{k/m}',
    'pendulum':   r'T = 2\pi\sqrt{L/g}',
    'gravity':    r'F = \dfrac{Gm_1 m_2}{r^2};\quad U = -\dfrac{Gm_1 m_2}{r}',
    'orbital':    r'v_{orb} = \sqrt{\dfrac{GM}{r}};\quad v_{esc} = \sqrt{\dfrac{2GM}{R}}',
    # E&M (Purcell)
    'coulomb':    r'F = \dfrac{kq_1 q_2}{r^2},\quad k = \dfrac{1}{4\pi\varepsilon_0}',
    'efield':     r'\mathbf{E} = \dfrac{k|q|}{r^2}\hat{r};\quad \mathbf{F} = q\mathbf{E}',
    'gauss':      r'\oint \mathbf{E}\cdot d\mathbf{A} = \dfrac{Q_{enc}}{\varepsilon_0}',
    'potential':  r'V = \dfrac{kq}{r};\quad \mathbf{E} = -\nabla V',
    'capacitor':  r'C = \dfrac{Q}{V} = \dfrac{\varepsilon_0 A}{d};\quad U = \tfrac{1}{2}CV^2',
    'ohm':        r'V = IR;\quad P = IV = I^2R = \dfrac{V^2}{R}',
    'rc':         r'\tau = RC;\quad q(t) = Q\!\left(1-e^{-t/\tau}\right)',
    'ampere':     r'\oint \mathbf{B}\cdot d\mathbf{l} = \mu_0 I_{enc}',
    'solenoid':   r'B = \mu_0 n I\quad\text{(inside solenoid)}',
    'faraday':    r'\mathcal{E} = -\dfrac{d\Phi_B}{dt};\quad \Phi_B = \iint \mathbf{B}\cdot d\mathbf{A}',
}
FIMGS = {k: fimg(v) for k, v in _FM.items()}

# ── Topic map ────────────────────────────────────────────────────────────────
TOPICS = {
    "SP211 — Kinematics":            {"exam":"SP211","area":"mechanics"},
    "SP211 — Newton's Laws":         {"exam":"SP211","area":"mechanics"},
    "SP211 — Work & Energy":         {"exam":"SP211","area":"mechanics"},
    "SP211 — Momentum & Collisions": {"exam":"SP211","area":"mechanics"},
    "SP211 — Rotational Dynamics":   {"exam":"SP211","area":"mechanics"},
    "SP211 — Simple Harmonic Motion":{"exam":"SP211","area":"mechanics"},
    "SP211 — Gravitation":           {"exam":"SP211","area":"mechanics"},
    "SP212 — Electric Force & Field":{"exam":"SP212","area":"em"},
    "SP212 — Electric Potential":    {"exam":"SP212","area":"em"},
    "SP212 — Capacitance & Circuits":{"exam":"SP212","area":"em"},
    "SP212 — Magnetism":             {"exam":"SP212","area":"em"},
    "SP212 — Faraday & Induction":   {"exam":"SP212","area":"em"},
}

def _tsec(title, body, formula_keys=None):
    parts = [f'<div style="max-width:860px;line-height:1.75">',
             f'<h3 style="font-family:Georgia,serif;color:#f4c542;border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:14px">{title}</h3>',
             f'<div style="color:rgba(232,234,240,0.88);font-size:0.92rem">{body}</div>']
    if formula_keys:
        parts.append('<div style="margin:14px 0">')
        for k in formula_keys:
            parts.append(FIMGS.get(k, ''))
        parts.append('</div>')
    parts.append('</div>')
    return '\n'.join(parts)

TOPIC_HTML = {
    "SP211 — Kinematics": _tsec(
        "SP211 — Kinematics",
        "<b>1D constant acceleration:</b> v=v₀+at, x=x₀+v₀t+½at², v²=v₀²+2aΔx<br>"
        "<b>Calculus:</b> v=dx/dt, a=dv/dt. For variable a: integrate.<br>"
        "<b>2D Projectile</b> (a_x=0, a_y=−g): x=v₀cosθ·t, y=v₀sinθ·t−½gt²<br>"
        "<b>Range:</b> R=v₀²sin(2θ)/g — max at θ=45°. <b>Circular:</b> a_c=v²/r toward center.",
        ['kinematics', 'range']),
    "SP211 — Newton's Laws": _tsec(
        "SP211 — Newton's Laws",
        "<b>1st:</b> ΣF=0 ↔ constant velocity. <b>2nd:</b> ΣF=ma (by component). <b>3rd:</b> F₁₂=−F₂₁ (on different objects).<br>"
        "<b>Common forces:</b> W=mg↓; N⊥surface (N=mg cosθ on incline); f_k=μ_k N; spring F=−kx<br>"
        '<div class="warn-banner">Draw a free-body diagram for EACH object separately. Never add action-reaction pairs within one FBD.</div>',
        ['newton2']),
    "SP211 — Work & Energy": _tsec(
        "SP211 — Work &amp; Energy",
        "<b>Work:</b> W=F·d·cosθ (dot product). Variable force: W=∫F(x)dx.<br>"
        "<b>KE:</b> K=½mv². <b>Work-Energy Theorem:</b> W_net=ΔK.<br>"
        "<b>PE:</b> U_g=mgh, U_spring=½kx². <b>Conservation:</b> K_i+U_i=K_f+U_f (no friction).<br>"
        "<b>With non-conservative forces:</b> W_nc=ΔE=ΔK+ΔU. <b>Power:</b> P=dW/dt=F·v",
        ['work_energy', 'energy_cons']),
    "SP211 — Momentum & Collisions": _tsec(
        "SP211 — Momentum &amp; Collisions",
        "<b>Momentum:</b> p=mv (vector). <b>Impulse-Momentum:</b> J=Δp=F_avg·Δt<br>"
        "<b>Conservation:</b> ΣF_ext=0 → Σp=constant.<br>"
        "<b>Elastic:</b> momentum AND KE conserved. Equal masses: velocities exchange.<br>"
        "<b>Perfectly inelastic:</b> objects stick. (m₁+m₂)v_f=m₁v₁+m₂v₂<br>"
        "<b>Center of mass:</b> r_cm=Σmᵢrᵢ/M",
        ['momentum']),
    "SP211 — Rotational Dynamics": _tsec(
        "SP211 — Rotational Dynamics",
        "<b>τ=Iα</b> (analogous to F=ma). <b>Moments of inertia:</b><br>"
        "Solid disk: ½MR² · Hollow cylinder: MR² · Solid sphere: ⅖MR² · Rod(center): ML²/12<br>"
        "<b>Parallel axis:</b> I=I_cm+Md². <b>Rolling:</b> v_cm=ωR; KE=½mv_cm²+½Iω²<br>"
        "<b>Conservation of L:</b> τ_net=0 → L=Iω=const.",
        ['torque', 'ang_mom']),
    "SP211 — Simple Harmonic Motion": _tsec(
        "SP211 — Simple Harmonic Motion",
        "<b>Condition:</b> linear restoring force F=−kx.<br>"
        "<b>Mass-spring:</b> ω=√(k/m), T=2π√(m/k). <b>Pendulum:</b> ω=√(g/L), T=2π√(L/g).<br>"
        "<b>v_max=Aω</b> (at x=0). <b>v at x:</b> v=ω√(A²−x²). <b>Energy:</b> E=½kA²=constant.<br>"
        "Period does NOT depend on amplitude (ideal SHM). Pendulum period does NOT depend on mass.",
        ['shm', 'pendulum']),
    "SP211 — Gravitation": _tsec(
        "SP211 — Gravitation",
        "<b>Newton:</b> F=Gm₁m₂/r². <b>PE:</b> U=−Gm₁m₂/r (zero at r=∞).<br>"
        "<b>Circular orbit:</b> Gravity=centripetal → v=√(GM/r).<br>"
        "<b>Escape velocity:</b> v_esc=√(2GM/R) (set KE=|U|).<br>"
        "<b>Kepler's 3rd:</b> T²=4π²a³/(GM). G=6.674×10⁻¹¹ N·m²/kg².",
        ['gravity', 'orbital']),
    "SP212 — Electric Force & Field": _tsec(
        "SP212 — Electric Force &amp; Field · Purcell Ch. 1",
        "<b>Coulomb:</b> F=kq₁q₂/r², k=9×10⁹ N·m²/C², ε₀=8.85×10⁻¹² C²/(N·m²).<br>"
        "<b>E field:</b> E=kq/r² (point charge); superposition for multiple charges (vector sum).<br>"
        "<b>Gauss's law — use for symmetric distributions:</b><br>"
        "Outside sphere: E=kQ/r² · Inside uniform sphere: E=kQr/R³ · Infinite line: E=λ/(2πε₀r)",
        ['coulomb', 'efield', 'gauss']),
    "SP212 — Electric Potential": _tsec(
        "SP212 — Electric Potential · Purcell Ch. 2",
        "<b>Potential V</b> (scalar): V=kq/r (point charge). Multiple charges: V=Σkqᵢ/rᵢ (scalar!).<br>"
        "<b>Field-potential:</b> E=−dV/dx (1D); E=−∇V (3D). Field points high→low V.<br>"
        "<b>Work:</b> W=q(V_A−V_B)=−ΔU. <b>Equipotentials:</b> ⊥ to field lines.<br>"
        "<b>Conductors:</b> E=0 inside; surface is equipotential.",
        ['potential']),
    "SP212 — Capacitance & Circuits": _tsec(
        "SP212 — Capacitance &amp; Circuits · Purcell Ch. 3–4",
        "<b>Capacitor:</b> C=Q/V. Parallel plate: C=ε₀A/d. With dielectric κ: C=κε₀A/d.<br>"
        "<b>Series:</b> 1/C_eq=Σ1/Cᵢ (same Q). <b>Parallel:</b> C_eq=ΣCᵢ (same V).<br>"
        "<b>KVL:</b> ΣV around loop=0. <b>KCL:</b> ΣI into node=0.<br>"
        "<b>RC circuits:</b> τ=RC. At t=τ: ~63% charged/discharged.",
        ['capacitor', 'ohm', 'rc']),
    "SP212 — Magnetism": _tsec(
        "SP212 — Magnetism · Purcell Ch. 5–6",
        "<b>Force on charge:</b> F=qv×B. <b>Force on wire:</b> F=IL×B. Magnitude: F=qvBsinθ.<br>"
        "<b>Magnetic force does NO work</b> (always ⊥ v).<br>"
        "<b>Circular orbit radius:</b> r=mv/(qB).<br>"
        "<b>Infinite wire:</b> B=μ₀I/(2πr). <b>Solenoid:</b> B=μ₀nI (inside only). μ₀=4π×10⁻⁷ T·m/A.",
        ['ampere', 'solenoid']),
    "SP212 — Faraday & Induction": _tsec(
        "SP212 — Faraday &amp; Induction · Purcell Ch. 7",
        "<b>Faraday:</b> ε=−dΦ_B/dt. Induced EMF = negative rate of flux change.<br>"
        "<b>Lenz's law:</b> Induced current opposes the change in flux (determines direction).<br>"
        "<b>Motional EMF:</b> ε=BLv. <b>Inductance:</b> L=NΦ_B/I. Solenoid: L=μ₀n²V.<br>"
        "<b>Maxwell's equations:</b> ∮E·dA=Q/ε₀ · ∮B·dA=0 · ε=−dΦ_B/dt · ∮B·dl=μ₀(I+ε₀dΦ_E/dt)",
        ['faraday']),
}

# ── 20 Diagnostic Questions ───────────────────────────────────────────────────
# Q1-10: Mechanics (SP211) · Q11-20: E&M (SP212)
DIAGNOSTIC = [
    # SP211 Mechanics
    {"q": "A ball is launched at θ=30° with v₀=20 m/s. Horizontal range? (g=10 m/s²)",
     "choices": ["A) 20 m", "B) 20√3 m ≈ 34.6 m", "C) 40 m", "D) 30 m"],
     "answer": "B)", "topic": "SP211 — Kinematics", "ch": "SP211 Kinematics",
     "solution": "R=v₀²sin(2θ)/g=(400·sin60°)/10=40·(√3/2)=20√3≈34.6 m. At 45° range is maximum."},
    {"q": "A 5 kg block sits on a frictionless 30° incline. Acceleration down the slope? (g=9.8)",
     "choices": ["A) 9.8 m/s²", "B) 4.9 m/s²", "C) 8.5 m/s²", "D) 0 m/s²"],
     "answer": "B)", "topic": "SP211 — Newton's Laws", "ch": "SP211 Newton's Laws",
     "solution": "Net force along incline=mg sin30°=5(9.8)(0.5)=24.5 N. a=F/m=4.9 m/s²=g sin30°."},
    {"q": "A spring (k=200 N/m) compressed 0.1 m releases a 0.5 kg block. Speed when released?",
     "choices": ["A) 1 m/s", "B) 2 m/s", "C) √2 m/s", "D) 4 m/s"],
     "answer": "B)", "topic": "SP211 — Work & Energy", "ch": "SP211 Work & Energy",
     "solution": "½kx²=½mv². v=x√(k/m)=0.1·√(200/0.5)=0.1·20=2 m/s."},
    {"q": "A 3 kg block at 4 m/s collides and sticks with a stationary 5 kg block. Final velocity?",
     "choices": ["A) 1.5 m/s", "B) 2 m/s", "C) 2.4 m/s", "D) 4 m/s"],
     "answer": "A)", "topic": "SP211 — Momentum & Collisions", "ch": "SP211 Momentum",
     "solution": "Perfectly inelastic: 3(4)=(3+5)v_f → v_f=12/8=1.5 m/s. KE is NOT conserved."},
    {"q": "A solid disk (I=½MR²) rolls down an incline descending h=2 m. Speed at bottom? (g=9.8)",
     "choices": ["A) √(4gh/3) ≈ 5.1 m/s", "B) √(2gh) ≈ 6.3 m/s", "C) √(gh) ≈ 4.4 m/s", "D) √(4gh/5) ≈ 4.0 m/s"],
     "answer": "A)", "topic": "SP211 — Rotational Dynamics", "ch": "SP211 Rotation",
     "solution": "Energy: Mgh=¾Mv². v=√(4gh/3)=√(4·9.8·2/3)≈5.1 m/s. Rolling uses BOTH translational + rotational KE."},
    {"q": "A mass-spring system: m=0.4 kg, k=100 N/m, A=0.05 m. Maximum speed?",
     "choices": ["A) 0.79 m/s", "B) 1.25 m/s", "C) 0.5 m/s", "D) 2.5 m/s"],
     "answer": "A)", "topic": "SP211 — Simple Harmonic Motion", "ch": "SP211 SHM",
     "solution": "ω=√(100/0.4)=√250=5√10≈15.81 rad/s. v_max=Aω=0.05×15.81≈0.79 m/s."},
    {"q": "Orbital speed of a satellite at altitude h above Earth? (M_E=Earth mass, R_E=Earth radius)",
     "choices": ["A) √(GM_E/h)", "B) √(GM_E/(R_E+h))", "C) √(2GM_E/R_E)", "D) √(GM_E·R_E)"],
     "answer": "B)", "topic": "SP211 — Gravitation", "ch": "SP211 Gravitation",
     "solution": "Gravity=centripetal: GM_E m/(R_E+h)²=mv²/(R_E+h). v=√(GM_E/(R_E+h)). Option C is escape velocity."},
    {"q": "Torque τ=40 N·m on a flywheel with I=8 kg·m². Starting from rest, ω after 5 s?",
     "choices": ["A) 25 rad/s", "B) 40 rad/s", "C) 5 rad/s", "D) 200 rad/s"],
     "answer": "A)", "topic": "SP211 — Rotational Dynamics", "ch": "SP211 Rotation",
     "solution": "α=τ/I=40/8=5 rad/s². ω=αt=5×5=25 rad/s. Analogy: τ=Iα ↔ F=ma."},
    {"q": "A particle moves at constant speed v in a circle of radius r. Its acceleration is:",
     "choices": ["A) v²/r toward center", "B) v/r²", "C) Zero — constant speed", "D) 2πv/T"],
     "answer": "A)", "topic": "SP211 — Kinematics", "ch": "SP211 Kinematics",
     "solution": "Centripetal acceleration=v²/r, directed toward center. Speed constant but direction changes → a≠0."},
    {"q": "Atwood machine: m₁=3 kg, m₂=5 kg, frictionless pulley. Acceleration?",
     "choices": ["A) g/4 ≈ 2.45 m/s²", "B) g/2 ≈ 4.9 m/s²", "C) g/8 ≈ 1.23 m/s²", "D) 2g/5 ≈ 3.92 m/s²"],
     "answer": "A)", "topic": "SP211 — Newton's Laws", "ch": "SP211 Newton's Laws",
     "solution": "Net force=(m₂−m₁)g=2(9.8)=19.6 N. Total mass=8 kg. a=19.6/8=g/4≈2.45 m/s²."},
    # SP212 E&M (Purcell-aligned)
    {"q": "Two point charges +q and −q separated by d. Electric potential at the midpoint?",
     "choices": ["A) 2kq/d", "B) kq/(d/2)", "C) 0", "D) −kq/d"],
     "answer": "C)", "topic": "SP212 — Electric Potential", "ch": "Purcell Ch. 2",
     "solution": "V=kq/(d/2)+k(−q)/(d/2)=0. Potential is SCALAR — do not use vector rules."},
    {"q": "Parallel-plate capacitor with charge Q. Plate separation doubled. How does V change?",
     "choices": ["A) Doubles", "B) Halves", "C) Same", "D) Quadruples"],
     "answer": "A)", "topic": "SP212 — Capacitance & Circuits", "ch": "Purcell Ch. 3",
     "solution": "C=ε₀A/d. Double d → C halves → V=Q/C doubles (Q fixed)."},
    {"q": "By Gauss's Law, E at distance r>R outside a uniformly charged sphere of charge Q?",
     "choices": ["A) kQ/r²", "B) kQr/R³", "C) kQ/R²", "D) 0"],
     "answer": "A)", "topic": "SP212 — Electric Force & Field", "ch": "Purcell Ch. 1",
     "solution": "Gauss: E·4πr²=Q/ε₀ → E=kQ/r². Same as point charge. Option B is inside the sphere."},
    {"q": "Three 6-Ω resistors connected in parallel. Equivalent resistance?",
     "choices": ["A) 18 Ω", "B) 6 Ω", "C) 2 Ω", "D) 3 Ω"],
     "answer": "C)", "topic": "SP212 — Capacitance & Circuits", "ch": "Purcell Ch. 4",
     "solution": "1/R_eq=1/6+1/6+1/6=3/6=1/2 → R_eq=2 Ω. (Series mistake: would give 18 Ω.)"},
    {"q": "Proton (q=1.6×10⁻¹⁹ C) at 10⁶ m/s in +x, B=0.1 T in +z. Magnetic force magnitude?",
     "choices": ["A) 1.6×10⁻¹⁴ N", "B) 1.6×10⁻²⁰ N", "C) 10⁻²⁵ N", "D) 1.6×10⁻⁸ N"],
     "answer": "A)", "topic": "SP212 — Magnetism", "ch": "Purcell Ch. 5",
     "solution": "F=qvB sin90°=(1.6×10⁻¹⁹)(10⁶)(0.1)=1.6×10⁻¹⁴ N. Direction: v×B=+x×+z=−y."},
    {"q": "RC circuit: R=10 kΩ, C=100 μF. Time constant τ?",
     "choices": ["A) 1 s", "B) 0.1 s", "C) 10 s", "D) 1000 s"],
     "answer": "A)", "topic": "SP212 — Capacitance & Circuits", "ch": "Purcell Ch. 4",
     "solution": "τ=RC=(10×10³)(100×10⁻⁶)=1 s. At t=τ: ~63% charged."},
    {"q": "Solenoid: n=1000 turns/m, I=2 A. B inside? (μ₀=4π×10⁻⁷ T·m/A)",
     "choices": ["A) 2.51×10⁻³ T", "B) 2π×10⁻³ T", "C) 4π×10⁻⁷ T", "D) 4π×10⁻³ T"],
     "answer": "A)", "topic": "SP212 — Magnetism", "ch": "Purcell Ch. 6",
     "solution": "B=μ₀nI=(4π×10⁻⁷)(1000)(2)=8π×10⁻⁴≈2.51×10⁻³ T. Zero outside ideal solenoid."},
    {"q": "Square loop (0.2 m side) in B=0.5 T ⊥ to loop. B decreases at 2 T/s. |EMF|?",
     "choices": ["A) 0.08 V", "B) 0.02 V", "C) 0.2 V", "D) 0.5 V"],
     "answer": "A)", "topic": "SP212 — Faraday & Induction", "ch": "Purcell Ch. 7",
     "solution": "|EMF|=|dΦ/dt|=A|dB/dt|=0.04×2=0.08 V. Lenz's law gives direction."},
    {"q": "Charge q=2 μC at a point where V=150 V. Electric potential energy U?",
     "choices": ["A) 3×10⁻⁴ J", "B) 7.5×10⁻⁵ J", "C) 6×10⁻⁴ J", "D) 1.5×10⁻⁴ J"],
     "answer": "A)", "topic": "SP212 — Electric Potential", "ch": "Purcell Ch. 2",
     "solution": "U=qV=(2×10⁻⁶)(150)=3×10⁻⁴ J=0.3 mJ."},
    {"q": "Gauss's Law for magnetism states the total magnetic flux through any closed surface is:",
     "choices": ["A) Q_enc/ε₀", "B) μ₀I_enc", "C) Zero", "D) −dΦ_E/dt"],
     "answer": "C)", "topic": "SP212 — Faraday & Induction", "ch": "Purcell Ch. 7",
     "solution": "∮B·dA=0. No magnetic monopoles — B field lines always close on themselves."},
]
assert len(DIAGNOSTIC) == 20

# ── Visualization helpers ─────────────────────────────────────────────────────
def _fig(w=7, h=4):
    for k, v in DARK.items(): plt.rcParams[k] = v
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("#0b1a2e"); ax.set_facecolor("#112240"); ax.grid(True)
    return fig, ax

def _save(fig):
    from PIL import Image as PILImage
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig); buf.seek(0)
    return PILImage.open(buf)

def plot_projectile():
    fig, ax = _fig()
    g = 9.8
    for angle, color in [(30,"#f4c542"),(45,"#4fc3f7"),(60,"#81c784")]:
        θ = np.radians(angle); T = 2*20*np.sin(θ)/g
        t = np.linspace(0, T, 300)
        ax.plot(20*np.cos(θ)*t, 20*np.sin(θ)*t-0.5*g*t**2, color=color, lw=2, label=f"{angle}°")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.legend(fontsize=9)
    ax.set_title("Projectile Motion (v₀=20 m/s) — Max range at 45°", color="#f4c542", fontsize=10)
    return _save(fig)

def plot_shm():
    fig, ax = _fig()
    t = np.linspace(0, 6*np.pi, 500); omega = 1.0
    ax.plot(t, np.cos(omega*t), color="#f4c542", lw=2, label="x(t)=A cos(ωt)")
    ax.plot(t, -np.sin(omega*t), color="#4fc3f7", lw=2, ls="--", label="v(t)/(Aω)")
    ax.set_xlabel("t"); ax.legend(fontsize=9)
    ax.set_title("SHM — Position and Velocity", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_energy_spring():
    fig, ax = _fig()
    x = np.linspace(-1, 1, 300); k = 100; m = 0.5; A = 1.0
    ke = 0.5*m*k/m*(A**2 - x**2); pe = 0.5*k*x**2
    ax.plot(x, pe, color="#f4c542", lw=2, label="U = ½kx²")
    ax.plot(x, ke, color="#4fc3f7", lw=2, label="K = ½mω²(A²−x²)")
    ax.plot(x, pe+ke, color="#81c784", lw=2, ls="--", label="Total E = ½kA²")
    ax.set_xlabel("x (m)"); ax.set_ylabel("Energy (J)"); ax.legend(fontsize=9)
    ax.set_title("SHM Energy Conservation", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_gauss():
    fig, ax = _fig(6, 5)
    ax.set_aspect("equal"); ax.grid(False)
    for r, c, lbl in [(2.5,"#4fc3f7","Gauss surface r>R"),(1.0,"#f4c542","Sphere R")]:
        circle = plt.Circle((0,0), r, fill=False, color=c, lw=2, label=lbl)
        ax.add_patch(circle)
    ax.plot(0, 0, 'o', color="#f06292", ms=8, label="+Q at center")
    for angle in range(0,360,45):
        θ = np.radians(angle); s = 2.5
        ax.annotate("", xy=(s*np.cos(θ),s*np.sin(θ)),
                    xytext=(1.2*np.cos(θ),1.2*np.sin(θ)),
                    arrowprops=dict(arrowstyle="->",color="#4fc3f7",lw=1.5))
    ax.set_xlim(-3.5,3.5); ax.set_ylim(-3.5,3.5)
    ax.set_title("Gauss's Law — E field outside sphere = kQ/r²", color="#f4c542", fontsize=10)
    ax.legend(fontsize=8)
    return _save(fig)

def plot_rc():
    fig, ax = _fig()
    t = np.linspace(0, 6, 400)
    for tau, c in [(0.5,"#f4c542"),(1.0,"#4fc3f7"),(2.0,"#81c784")]:
        ax.plot(t, 1-np.exp(-t/tau), color=c, lw=2, label=f"τ={tau}s")
    ax.axhline(1-np.exp(-1), color="white", ls=":", lw=1, alpha=0.5, label="63% at t=τ")
    ax.set_xlabel("t (s)"); ax.set_ylabel("q/Q_max"); ax.legend(fontsize=9)
    ax.set_title("RC Charging: q(t) = Q(1 − e^{−t/τ})", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_results(area_scores: dict):
    fig, ax = _fig(6, 3)
    for k, v in DARK.items(): plt.rcParams[k] = v
    cats = list(area_scores.keys()); vals = list(area_scores.values())
    bars = ax.barh(cats, vals, color=["#f4c542" if v>=0.6 else "#f06292" for v in vals], height=0.5)
    ax.set_xlim(0,1); ax.set_xlabel("Score")
    ax.set_title("Diagnostic Results", color="#f4c542", fontsize=11)
    for bar, val in zip(bars, vals):
        ax.text(val+0.02, bar.get_y()+bar.get_height()/2,
                f"{val*100:.0f}%", va="center", color="#e8eaf0", fontsize=9)
    return _save(fig)

PLOT_MAP = {
    "SP211 — Kinematics": plot_projectile,
    "SP211 — Simple Harmonic Motion": plot_shm,
    "SP211 — Work & Energy": plot_energy_spring,
    "SP212 — Electric Force & Field": plot_gauss,
    "SP212 — Capacitance & Circuits": plot_rc,
    "SP212 — Faraday & Induction": plot_rc,
}

# ── Pathway generator ─────────────────────────────────────────────────────────
DAYS_LEFT = max(0, (date(2026, 6, 21) - date.today()).days)

def generate_pathway(scores: dict) -> str:
    mech = [v for t,v in scores.items() if "SP211" in t]
    em   = [v for t,v in scores.items() if "SP212" in t]
    m_avg = sum(mech)/len(mech) if mech else 0
    e_avg = sum(em)/len(em) if em else 0
    md = f"## 📍 Your USNA Physics Pathway\n\n**{DAYS_LEFT} days until June 21 — I-Day June 25.**\n\n"
    md += "> ⚡ **SP211 must be validated before SP212.** Pass mechanics first.\n\n"
    for label, avg in [("SP211 Mechanics", m_avg), ("SP212 E&M", e_avg)]:
        bar = "█"*int(avg*10)+"░"*(10-int(avg*10))
        st = "✅ Strong" if avg>=0.7 else ("⚠️ Review" if avg>=0.4 else "🔴 Focus Here")
        md += f"- **{label}:** {bar} {avg*100:.0f}%  {st}\n"
    md += "\n### Recommended Plan\n"
    md += ("- 🔴 **SP211 needs serious work.** Spend 10 days on mechanics before touching E&M.\n"
           if m_avg < 0.5 else
           "- ✅ SP211 looks solid. Run a timed mock test to confirm, then move to SP212.\n")
    md += ("- ⚠️ **SP212:** After SP211 validated — drill Gauss, circuits, Faraday systematically.\n"
           if e_avg < 0.6 else
           "- ✅ SP212 foundation looks good.\n")
    weak = [t for t, s in scores.items() if s < 0.5]
    if weak:
        md += "\n### ⚡ Immediate Focus\n" + "".join(f"- {t}\n" for t in weak)
    return md

# ── Results builder ───────────────────────────────────────────────────────────
def build_results(answers: dict) -> tuple:
    correct_count = 0; html_parts = []
    topic_hits = {}; topic_total = {}
    for i, q in enumerate(DIAGNOSTIC):
        chosen = answers.get(i, "")
        is_right = bool(chosen and chosen.startswith(q["answer"]))
        if is_right: correct_count += 1
        t = q["topic"]
        topic_total[t] = topic_total.get(t,0)+1
        topic_hits[t] = topic_hits.get(t,0)+(1 if is_right else 0)
        icon = "✅" if is_right else "❌"
        box_cls = "correct-box" if is_right else "wrong-box"
        sol = (f'<div class="solution-text"><b>Solution:</b> {q["solution"]}</div>')
        html_parts.append(
            f'<div class="q-block">'
            f'<div class="q-label">Q{i+1} · {q["ch"]}</div>'
            f'<div style="color:#f0ebe0;font-size:0.95rem;margin-bottom:8px">{q["q"]}</div>'
            f'<div class="{box_cls}">{icon} Your answer: <b>{chosen or "(none)"}</b> · Correct: <b>{q["answer"]}</b></div>'
            f'{sol}</div>')
    scores = {t: topic_hits.get(t,0)/topic_total[t] for t in topic_total}
    pct = correct_count/20*100
    mech_score = sum(v for t,v in scores.items() if "SP211" in t)/max(1,sum(1 for t in scores if "SP211" in t))
    em_score   = sum(v for t,v in scores.items() if "SP212" in t)/max(1,sum(1 for t in scores if "SP212" in t))
    color = "#28c864" if pct>=70 else ("#f4c542" if pct>=50 else "#ff5050")
    banner = (f'<div class="score-banner">'
              f'<div style="font-family:Georgia,serif;font-size:3rem;font-weight:700;color:{color}">{correct_count}/20</div>'
              f'<div style="color:rgba(232,234,240,0.6);margin-top:6px">{pct:.0f}% correct</div>'
              f'<div style="display:flex;gap:20px;justify-content:center;margin-top:12px">'
              f'<div style="background:rgba(255,255,255,0.05);padding:8px 16px;border-radius:8px">'
              f'<div style="font-size:0.72rem;color:rgba(232,234,240,0.4)">SP211 Mechanics</div>'
              f'<div style="color:#f4c542;font-weight:700">{mech_score*100:.0f}%</div></div>'
              f'<div style="background:rgba(255,255,255,0.05);padding:8px 16px;border-radius:8px">'
              f'<div style="font-size:0.72rem;color:rgba(232,234,240,0.4)">SP212 E&M</div>'
              f'<div style="color:#f4c542;font-weight:700">{em_score*100:.0f}%</div></div></div>'
              f'<div style="color:rgba(232,234,240,0.35);font-size:0.78rem;margin-top:8px">SP211 required before SP212</div>'
              f'</div>')
    return banner + DIVIDER + "\n".join(html_parts), scores, {"SP211 Mechanics": mech_score, "SP212 E&M": em_score}

# ── Gradio app ────────────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="FissionLab Physics — Dr. Preston PhD") as demo:

    gr.HTML("""<div style="background:rgba(201,168,76,0.08);border-bottom:1px solid rgba(201,168,76,0.2);
    padding:16px 24px;border-radius:12px;margin-bottom:16px;display:flex;align-items:center;gap:14px">
    <span style="font-size:2.2rem">⚛️</span>
    <div>
      <div style="font-family:Georgia,serif;font-size:1.4rem;font-weight:700;color:#f4c542">
        FissionLab Physics — USNA SP211/SP212 Prep</div>
      <div style="font-size:0.82rem;color:rgba(232,234,240,0.5)">
        Dr. P · Mechanics + E&M · Purcell aligned · 20-question diagnostic</div>
    </div></div>""")

    with gr.Tabs():

        # ── DIAGNOSTIC ───────────────────────────────────────────────────────
        with gr.Tab("🎯 Diagnostic"):
            diag_state = gr.State({"page": 0, "answers": {}})

            with gr.Column(visible=True) as intro_col:
                gr.HTML("""<div style="text-align:center;padding:32px 20px">
                <h2 style="font-family:Georgia,serif;color:#f4c542;margin-bottom:12px">20-Question Diagnostic</h2>
                <div class="warn-banner" style="max-width:500px;margin:0 auto 16px;text-align:left">
                ⚡ <b>USNA requirement:</b> SP211 (mechanics) must be validated before you can sit SP212 (E&M).
                Prioritize questions 1–10 first.</div>
                <p style="color:rgba(232,234,240,0.7);max-width:500px;margin:0 auto 24px">
                Q1–10: SP211 Mechanics · Q11–20: SP212 E&M (Purcell aligned)<br>
                10 questions at a time · Solutions shown at end only</p></div>""")
                start_btn = gr.Button("▶ Begin Diagnostic", variant="primary", size="lg")

            with gr.Column(visible=False) as page1_col:
                gr.HTML('<div style="font-family:Georgia,serif;font-size:1.2rem;color:#f4c542;'
                        'border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:16px">'
                        'Questions 1–10 of 20 · SP211 Mechanics</div>')
                radios_p1 = []
                for i, q in enumerate(DIAGNOSTIC[:10]):
                    gr.HTML(f'<div class="q-block"><div class="q-label">Q{i+1} · {q["ch"]}</div>'
                            f'<div style="color:#f0ebe0;font-size:0.95rem;margin-bottom:8px">{q["q"]}</div>'
                            f'<div class="q-tag">Topic: {q["topic"]}</div></div>')
                    r = gr.Radio(choices=q["choices"], label="Your answer:", value=None, interactive=True)
                    radios_p1.append(r)
                next_btn = gr.Button("Next: Questions 11–20 (E&M) →", variant="primary")

            with gr.Column(visible=False) as page2_col:
                gr.HTML('<div style="font-family:Georgia,serif;font-size:1.2rem;color:#f4c542;'
                        'border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:16px">'
                        'Questions 11–20 of 20 · SP212 E&M (Purcell)</div>')
                radios_p2 = []
                for i, q in enumerate(DIAGNOSTIC[10:]):
                    gr.HTML(f'<div class="q-block"><div class="q-label">Q{i+11} · {q["ch"]}</div>'
                            f'<div style="color:#f0ebe0;font-size:0.95rem;margin-bottom:8px">{q["q"]}</div>'
                            f'<div class="q-tag">Topic: {q["topic"]}</div></div>')
                    r = gr.Radio(choices=q["choices"], label="Your answer:", value=None, interactive=True)
                    radios_p2.append(r)
                submit_btn = gr.Button("Submit &amp; See Results →", variant="primary")

            with gr.Column(visible=False) as results_col:
                results_html = gr.HTML("")
                pathway_md   = gr.Markdown("")
                results_img  = gr.Image(label="Performance Chart", visible=False, type="pil")
                concept_imgs = [gr.Image(label="", visible=False, type="pil") for _ in range(3)]
                restart_btn  = gr.Button("↺ Restart Diagnostic", variant="secondary")

        # ── TOPIC GUIDE ──────────────────────────────────────────────────────
        with gr.Tab("📚 Topic Guide"):
            topic_dd  = gr.Dropdown(choices=list(TOPICS.keys()), label="Select Topic",
                                    value=list(TOPICS.keys())[0])
            topic_out = gr.HTML("")
            topic_img = gr.Image(label="Visualization", visible=False, type="pil")

            def load_topic(topic):
                html = TOPIC_HTML.get(topic, "<p>No content.</p>")
                fn = PLOT_MAP.get(topic)
                if fn:
                    try:
                        return gr.update(value=html), gr.update(visible=True, value=fn())
                    except Exception:
                        pass
                return gr.update(value=html), gr.update(visible=False)

            topic_dd.change(load_topic, [topic_dd], [topic_out, topic_img])
            demo.load(load_topic, [topic_dd], [topic_out, topic_img])

        # ── STUDY PLAN ───────────────────────────────────────────────────────
        with gr.Tab("📅 Study Plan"):
            gr.Markdown(f"### USNA Physics Study Plan — {DAYS_LEFT} days until June 21\n\n"
                "> ⚡ **SP211 must be validated before SP212.** Pass mechanics first.\n\n"
                "**Week 1: June 2–7 — SP211 Mechanics Foundations**\n"
                "- Mon–Tue: Kinematics — 1D/2D equations, projectile motion, circular motion\n"
                "- Wed–Thu: Newton's Laws — FBD for every problem, inclines, Atwood machines\n"
                "- Fri: Work-Energy theorem — conservative vs non-conservative forces\n"
                "- Sat: Momentum and collisions — elastic vs perfectly inelastic\n"
                "- Sun: Timed SP211 practice — 10 problems\n\n"
                "**Week 2: June 8–14 — SP211 Complete + SP212 Start**\n"
                "- Mon: Rotational dynamics — moments of inertia table, τ=Iα, rolling KE\n"
                "- Tue: SHM — mass-spring and pendulum, energy in SHM, v_max=Aω\n"
                "- Wed: Gravitation — orbital mechanics, Kepler's laws, escape velocity\n"
                "- Thu–Fri: **SP212 Start** — Coulomb's law, Gauss's law (sphere/line/plane)\n"
                "- Sat: Electric potential — V from point charges, E=−∇V, equipotentials\n"
                "- Sun: **Mock SP211** — confirm pass before SP212 time\n\n"
                "**Week 3: June 15–20 — SP212 E&M (Purcell)**\n"
                "- Mon: Capacitance — parallel plate, energy, series/parallel combinations\n"
                "- Tue: DC circuits — Ohm's law, KVL/KCL, RC time constant τ=RC\n"
                "- Wed: Magnetism — force on charges/wires, Biot-Savart, Ampere's law\n"
                "- Thu: Solenoid and circular wire B fields\n"
                "- Fri: Faraday's law, Lenz's law, motional EMF, RL circuits\n"
                "- Sat: Maxwell's equations summary + **mock SP212 diagnostic**\n\n"
                "**June 21:** Full 20-question diagnostic + targeted review\n\n"
                "---\n*Daily minimum: 20 min concept → 30 min problems → 10 min FBD practice.*")

        # ── UNLOCK ──────────────────────────────────────────────────────────
        with gr.Tab("🔑 Unlock"):
            gr.Markdown("## Unlock Full Access\nEnter your FissionLab token.")
            tok_in  = gr.Textbox(label="Token", placeholder="FLAB-XXXX-XXXX-XXXX")
            tok_btn = gr.Button("Verify Token", variant="primary")
            tok_out = gr.Markdown("")
            gr.Markdown("No token? Contact **Dr_PrestonD@proton.me**")
            def verify_action(token, s):
                if verify_token(token):
                    s["verified"] = True; return s, "✅ **Premium access unlocked!**"
                return s, "❌ Invalid token. Contact Dr. Preston."
            tok_btn.click(verify_action, [tok_in, diag_state], [diag_state, tok_out])

    gr.HTML("<div style='text-align:center;color:#8fa8c8;font-size:0.78rem;padding:16px 0'>Dr. Preston · PhD · FissionLab · SP211/SP212 USNA Validation Prep · Purcell E&M</div>")

    # ── Diagnostic wiring ────────────────────────────────────────────────────
    def on_start(s):
        return {"page":1,"answers":{}}, gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    # NOTE: on_start shows intro initially — need to flip
    def on_start_fixed(s):
        return {"page":1,"answers":{}}, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

    def on_next(s, *radio_vals):
        answers = dict(s.get("answers", {}))
        for i, v in enumerate(radio_vals):
            if v is not None: answers[i] = v
        return {"page":2,"answers":answers}, gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

    def on_submit(s, *radio_vals):
        answers = dict(s.get("answers", {}))
        for i, v in enumerate(radio_vals):
            if v is not None: answers[i+10] = v
        s = {"page":3,"answers":answers}
        results_htm, scores, area_avg = build_results(answers)
        pathway = generate_pathway(scores)
        try: chart = plot_results(area_avg)
        except Exception: chart = None
        weak_topics = [t for t, sc in scores.items() if sc < 0.5]
        cimgs = []
        for t in weak_topics[:3]:
            fn = PLOT_MAP.get(t)
            try: cimgs.append(fn() if fn else None)
            except Exception: cimgs.append(None)
        while len(cimgs) < 3: cimgs.append(None)
        return (s,
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=True),
                gr.update(value=results_htm),
                gr.update(value=pathway),
                gr.update(visible=chart is not None, value=chart),
                gr.update(visible=cimgs[0] is not None, value=cimgs[0]),
                gr.update(visible=cimgs[1] is not None, value=cimgs[1]),
                gr.update(visible=cimgs[2] is not None, value=cimgs[2]))

    def on_restart(s):
        return {"page":0,"answers":{}}, gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    col_outs = [diag_state, intro_col, page1_col, page2_col, results_col]
    start_btn.click(on_start_fixed, [diag_state], col_outs)
    next_btn.click(on_next, [diag_state]+radios_p1, col_outs)
    submit_btn.click(on_submit, [diag_state]+radios_p2,
                     col_outs+[results_html, pathway_md, results_img]+concept_imgs)
    restart_btn.click(on_restart, [diag_state], col_outs)

if __name__ == "__main__":
    demo.launch()
