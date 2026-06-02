"""
FissionLab Physics — USNA SP211/SP212 Prep
Dr. Preston PhD · SP211 Mechanics + SP212 E&M (Purcell)
20-question diagnostic · 10 at a time · Solutions revealed at end only
SP211 must be validated before SP212
"""
import io, base64, re, math
from datetime import date
import requests
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['mathtext.fontset'] = 'cm'
import gradio as gr

PORTAL  = "https://web-production-202b9.up.railway.app/api/verify"
PATTERN = re.compile(r"^FLAB-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", re.IGNORECASE)
DAYS_LEFT = max(0, (date(2026, 6, 21) - date.today()).days)

def verify_token(token: str) -> bool:
    t = token.strip().upper()
    if not PATTERN.match(t): return False
    try:
        r = requests.get(PORTAL, params={"token": t}, timeout=5)
        return r.status_code == 200 and r.json().get("valid", False)
    except Exception:
        return False

CSS = """
body, .gradio-container, .main, .wrap {background:#0a1628!important;color:#f0ebe0!important}
h1,h2,h3 {color:#c9a84c!important;font-family:Georgia,serif}
.app-hdr {background:rgba(201,168,76,0.08);border-bottom:1px solid rgba(201,168,76,0.2);
  padding:16px 24px;margin-bottom:16px;border-radius:12px}
.q-block {background:rgba(13,31,60,0.8);border:1px solid rgba(201,168,76,0.2);
  border-radius:10px;padding:16px 20px;margin:12px 0}
.q-num {color:#c9a84c;font-weight:700;font-size:0.8rem;letter-spacing:0.08em;
  text-transform:uppercase;margin-bottom:6px}
.q-text {color:#f0ebe0;font-size:0.95rem;line-height:1.55;margin-bottom:6px}
.q-tag {color:rgba(240,235,224,0.35);font-size:0.7rem}
.correct-row {background:rgba(40,200,100,0.1);border-left:3px solid #28c864;
  padding:10px 14px;border-radius:0 8px 8px 0;margin:6px 0;font-size:0.9rem}
.wrong-row {background:rgba(255,80,80,0.08);border-left:3px solid #ff5050;
  padding:10px 14px;border-radius:0 8px 8px 0;margin:6px 0;font-size:0.9rem}
.sol-box {background:rgba(10,25,55,0.7);border:1px solid rgba(100,150,255,0.15);
  border-radius:8px;padding:12px 16px;margin:6px 0;font-size:0.87rem;
  color:rgba(240,235,224,0.82)}
.score-banner {text-align:center;padding:28px 20px;
  background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.25);
  border-radius:12px;margin-bottom:20px}
.pg-hdr {font-family:Georgia,serif;font-size:1.15rem;color:#c9a84c;
  border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:18px}
.warn-box {background:rgba(255,120,50,0.1);border-left:3px solid #ff7832;
  padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0;font-size:0.9rem;
  color:rgba(255,180,120,0.9)}
.tip-box {background:rgba(201,168,76,0.1);border-left:3px solid #c9a84c;
  padding:12px 16px;border-radius:0 8px 8px 0;margin:14px 0;font-size:0.9rem}
label, .label-wrap {color:rgba(240,235,224,0.7)!important;font-size:0.82rem!important}
input[type=text], textarea {background:rgba(255,255,255,0.06)!important;
  border:1px solid rgba(255,255,255,0.15)!important;color:#f0ebe0!important;
  border-radius:8px!important}
.gr-button.primary, button.primary {background:#c9a84c!important;color:#0a1628!important;
  font-weight:700!important;border:none!important}
.gr-button.secondary, button.secondary {background:rgba(255,255,255,0.07)!important;
  color:#c9a84c!important;border:1px solid rgba(201,168,76,0.3)!important}
.tabitem {background:#0a1628!important}
.tab-nav button {color:rgba(240,235,224,0.55)!important;background:transparent!important}
.tab-nav button.selected {color:#c9a84c!important;border-bottom-color:#c9a84c!important}
footer {display:none!important}
"""
DIV = '<hr style="border:none;border-top:1px solid rgba(201,168,76,0.2);margin:20px 0">'

# ── Formula renderer ──────────────────────────────────────────────────────────
def fimg(latex: str, fs: int = 14) -> str:
    try:
        fig, ax = plt.subplots(figsize=(7.5, 0.72))
        fig.patch.set_facecolor('#0d1f3c')
        ax.set_facecolor('#0d1f3c')
        ax.axis('off')
        ax.text(0.5, 0.5, r'$' + latex + r'$', transform=ax.transAxes,
                ha='center', va='center', fontsize=fs, color='#f0ebe0')
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=130, bbox_inches='tight',
                    facecolor='#0d1f3c', edgecolor='none')
        buf.seek(0); plt.close(fig)
        b64 = base64.b64encode(buf.read()).decode()
        return (f'<img src="data:image/png;base64,{b64}" '
                f'style="display:block;margin:10px auto;max-width:92%;border-radius:5px">')
    except Exception:
        return f'<div style="color:#c9a84c;font-family:monospace;padding:6px 0">{latex}</div>'

FIMGS = {k: fimg(v) for k, v in {
    'kinem':    r'v=v_0+at;\quad x=x_0+v_0t+\tfrac{1}{2}at^2;\quad v^2=v_0^2+2a\Delta x',
    'range':    r'R = \frac{v_0^2\sin(2\theta)}{g}\quad\text{(max at }\theta=45°)',
    'newton2':  r'\sum \mathbf{F} = m\mathbf{a}',
    'we_thm':   r'W_{net} = \Delta K = K_f - K_i',
    'e_cons':   r'K_i + U_i = K_f + U_f\quad\text{(no friction)}',
    'momentum': r'\mathbf{J} = \Delta\mathbf{p} = \int \mathbf{F}\,dt',
    'torque':   r'\sum\tau = I\alpha',
    'ang_mom':  r'L = I\omega;\quad\tau_{net} = \frac{dL}{dt}',
    'shm':      r'x(t)=A\cos(\omega t+\phi);\quad\omega=\sqrt{k/m};\quad T=2\pi\sqrt{m/k}',
    'pendulum': r'T = 2\pi\sqrt{L/g};\quad\omega=\sqrt{g/L}',
    'gravity':  r'F=\frac{Gm_1m_2}{r^2};\quad U=-\frac{Gm_1m_2}{r}',
    'orbital':  r'v_{orb}=\sqrt{\frac{GM}{r}};\quad v_{esc}=\sqrt{\frac{2GM}{R}}',
    'coulomb':  r'F=\frac{k|q_1||q_2|}{r^2},\quad k=\frac{1}{4\pi\varepsilon_0}=9\times10^9',
    'efield':   r'\mathbf{E}=\frac{k|q|}{r^2}\hat{r};\quad\mathbf{F}=q\mathbf{E}',
    'gauss':    r'\oint\mathbf{E}\cdot d\mathbf{A}=\frac{Q_{enc}}{\varepsilon_0}',
    'potential':r'V=\frac{kq}{r};\quad\mathbf{E}=-\nabla V',
    'cap':      r'C=\frac{Q}{V}=\frac{\varepsilon_0 A}{d};\quad U=\tfrac{1}{2}CV^2',
    'ohm':      r'V=IR;\quad P=IV=I^2R=\frac{V^2}{R}',
    'rc':       r'\tau=RC;\quad q(t)=Q\!\left(1-e^{-t/\tau}\right)',
    'ampere':   r'\oint\mathbf{B}\cdot d\mathbf{l}=\mu_0 I_{enc}',
    'solenoid': r'B=\mu_0 nI\quad\text{(inside solenoid)};\quad\mu_0=4\pi\times10^{-7}',
    'faraday':  r'\mathcal{E}=-\frac{d\Phi_B}{dt};\quad\Phi_B=\iint\mathbf{B}\cdot d\mathbf{A}',
}.items()}

def _sec(title, body, keys=None):
    p = [f'<div style="max-width:860px;line-height:1.72">',
         f'<h3 style="font-family:Georgia,serif;color:#c9a84c;border-bottom:1px solid '
         f'rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:14px">{title}</h3>',
         f'<div style="color:rgba(240,235,224,0.87);font-size:0.92rem">{body}</div>']
    if keys:
        p.append('<div style="margin:14px 0">' + ''.join(FIMGS.get(k,'') for k in keys) + '</div>')
    p.append('</div>')
    return '\n'.join(p)

SHEETS = {
    "SP211 — Kinematics": _sec("SP211 — Kinematics",
        "<b>1D const. acceleration:</b> v=v₀+at, x=x₀+v₀t+½at², v²=v₀²+2aΔx<br>"
        "<b>Calculus:</b> v=dx/dt, a=dv/dt. For variable a: integrate.<br>"
        "<b>Projectile</b> (a_x=0, a_y=−g): x=v₀cosθ·t, y=v₀sinθ·t−½gt²<br>"
        "<b>Circular motion:</b> a_c=v²/r (toward center). Constant speed ≠ zero acceleration.",
        ['kinem','range']),
    "SP211 — Newton's Laws": _sec("SP211 — Newton's Laws",
        "<b>1st:</b> ΣF=0 ↔ constant velocity. <b>2nd:</b> ΣF=ma (by component for each object).<br>"
        "<b>3rd:</b> F₁₂=−F₂₁ — on DIFFERENT objects. Never add action-reaction pairs within one FBD.<br>"
        "<b>On incline:</b> a=g sinθ (frictionless). N=mg cosθ (normal ⊥ surface).<br>"
        '<div class="tip-box"><b>Draw a FBD for each object separately.</b> Never skip this step.</div>',
        ['newton2']),
    "SP211 — Work & Energy": _sec("SP211 — Work &amp; Energy",
        "<b>Work:</b> W=F·d·cosθ. Variable force: W=∫F(x)dx.<br>"
        "<b>KE:</b> K=½mv². <b>PE:</b> U_g=mgh, U_spring=½kx².<br>"
        "<b>Conservation:</b> K_i+U_i=K_f+U_f (no friction). With friction: W_nc=ΔE=ΔK+ΔU.<br>"
        "<b>Power:</b> P=dW/dt=F·v. <b>Spring release:</b> v=x√(k/m).",
        ['we_thm','e_cons']),
    "SP211 — Momentum": _sec("SP211 — Momentum &amp; Collisions",
        "<b>Elastic:</b> KE conserved. Equal masses: velocities exchange.<br>"
        "<b>Perfectly inelastic:</b> objects stick. (m₁+m₂)v_f=m₁v₁+m₂v₂<br>"
        "<b>Atwood:</b> a=(m₂−m₁)g/(m₁+m₂)",
        ['momentum']),
    "SP211 — Rotation": _sec("SP211 — Rotational Dynamics",
        "<b>Analogies:</b> τ=Iα (like F=ma), L=Iω (like p=mv).<br>"
        "<b>Moments of inertia:</b> Solid disk: ½MR² · Hollow ring: MR² · Solid sphere: ⅖MR²<br>"
        "Rod (center): ML²/12 · Rod (end): ML²/3 · <b>Parallel axis:</b> I=I_cm+Md²<br>"
        "<b>Rolling KE:</b> KE=½mv_cm²+½Iω². <b>Conservation L:</b> τ_net=0 → Iω=const.",
        ['torque','ang_mom']),
    "SP211 — SHM": _sec("SP211 — Simple Harmonic Motion",
        "<b>Condition:</b> linear restoring force F=−kx.<br>"
        "<b>v_max=Aω</b> (at x=0). <b>v at x:</b> v=ω√(A²−x²). <b>E=½kA²</b>=constant.<br>"
        "Period does NOT depend on amplitude. Pendulum period does NOT depend on mass.",
        ['shm','pendulum']),
    "SP211 — Gravitation": _sec("SP211 — Gravitation",
        "<b>Newton:</b> F=Gm₁m₂/r². <b>PE:</b> U=−Gm₁m₂/r (zero at r=∞).<br>"
        "<b>Circular orbit:</b> gravity=centripetal → v=√(GM/r).<br>"
        "<b>Escape:</b> v_esc=√(2GM/R). <b>Kepler 3:</b> T²=4π²a³/(GM). G=6.674×10⁻¹¹ N·m²/kg².",
        ['gravity','orbital']),
    "SP212 — Coulomb & Field": _sec("SP212 — Electric Force &amp; Field · Purcell Ch. 1",
        "<b>Coulomb:</b> F=kq₁q₂/r², k=9×10⁹ N·m²/C², ε₀=8.85×10⁻¹² C²/(N·m²).<br>"
        "<b>Gauss (symmetric distributions):</b><br>"
        "Outside sphere: E=kQ/r² · Inside uniform sphere: E=kQr/R³ · Infinite line: E=λ/(2πε₀r)",
        ['coulomb','efield','gauss']),
    "SP212 — Potential": _sec("SP212 — Electric Potential · Purcell Ch. 2",
        "<b>V</b> is scalar: V=kq/r. Multiple charges: V=Σkqᵢ/rᵢ (scalar sum — easier than E field!).<br>"
        "<b>E=−∇V.</b> Field points from high V to low V. Equipotentials ⊥ field lines.<br>"
        "<b>Conductors:</b> E=0 inside; surface is equipotential.",
        ['potential']),
    "SP212 — Circuits": _sec("SP212 — Capacitance &amp; Circuits · Purcell Ch. 3–4",
        "<b>Series C:</b> 1/C_eq=Σ1/Cᵢ. <b>Parallel C:</b> C_eq=ΣCᵢ.<br>"
        "<b>Series R:</b> R_eq=ΣRᵢ. <b>Parallel R:</b> 1/R_eq=Σ1/Rᵢ.<br>"
        "<b>KVL:</b> ΣV=0 around any loop. <b>KCL:</b> ΣI into node=0.<br>"
        "<b>RC:</b> τ=RC. At t=τ: ~63% charged.",
        ['cap','ohm','rc']),
    "SP212 — Magnetism": _sec("SP212 — Magnetism · Purcell Ch. 5–6",
        "<b>Force:</b> F=qv×B. Force on wire: F=IL×B. <b>Magnetic force does NO work.</b><br>"
        "<b>Circular radius:</b> r=mv/(qB).<br>"
        "<b>Wire:</b> B=μ₀I/(2πr). <b>Solenoid:</b> B=μ₀nI (inside only). μ₀=4π×10⁻⁷ T·m/A.",
        ['ampere','solenoid']),
    "SP212 — Faraday": _sec("SP212 — Faraday &amp; Induction · Purcell Ch. 7",
        "<b>Faraday:</b> ε=−dΦ_B/dt. Flux: Φ=BA cosθ.<br>"
        "<b>Lenz:</b> induced current opposes the change in flux.<br>"
        "<b>Motional EMF:</b> ε=BLv. <b>Maxwell equations:</b><br>"
        "∮E·dA=Q/ε₀ · ∮B·dA=0 · ε=−dΦ_B/dt · ∮B·dl=μ₀(I+ε₀dΦ_E/dt)",
        ['faraday']),
}

# ── 20 Pre-generated questions ────────────────────────────────────────────────
# Q1-10: SP211 Mechanics · Q11-20: SP212 E&M (Purcell aligned)
QUESTIONS = [
    {"n":1,"area":"SP211","text":"Ball launched at θ=30°, v₀=20 m/s. Horizontal range? (g=10 m/s²)",
     "choices":["A) 20 m","B) 20√3 m ≈ 34.6 m","C) 40 m","D) 30 m"],"ans":"B)","ch":"SP211 Kinematics",
     "sol":"R=v₀²sin(2θ)/g=(400·sin60°)/10=40·(√3/2)=<b>20√3≈34.6 m</b>. Max range at 45°."},
    {"n":2,"area":"SP211","text":"5 kg block on frictionless 30° incline. Acceleration down the slope? (g=9.8 m/s²)",
     "choices":["A) 9.8 m/s²","B) 4.9 m/s²","C) 8.5 m/s²","D) 0 m/s²"],"ans":"B)","ch":"SP211 Newton's Laws",
     "sol":"a=g sin30°=9.8×0.5=<b>4.9 m/s²</b>. N=mg cos30° has no component along incline."},
    {"n":3,"area":"SP211","text":"Spring k=200 N/m compressed 0.1 m releases a 0.5 kg block. Speed when released?",
     "choices":["A) 1 m/s","B) 2 m/s","C) √2 m/s","D) 4 m/s"],"ans":"B)","ch":"SP211 Work & Energy",
     "sol":"½kx²=½mv². v=x√(k/m)=0.1√(200/0.5)=0.1×20=<b>2 m/s</b>."},
    {"n":4,"area":"SP211","text":"3 kg block at 4 m/s collides and sticks with stationary 5 kg block. Final velocity?",
     "choices":["A) 1.5 m/s","B) 2 m/s","C) 2.4 m/s","D) 4 m/s"],"ans":"A)","ch":"SP211 Momentum",
     "sol":"3(4)=(3+5)v_f → v_f=12/8=<b>1.5 m/s</b>. KE is NOT conserved (perfectly inelastic)."},
    {"n":5,"area":"SP211","text":"Solid disk (I=½MR²) rolls down incline descending h=2 m. Speed at bottom? (g=9.8 m/s²)",
     "choices":["A) √(4gh/3)≈5.1 m/s","B) √(2gh)≈6.3 m/s","C) √(gh)≈4.4 m/s","D) √(4gh/5)≈4.0 m/s"],
     "ans":"A)","ch":"SP211 Rotation",
     "sol":"Mgh=¾Mv². v=√(4gh/3)=√(4·9.8·2/3)≈<b>5.1 m/s</b>. Uses BOTH translational + rotational KE."},
    {"n":6,"area":"SP211","text":"Mass-spring: m=0.4 kg, k=100 N/m, A=0.05 m. Maximum speed?",
     "choices":["A) 0.79 m/s","B) 1.25 m/s","C) 0.5 m/s","D) 2.5 m/s"],"ans":"A)","ch":"SP211 SHM",
     "sol":"ω=√(100/0.4)=√250≈15.81 rad/s. v_max=Aω=0.05×15.81≈<b>0.79 m/s</b>."},
    {"n":7,"area":"SP211","text":"Orbital speed of satellite at altitude h? (M_E=Earth mass, R_E=Earth radius)",
     "choices":["A) √(GM_E/h)","B) √(GM_E/(R_E+h))","C) √(2GM_E/R_E)","D) √(GM_E·R_E)"],
     "ans":"B)","ch":"SP211 Gravitation",
     "sol":"Gravity=centripetal: GM_E/(R_E+h)²=v²/(R_E+h) → v=<b>√(GM_E/(R_E+h))</b>. C is escape velocity."},
    {"n":8,"area":"SP211","text":"Torque τ=40 N·m on flywheel I=8 kg·m². Starting from rest, ω after 5 s?",
     "choices":["A) 25 rad/s","B) 40 rad/s","C) 5 rad/s","D) 200 rad/s"],"ans":"A)","ch":"SP211 Rotation",
     "sol":"α=τ/I=40/8=5 rad/s². ω=αt=5×5=<b>25 rad/s</b>. (τ=Iα ↔ F=ma)"},
    {"n":9,"area":"SP211","text":"Particle moves at constant speed v in circle of radius r. Its acceleration is:",
     "choices":["A) v²/r toward center","B) v/r²","C) Zero — constant speed","D) 2πv/T"],
     "ans":"A)","ch":"SP211 Kinematics",
     "sol":"Centripetal a=<b>v²/r</b> toward center. Speed constant but direction changes → a≠0."},
    {"n":10,"area":"SP211","text":"Atwood machine: m₁=3 kg, m₂=5 kg, massless frictionless pulley. Acceleration?",
     "choices":["A) g/4≈2.45 m/s²","B) g/2≈4.9 m/s²","C) g/8≈1.23 m/s²","D) 2g/5≈3.92 m/s²"],
     "ans":"A)","ch":"SP211 Newton's Laws",
     "sol":"Net force=(5−3)(9.8)=19.6 N. Total mass=8 kg. a=19.6/8=<b>g/4≈2.45 m/s²</b>."},
    {"n":11,"area":"SP212","text":"+q and −q separated by d. Electric potential at the midpoint?",
     "choices":["A) 2kq/d","B) kq/(d/2)","C) 0","D) −kq/d"],"ans":"C)","ch":"Purcell Ch. 2",
     "sol":"V=kq/(d/2)+k(−q)/(d/2)=<b>0</b>. Potential is SCALAR — superpose directly."},
    {"n":12,"area":"SP212","text":"Parallel-plate capacitor with charge Q. Plate separation doubled. V changes how?",
     "choices":["A) Doubles","B) Halves","C) Same","D) Quadruples"],"ans":"A)","ch":"Purcell Ch. 3",
     "sol":"C=ε₀A/d. Double d → C halves → V=Q/C <b>doubles</b> (Q fixed)."},
    {"n":13,"area":"SP212","text":"Gauss's Law: E outside uniformly charged sphere (charge Q, radius R) at r>R?",
     "choices":["A) kQ/r²","B) kQr/R³","C) kQ/R²","D) 0"],"ans":"A)","ch":"Purcell Ch. 1",
     "sol":"Gauss: E·4πr²=Q/ε₀ → E=<b>kQ/r²</b>. Same as point charge. B is inside the sphere."},
    {"n":14,"area":"SP212","text":"Three 6-Ω resistors in parallel. Equivalent resistance?",
     "choices":["A) 18 Ω","B) 6 Ω","C) 2 Ω","D) 3 Ω"],"ans":"C)","ch":"Purcell Ch. 4",
     "sol":"1/R_eq=1/6+1/6+1/6=1/2 → R_eq=<b>2 Ω</b>. (Series would give 18 Ω.)"},
    {"n":15,"area":"SP212","text":"Proton (q=1.6×10⁻¹⁹ C) at 10⁶ m/s in +x, B=0.1 T in +z. |F|=?",
     "choices":["A) 1.6×10⁻¹⁴ N","B) 1.6×10⁻²⁰ N","C) 10⁻²⁵ N","D) 1.6×10⁻⁸ N"],
     "ans":"A)","ch":"Purcell Ch. 5",
     "sol":"F=qvBsin90°=(1.6×10⁻¹⁹)(10⁶)(0.1)=<b>1.6×10⁻¹⁴ N</b>. Magnetic force does NO work."},
    {"n":16,"area":"SP212","text":"RC circuit: R=10 kΩ, C=100 μF. Time constant τ?",
     "choices":["A) 1 s","B) 0.1 s","C) 10 s","D) 1000 s"],"ans":"A)","ch":"Purcell Ch. 4",
     "sol":"τ=RC=(10⁴)(10⁻⁴)=<b>1 s</b>. At t=τ: ~63% charged."},
    {"n":17,"area":"SP212","text":"Solenoid: n=1000 turns/m, I=2 A. B inside? (μ₀=4π×10⁻⁷ T·m/A)",
     "choices":["A) 2.51×10⁻³ T","B) 2π×10⁻³ T","C) 4π×10⁻⁷ T","D) 4π×10⁻³ T"],
     "ans":"A)","ch":"Purcell Ch. 6",
     "sol":"B=μ₀nI=(4π×10⁻⁷)(1000)(2)=8π×10⁻⁴≈<b>2.51×10⁻³ T</b>. Zero outside (ideal solenoid)."},
    {"n":18,"area":"SP212","text":"Square loop (0.2 m side) in B=0.5 T ⊥ to loop. B decreases at 2 T/s. |EMF|?",
     "choices":["A) 0.08 V","B) 0.02 V","C) 0.2 V","D) 0.5 V"],"ans":"A)","ch":"Purcell Ch. 7",
     "sol":"|EMF|=A|dB/dt|=0.04×2=<b>0.08 V</b>. Lenz's law gives direction."},
    {"n":19,"area":"SP212","text":"Charge q=2 μC at point where V=150 V. Electric potential energy U?",
     "choices":["A) 3×10⁻⁴ J","B) 7.5×10⁻⁵ J","C) 6×10⁻⁴ J","D) 1.5×10⁻⁴ J"],
     "ans":"A)","ch":"Purcell Ch. 2",
     "sol":"U=qV=(2×10⁻⁶)(150)=<b>3×10⁻⁴ J</b>."},
    {"n":20,"area":"SP212","text":"Gauss's Law for magnetism: total magnetic flux through any closed surface is:",
     "choices":["A) Q_enc/ε₀","B) μ₀I_enc","C) Zero","D) −dΦ_E/dt"],"ans":"C)","ch":"Purcell Ch. 7",
     "sol":"∮B·dA=<b>0</b>. No magnetic monopoles — B field lines always close on themselves."},
]
assert len(QUESTIONS) == 20

# ── Matplotlib helpers ────────────────────────────────────────────────────────
_DK = {"figure.facecolor":"#0b1a2e","axes.facecolor":"#112240","axes.edgecolor":"#8fa8c8",
       "axes.labelcolor":"#e8eaf0","xtick.color":"#8fa8c8","ytick.color":"#8fa8c8",
       "text.color":"#e8eaf0","grid.color":"#1e3a5f","grid.alpha":0.4}

def _mkfig(w=7, h=4):
    for k, v in _DK.items(): plt.rcParams[k] = v
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_facecolor("#0b1a2e"); ax.set_facecolor("#112240"); ax.grid(True)
    return fig, ax

def _topil(fig):
    from PIL import Image as PILImage
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    plt.close(fig); buf.seek(0)
    return PILImage.open(buf)

def _plt_projectile():
    fig, ax = _mkfig()
    g = 9.8
    for angle, color in [(30,"#c9a84c"),(45,"#4fc3f7"),(60,"#81c784")]:
        theta = math.radians(angle); T = 2*20*math.sin(theta)/g
        t = np.linspace(0, T, 300)
        ax.plot(20*math.cos(theta)*t, 20*math.sin(theta)*t-0.5*g*t**2,
                color=color, lw=2, label=f"{angle}°")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)"); ax.legend(fontsize=9)
    ax.set_title("Projectile Motion v₀=20 m/s — Max range at 45°", color="#c9a84c", fontsize=10)
    return _topil(fig)

def _plt_shm():
    fig, ax = _mkfig()
    t = np.linspace(0, 6*np.pi, 500); w = 1.0
    ax.plot(t, np.cos(w*t), color="#c9a84c", lw=2, label="x(t)=A cos(ωt)")
    ax.plot(t, -np.sin(w*t), color="#4fc3f7", lw=2, ls="--", label="v(t)/(Aω)")
    ax.set_xlabel("t"); ax.legend(fontsize=9)
    ax.set_title("SHM — Position and Velocity", color="#c9a84c", fontsize=11)
    return _topil(fig)

def _plt_gauss():
    fig, ax = _mkfig(6, 5)
    ax.set_aspect("equal"); ax.grid(False)
    for r, c, lbl in [(2.5,"#4fc3f7","Gaussian surface r>R"),(1.0,"#c9a84c","Charged sphere R")]:
        ax.add_patch(plt.Circle((0,0), r, fill=False, color=c, lw=2, label=lbl))
    ax.plot(0, 0, 'o', color="#ff6b6b", ms=8, label="+Q at center")
    for ang in range(0, 360, 45):
        th = math.radians(ang); s = 2.5
        ax.annotate("", xy=(s*math.cos(th), s*math.sin(th)),
                    xytext=(1.2*math.cos(th), 1.2*math.sin(th)),
                    arrowprops=dict(arrowstyle="->", color="#4fc3f7", lw=1.5))
    ax.set_xlim(-3.5,3.5); ax.set_ylim(-3.5,3.5)
    ax.set_title("Gauss's Law — E outside sphere = kQ/r²", color="#c9a84c", fontsize=10)
    ax.legend(fontsize=8)
    return _topil(fig)

def _plt_rc():
    fig, ax = _mkfig()
    t = np.linspace(0, 5, 400)
    for tau, c in [(0.5,"#c9a84c"),(1.0,"#4fc3f7"),(2.0,"#81c784")]:
        ax.plot(t, 1-np.exp(-t/tau), color=c, lw=2, label=f"τ={tau}s")
    ax.axhline(1-math.exp(-1), color="white", ls=":", lw=1, alpha=0.5, label="63% at t=τ")
    ax.set_xlabel("t (s)"); ax.set_ylabel("q/Q_max"); ax.legend(fontsize=9)
    ax.set_title("RC Charging: q(t)=Q(1−e^{−t/τ})", color="#c9a84c", fontsize=11)
    return _topil(fig)

def _plt_results(m_sc, e_sc):
    fig, ax = _mkfig(7, 2.2)
    cats = ["SP211 Mechanics (Q1-10)", "SP212 E&M (Q11-20)"]
    vals = [m_sc, e_sc]
    bars = ax.barh(cats, vals, color=["#c9a84c" if v>=0.6 else "#ff5050" for v in vals], height=0.5)
    ax.set_xlim(0, 1); ax.set_xlabel("Score")
    ax.set_title("Diagnostic Results", color="#c9a84c", fontsize=11)
    for bar, val in zip(bars, vals):
        ax.text(val+0.02, bar.get_y()+bar.get_height()/2,
                f"{val*100:.0f}%", va="center", color="#e8eaf0", fontsize=10)
    return _topil(fig)

SHEET_PLOTS = {
    "SP211 — Kinematics": _plt_projectile,
    "SP211 — SHM":        _plt_shm,
    "SP212 — Coulomb & Field": _plt_gauss,
    "SP212 — Circuits":   _plt_rc,
}
CONCEPT_PLOTS = {"SP211": _plt_projectile, "SP212": _plt_rc}

# ── Results builder ───────────────────────────────────────────────────────────
def build_results(answers: dict):
    correct = 0; hits = {"SP211":[0,0],"SP212":[0,0]}
    rows = []
    for q in QUESTIONS:
        i = q["n"] - 1
        chosen = answers.get(i, "")
        right = bool(chosen and chosen.startswith(q["ans"]))
        if right: correct += 1
        area = q["area"]
        hits[area][1] += 1
        if right: hits[area][0] += 1
        icon = "✅" if right else "❌"
        cls = "correct-row" if right else "wrong-row"
        rows.append(
            f'<div class="q-block">'
            f'<div class="q-num">Q{q["n"]} &nbsp;·&nbsp; {q["ch"]}</div>'
            f'<div class="q-text">{q["text"]}</div>'
            f'<div class="{cls}">{icon} Your answer: <b>{chosen or "(no answer)"}</b>'
            f' &nbsp;·&nbsp; Correct: <b>{q["ans"]}</b></div>'
            f'<div class="sol-box"><b>Solution:</b> {q["sol"]}</div>'
            f'</div>'
        )
    m_sc = hits["SP211"][0]/hits["SP211"][1]
    e_sc = hits["SP212"][0]/hits["SP212"][1]
    pct = correct/20*100
    col = "#28c864" if pct>=70 else ("#c9a84c" if pct>=50 else "#ff5050")
    banner = (
        f'<div class="score-banner">'
        f'<div style="font-family:Georgia,serif;font-size:3rem;font-weight:700;color:{col}">{correct}/20</div>'
        f'<div style="color:rgba(240,235,224,0.55);margin-top:6px">{pct:.0f}% correct</div>'
        f'<div style="display:flex;gap:20px;justify-content:center;margin-top:14px">'
        + ''.join(
            f'<div style="background:rgba(255,255,255,0.05);padding:10px 18px;border-radius:8px">'
            f'<div style="font-size:0.7rem;color:rgba(240,235,224,0.4)">{lb}</div>'
            f'<div style="color:#c9a84c;font-weight:700;font-size:1.1rem">{sc*100:.0f}%</div></div>'
            for lb, sc in [("SP211 Mechanics",m_sc),("SP212 E&M",e_sc)]
        )
        + '</div>'
        f'<div class="warn-box" style="margin-top:14px;max-width:420px;margin-left:auto;'
        f'margin-right:auto;font-size:0.82rem">⚡ SP211 must be validated before SP212</div>'
        f'</div>'
    )
    try: chart = _plt_results(m_sc, e_sc)
    except Exception: chart = None
    return banner + DIV + "\n".join(rows), chart, m_sc, e_sc

# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="FissionLab Physics — Dr. Preston") as demo:

    gr.HTML('<div class="app-hdr" style="display:flex;align-items:center;gap:14px">'
            '<span style="font-size:2.2rem">⚛️</span>'
            '<div><div style="font-family:Georgia,serif;font-size:1.4rem;font-weight:700;color:#c9a84c">'
            'FissionLab Physics — USNA SP211/SP212 Prep</div>'
            '<div style="font-size:0.82rem;color:rgba(240,235,224,0.45)">'
            'Dr. Preston · Mechanics + E&M · Purcell aligned · 20-question diagnostic</div>'
            '</div></div>')

    with gr.Tabs():

        with gr.Tab("🎯 Diagnostic"):
            diag_state = gr.State({"page": 0, "answers": {}})

            with gr.Column(visible=True) as intro_col:
                gr.HTML(
                    '<div style="text-align:center;padding:36px 20px">'
                    '<div style="font-family:Georgia,serif;font-size:1.5rem;color:#c9a84c;margin-bottom:12px">'
                    '20-Question Diagnostic</div>'
                    '<div class="warn-box" style="max-width:480px;margin:0 auto 16px;text-align:left">'
                    '⚡ <b>USNA requirement:</b> SP211 (mechanics) must be validated '
                    'before you can sit SP212 (E&M). Prioritize Q1–10.</div>'
                    '<div style="color:rgba(240,235,224,0.65);max-width:500px;margin:0 auto 24px;line-height:1.65">'
                    'Q1–10: SP211 Mechanics &nbsp;·&nbsp; Q11–20: SP212 E&M (Purcell)<br>'
                    '<b style="color:#c9a84c">10 questions visible at a time</b> — answer all 10, then click Next'
                    '</div></div>'
                )
                start_btn = gr.Button("▶ Begin Diagnostic", variant="primary", size="lg")

            with gr.Column(visible=False) as page1_col:
                gr.HTML('<div class="pg-hdr">Questions 1–10 of 20 &nbsp;·&nbsp; SP211 Mechanics</div>')
                radios_p1 = []
                for q in QUESTIONS[:10]:
                    gr.HTML(f'<div class="q-block">'
                            f'<div class="q-num">Q{q["n"]} &nbsp;·&nbsp; {q["ch"]}</div>'
                            f'<div class="q-text">{q["text"]}</div>'
                            f'<div class="q-tag">Area: {q["area"]}</div></div>')
                    radios_p1.append(
                        gr.Radio(choices=q["choices"], label="Your answer:", value=None, interactive=True)
                    )
                gr.HTML('<div style="margin-top:16px"></div>')
                next_btn = gr.Button("Next: Questions 11–20 (E&M) →", variant="primary")

            with gr.Column(visible=False) as page2_col:
                gr.HTML('<div class="pg-hdr">Questions 11–20 of 20 &nbsp;·&nbsp; SP212 E&M (Purcell)</div>')
                radios_p2 = []
                for q in QUESTIONS[10:]:
                    gr.HTML(f'<div class="q-block">'
                            f'<div class="q-num">Q{q["n"]} &nbsp;·&nbsp; {q["ch"]}</div>'
                            f'<div class="q-text">{q["text"]}</div>'
                            f'<div class="q-tag">Area: {q["area"]}</div></div>')
                    radios_p2.append(
                        gr.Radio(choices=q["choices"], label="Your answer:", value=None, interactive=True)
                    )
                gr.HTML('<div style="margin-top:16px"></div>')
                submit_btn = gr.Button("Submit All &amp; See Results →", variant="primary")

            with gr.Column(visible=False) as results_col:
                results_html  = gr.HTML("")
                results_chart = gr.Image(label="Score Chart", visible=False, type="pil")
                cimgs         = [gr.Image(label="", visible=False, type="pil") for _ in range(2)]
                pathway_md    = gr.Markdown("")
                gr.HTML(DIV)
                restart_btn   = gr.Button("↺ Restart Diagnostic", variant="secondary")

        with gr.Tab("⚛️ Cheat Sheets"):
            sheet_dd  = gr.Dropdown(choices=list(SHEETS.keys()), label="Select Topic",
                                    value=list(SHEETS.keys())[0])
            sheet_out = gr.HTML("")
            sheet_img = gr.Image(label="Visualization", visible=False, type="pil")

            def load_sheet(topic):
                html = SHEETS.get(topic, "<p>No content.</p>")
                fn = SHEET_PLOTS.get(topic)
                if fn:
                    try: return gr.update(value=html), gr.update(visible=True, value=fn())
                    except Exception: pass
                return gr.update(value=html), gr.update(visible=False)

            sheet_dd.change(load_sheet, [sheet_dd], [sheet_out, sheet_img])
            demo.load(load_sheet, [sheet_dd], [sheet_out, sheet_img])

        with gr.Tab("📅 Study Plan"):
            gr.Markdown(
                f"### USNA Physics Plan — {DAYS_LEFT} days until June 21\n\n"
                "> ⚡ **SP211 must be validated before SP212.** Pass mechanics first.\n\n"
                "**Week 1 (Jun 2–7) — SP211 Mechanics**\n"
                "- Mon–Tue: Kinematics — 1D/2D equations, projectile motion, circular motion\n"
                "- Wed: Newton's Laws — FBD for EVERY problem (don't skip this)\n"
                "- Thu: Work-Energy theorem — conservation vs non-conservative\n"
                "- Fri: Momentum — elastic vs perfectly inelastic. Atwood machine.\n"
                "- Sat: Rotation — moments of inertia table, τ=Iα, rolling KE formula\n"
                "- Sun: SHM + Gravitation — period formulas, orbital speed, escape velocity\n\n"
                "**Week 2 (Jun 8–14) — SP211 Mock + SP212 Start**\n"
                "- Mon: **Mock SP211** — timed 10-problem test. Review all misses.\n"
                "- Tue–Wed: SP212 Coulomb's law, Gauss's law (sphere/line/plane symmetry)\n"
                "- Thu: Electric potential — V from point charges, E=−∇V, equipotentials\n"
                "- Fri: Capacitance — C=Q/V, parallel plate, energy stored, series/parallel\n"
                "- Sat: DC circuits — Ohm's, KVL/KCL, RC time constant τ=RC\n"
                "- Sun: Light review\n\n"
                "**Week 3 (Jun 15–20) — SP212 E&M**\n"
                "- Mon: Magnetism — force on charge (F=qv×B), Biot-Savart, Ampere's law\n"
                "- Tue: Solenoid B field, magnetic force on wires, circular orbit r=mv/(qB)\n"
                "- Wed: Faraday's law, Lenz's law, motional EMF ε=BLv\n"
                "- Thu: Maxwell's equations (4 equations — know what each says)\n"
                "- Fri–Sat: **Mock SP212** diagnostic + targeted review\n\n"
                "**June 21 — Final Review:** Full 20-question diagnostic + weak area drill\n\n"
                "---\n*Daily: 20 min concept → 30 min problems → 10 min FBD practice*"
            )

        with gr.Tab("🔑 Unlock"):
            gr.Markdown("## Verify Access\nEnter your FissionLab token.")
            tok_in  = gr.Textbox(label="Token", placeholder="FLAB-XXXX-XXXX-XXXX")
            tok_btn = gr.Button("Verify", variant="primary")
            tok_out = gr.Markdown("")
            gr.Markdown("No token? Contact **Dr_PrestonD@proton.me**")
            tok_btn.click(lambda t: "✅ Verified!" if verify_token(t) else "❌ Invalid token.",
                          [tok_in], [tok_out])

    gr.HTML('<div style="text-align:center;color:rgba(201,168,76,0.4);font-size:0.75rem;'
            'padding:14px 0;border-top:1px solid rgba(201,168,76,0.1);margin-top:8px">'
            'Dr. Preston · PhD · FissionLab · SP211/SP212 USNA Validation Prep · Purcell E&M</div>')

    _cols = [diag_state, intro_col, page1_col, page2_col, results_col]

    def on_start(_):
        return ({"page":1,"answers":{}},
                gr.update(visible=False), gr.update(visible=True),
                gr.update(visible=False), gr.update(visible=False))

    def on_next(s, *vals):
        ans = {i: v for i, v in enumerate(vals) if v is not None}
        return ({"page":2,"answers":ans},
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=True), gr.update(visible=False))

    def on_submit(s, *vals):
        answers = dict(s.get("answers", {}))
        for i, v in enumerate(vals):
            if v is not None: answers[i+10] = v
        htm, chart, m_sc, e_sc = build_results(answers)
        imgs = []
        for area in (["SP211"] if m_sc < e_sc else ["SP212"]):
            fn = CONCEPT_PLOTS.get(area)
            try: imgs.append(fn() if fn else None)
            except Exception: imgs.append(None)
        imgs.append(None)
        lines = [f"### Pathway — {DAYS_LEFT} days to June 21\n",
                 "> SP211 must be validated before SP212\n"]
        for lb, sc in [("SP211 Mechanics",m_sc),("SP212 E&M",e_sc)]:
            bar = "█"*int(sc*10)+"░"*(10-int(sc*10))
            flag = "✅" if sc>=0.7 else ("⚠️" if sc>=0.4 else "🔴")
            lines.append(f"- **{lb}:** {bar} {sc*100:.0f}% {flag}")
        return ({"page":3,"answers":answers},
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=True),
                gr.update(value=htm),
                gr.update(visible=chart is not None, value=chart),
                gr.update(visible=imgs[0] is not None, value=imgs[0]),
                gr.update(visible=False, value=None),
                gr.update(value="\n".join(lines)))

    def on_restart(_):
        return ({"page":0,"answers":{}},
                gr.update(visible=True), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=False))

    start_btn.click(on_start, [diag_state], _cols)
    next_btn.click(on_next, [diag_state] + radios_p1, _cols)
    submit_btn.click(on_submit, [diag_state] + radios_p2,
                     _cols + [results_html, results_chart] + cimgs + [pathway_md])
    restart_btn.click(on_restart, [diag_state], _cols)

if __name__ == "__main__":
    demo.launch()
