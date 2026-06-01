"""
FissionLab Physics Practice App v2.0 — Dr. Preston PhD
SP211 Calculus-Based Mechanics + SP212 Electromagnetism
USNA Validation Prep — Plebe Summer
"""
import io, json, random, re
from datetime import date
import requests
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
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

# ── Topic Map ────────────────────────────────────────────────────────────────
TOPICS = {
    "SP211 — Kinematics":           {"exam":"SP211", "area":"mechanics"},
    "SP211 — Newton's Laws":        {"exam":"SP211", "area":"mechanics"},
    "SP211 — Work & Energy":        {"exam":"SP211", "area":"mechanics"},
    "SP211 — Momentum & Collisions":{"exam":"SP211", "area":"mechanics"},
    "SP211 — Rotational Dynamics":  {"exam":"SP211", "area":"mechanics"},
    "SP211 — Simple Harmonic Motion":{"exam":"SP211","area":"mechanics"},
    "SP211 — Gravitation":          {"exam":"SP211", "area":"mechanics"},
    "SP212 — Electric Force & Field":{"exam":"SP212","area":"em"},
    "SP212 — Electric Potential":   {"exam":"SP212", "area":"em"},
    "SP212 — Capacitance & Circuits":{"exam":"SP212","area":"em"},
    "SP212 — Magnetism":            {"exam":"SP212", "area":"em"},
    "SP212 — Faraday & Induction":  {"exam":"SP212", "area":"em"},
}

EXPLANATIONS = {
    "SP211 — Kinematics": """
**Kinematics — Describing Motion**

**1D constant acceleration (the 4 equations):**
- v = v₀ + at
- x = x₀ + v₀t + ½at²
- v² = v₀² + 2a(x − x₀)
- x = x₀ + ½(v₀ + v)t

**Calculus link:** v = dx/dt, a = dv/dt. For non-constant a: integrate.

**2D Projectile** (a_x=0, a_y=−g):
- x(t) = x₀ + v₀cosθ · t
- y(t) = y₀ + v₀sinθ · t − ½gt²
- Range (level): R = v₀²sin(2θ)/g, maximized at θ=45°
- Max height: H = v₀²sin²θ/(2g)

**Circular motion:** centripetal acceleration a_c = v²/r = ω²r (toward center).

**Trap:** In projectile motion, horizontal and vertical motions are independent.
""",
    "SP211 — Newton's Laws": """
**Newton's Laws**

**1st:** ΣF = 0 ↔ constant velocity (or rest).
**2nd:** ΣF = ma — apply component by component to each object.
**3rd:** F₁₂ = −F₂₁ — action-reaction pairs act on DIFFERENT objects.

**Step-by-step FBD method:**
1. Draw free-body diagram for each object separately
2. Choose positive direction (usually up or direction of motion)
3. Write ΣF = ma for each direction
4. Solve the system

**Common forces:**
- Weight: W = mg (down)
- Normal: perpendicular to surface
- Friction: f_k = μ_k N (kinetic), f_s ≤ μ_s N (static)
- On incline: N = mg cosθ, component along incline = mg sinθ
- Spring: F = −kx (Hooke's Law)

**Trap:** Normal force is NOT always mg. Trap: action-reaction pairs never add up within one object's FBD.
""",
    "SP211 — Work & Energy": """
**Work, Energy, and Power**

**Work:** W = F·d·cosθ (dot product). For variable force: W = ∫F(x) dx.
**Kinetic energy:** K = ½mv²
**Work-energy theorem:** W_net = ΔK = K_f − K_i

**Potential energy:**
- Gravitational: U_g = mgh (ref. at h=0)
- Spring: U_s = ½kx²

**Conservation of energy** (no non-conservative forces):
K_i + U_i = K_f + U_f

**With friction/applied force:**
W_nc = ΔE = ΔK + ΔU

**Power:** P = dW/dt = F·v·cosθ (Watts)

**Trap:** Conservation of energy ONLY holds when no non-conservative forces (friction, applied) do work. If friction is present, use W_nc = ΔE.
""",
    "SP211 — Momentum & Collisions": """
**Momentum and Collisions**

**Momentum:** p = mv (vector)
**Impulse-momentum:** J = Δp = F_avg · Δt
**Conservation of momentum:** if ΣF_ext = 0, then Σp = constant.

**Elastic collision:** both momentum AND kinetic energy conserved.
- Equal masses: velocities exchange.
- General 1D: v₁' = (m₁−m₂)v₁/(m₁+m₂), v₂' = 2m₁v₁/(m₁+m₂)

**Perfectly inelastic:** objects stick together.
(m₁+m₂)v_f = m₁v₁ + m₂v₂

**Center of mass:** r_cm = Σmᵢrᵢ/M; v_cm = Σmᵢvᵢ/M

**Trap:** Momentum is a vector — include direction. Elastic collisions are rare (billiards, molecular); most real collisions are inelastic.
""",
    "SP211 — Rotational Dynamics": """
**Rotational Dynamics**

**Analogies to linear motion:**

| Linear | Rotational |
|--------|-----------|
| F = ma | τ = Iα |
| p = mv | L = Iω |
| KE = ½mv² | KE = ½Iω² |

**Moment of inertia:**
- Solid disk/cylinder: I = ½MR²
- Hollow cylinder: I = MR²
- Solid sphere: I = 2/5 MR²
- Rod (center): I = ML²/12; Rod (end): I = ML²/3
- **Parallel axis:** I = I_cm + Md²

**Torque:** τ = r × F = rF sinθ
**Angular momentum:** L = Iω; τ_net = dL/dt
**Conservation of L:** if τ_net = 0, L = Iω = constant. (Ice skater pulling arms in: I↓ → ω↑)

**Rolling without slipping:** v_cm = ωR; Total KE = ½mv_cm² + ½Iω²
""",
    "SP211 — Simple Harmonic Motion": """
**Simple Harmonic Motion (SHM)**

**Condition:** Linear restoring force F = −kx.
**Solution:** x(t) = A cos(ωt + φ)
- ω = angular frequency (rad/s)
- A = amplitude (max displacement)
- T = 2π/ω = period

**Velocity and acceleration:**
v(t) = −Aω sin(ωt+φ); v_max = Aω
a(t) = −Aω² cos(ωt+φ) = −ω²x

**Mass-spring:** ω = √(k/m); T = 2π√(m/k)
**Simple pendulum (small angle):** ω = √(g/L); T = 2π√(L/g)

**Energy:** E = ½kA² = ½mv_max² = K+U (constant)
At position x: K = ½mω²(A²−x²), U = ½kx²

**Speed at position x:** v = ω√(A²−x²)

**Key facts:** Period does NOT depend on amplitude (for ideal SHM). Pendulum period depends on L and g, not mass.
""",
    "SP211 — Gravitation": """
**Gravitation**

**Newton's law:** F = Gm₁m₂/r²   (G = 6.674×10⁻¹¹ N·m²/kg²)

**Gravitational PE:** U = −Gm₁m₂/r (zero at r=∞)

**Circular orbit** (gravity = centripetal):
Gm₁m₂/r² = m₂v²/r  →  v = √(Gm₁/r)

**Escape velocity:** v_esc = √(2GM/R) (set KE = |U|)

**Kepler's laws:**
1. Elliptical orbits, sun at one focus.
2. Equal areas swept in equal times (conservation of angular momentum).
3. T² = 4π²a³/(GM) (a = semi-major axis)
""",
    "SP212 — Electric Force & Field": """
**Electric Force and Field** *(SP212 — requires SP211 validated first)*

**Coulomb's law:** F = k|q₁||q₂|/r²
k = 9×10⁹ N·m²/C², ε₀ = 8.85×10⁻¹² C²/(N·m²)

**Electric field:** E = kq/r² (point charge); **F = qE** (force on test charge)
For multiple charges: superposition (vector sum).

**Gauss's law:** ∮ E·dA = Q_enc/ε₀
Use for symmetric charge distributions:
- Outside sphere: E = kQ/r²
- Inside uniform sphere: E = kQr/R³
- Infinite line (λ): E = λ/(2πε₀r)
- Infinite plane (σ): E = σ/(2ε₀)

**Field lines:** start at +, end at −; closer = stronger; never cross.
""",
    "SP212 — Electric Potential": """
**Electric Potential**

**Potential V** (scalar, J/C):  V = kq/r  (point charge)

**Field-potential relation:** E = −dV/dx (1D);  E = −∇V (3D)
Fields point from high V to low V.

**Work:** W = q(V_A − V_B) = −ΔU

**Equipotential surfaces:** ⊥ to electric field lines.

**Multiple charges:** V = Σ kqᵢ/rᵢ (scalar sum — easier than vector sum for E).

**Conductors in equilibrium:** E=0 inside; surface is equipotential; charge on surface.
""",
    "SP212 — Capacitance & Circuits": """
**Capacitance and DC Circuits**

**Capacitor:** C = Q/V (Farads). Parallel plate: C = ε₀A/d. With dielectric κ: C = κε₀A/d.
Energy stored: U = ½CV² = Q²/(2C).
**Series:** 1/C_eq = ΣΆ1/Cᵢ (same Q). **Parallel:** C_eq = ΣCᵢ (same V).

**Ohm's law:** V = IR. Resistivity: R = ρL/A.
Power dissipated: P = IV = I²R = V²/R.
**Series R:** R_eq = ΣRᵢ. **Parallel:** 1/R_eq = Σ1/Rᵢ.

**Kirchhoff's laws:**
- KVL: ΣV around any loop = 0
- KCL: ΣI into node = ΣI out

**RC circuits:** τ = RC. Charging: q(t) = Cε(1−e^{−t/τ}). At t=τ: 63% charged.

**Trap:** Series capacitors → 1/C formula (like parallel resistors). Parallel capacitors → add directly.
""",
    "SP212 — Magnetism": """
**Magnetic Fields**

**Force on charge:** F = qv×B; |F| = qvB sinθ
**Force on wire:** F = IL×B; |F| = BIL sinθ
**Magnetic force does NO work** (always ⊥ velocity).
**Circular orbit radius:** r = mv/(qB)

**Biot-Savart:** dB = (μ₀/4π)(I dL × r̂)/r²
**Ampere's law:** ∮ B·dL = μ₀I_enc
- Infinite wire: B = μ₀I/(2πr)
- Solenoid: B = μ₀nI (inside only; n = turns/length)

μ₀ = 4π×10⁻⁷ T·m/A

**Trap:** Magnetic force does no work (B ⊥ v always). No work → no ΔKE from B alone.
""",
    "SP212 — Faraday & Induction": """
**Faraday's Law and Electromagnetic Induction**

**Magnetic flux:** Φ_B = ∫∫ B·dA = BA cosθ (uniform B)

**Faraday's law:** ε = −dΦ_B/dt
Induced EMF = negative rate of change of flux.

**Lenz's law:** Induced current direction opposes the change in flux (determines direction of ε).

**Motional EMF:** ε = BLv (conductor length L moving at speed v perpendicular to B)

**Inductance:** L = NΦ_B/I. Solenoid: L = μ₀n²V = μ₀N²A/ℓ (Henry).
**RL circuits:** τ = L/R. I(t) = (ε/R)(1−e^{−t/τ}).

**Maxwell's 4 equations summarized:**
1. Gauss (E): ∮E·dA = Q_enc/ε₀
2. Gauss (B): ∮B·dA = 0 (no magnetic monopoles)
3. Faraday: ∮E·dL = −dΦ_B/dt
4. Ampere-Maxwell: ∮B·dL = μ₀(I + ε₀dΦ_E/dt)
""",
}

# ── Diagnostic Questions ──────────────────────────────────────────────────────
DIAGNOSTIC = [
    # SP211 Mechanics
    {"q":"A car starts from rest and accelerates at 4 m/s². Distance after 5 s?",
     "choices":["A) 20 m","B) 50 m","C) 100 m","D) 40 m"],"answer":1,
     "topic":"SP211 — Kinematics","explanation":"x = ½at² = ½(4)(25) = **50 m**."},
    {"q":"A projectile launched at 45° with v₀=20 m/s. Range? (g=10 m/s²)",
     "choices":["A) 20 m","B) 40 m","C) 28 m","D) 10 m"],"answer":1,
     "topic":"SP211 — Kinematics","explanation":"R = v₀²sin(90°)/g = 400/10 = **40 m**."},
    {"q":"A 5 kg block on a frictionless incline (30°). Acceleration down the slope?",
     "choices":["A) 5 m/s²","B) 9.8 m/s²","C) 4.9 m/s²","D) 2.45 m/s²"],"answer":2,
     "topic":"SP211 — Newton's Laws","explanation":"a = g sin30° = 9.8×0.5 = **4.9 m/s²**."},
    {"q":"A 0.5 kg ball on a 1.2 m string moves at 3 m/s in a circle. Centripetal force?",
     "choices":["A) 1.25 N","B) 3.75 N","C) 7.5 N","D) 0.9 N"],"answer":1,
     "topic":"SP211 — Newton's Laws","explanation":"F_c = mv²/r = 0.5(9)/1.2 = **3.75 N**."},
    {"q":"A 2 kg block released from h=5 m (frictionless). Speed at bottom?",
     "choices":["A) 7 m/s","B) 10 m/s","C) 5 m/s","D) √98 ≈ 9.9 m/s"],"answer":3,
     "topic":"SP211 — Work & Energy","explanation":"mgh=½mv² → v=√(2gh)=√(2·9.8·5)=√98≈**9.9 m/s**."},
    {"q":"Two carts: A (2 kg, 4 m/s) + B (3 kg, rest) stick together. Final speed?",
     "choices":["A) 4 m/s","B) 2.4 m/s","C) 1.6 m/s","D) 3 m/s"],"answer":2,
     "topic":"SP211 — Momentum & Collisions","explanation":"2(4)+0=(2+3)v_f → v_f=8/5=**1.6 m/s**."},
    {"q":"A solid disk (M=4kg, R=0.3m) spins up from 0 to 4π rad/s in 5s. α?",
     "choices":["A) π rad/s²","B) 4π/5 rad/s²","C) 2π rad/s²","D) 0.8 rad/s²"],"answer":1,
     "topic":"SP211 — Rotational Dynamics","explanation":"α=(ω_f−ω_i)/t=4π/5=**0.8π rad/s²**."},
    {"q":"A mass-spring system (k=100 N/m, m=0.25 kg). Period T?",
     "choices":["A) π/5 s","B) π/10 s","C) 0.314 s","D) Both A and C"],"answer":3,
     "topic":"SP211 — Simple Harmonic Motion","explanation":"T=2π√(m/k)=2π√(0.0025)=2π/20=π/10≈0.314s. Both A and C are the same number. **Both A and C**."},
    {"q":"The Moon orbits Earth at r=3.84×10⁸m. Its centripetal acceleration ≈",
     "choices":["A) 9.8 m/s²","B) 0.027 m/s²","C) 0.0027 m/s²","D) 0.27 m/s²"],"answer":2,
     "topic":"SP211 — Gravitation","explanation":"g_moon surface = g_Earth/3600 ≈ 9.8/3600 ≈ **0.0027 m/s²** (distance 60 Earth radii away)."},
    # SP212 E&M
    {"q":"Two charges +3μC and +5μC separated by 0.2m. Force? (k=9×10⁹)",
     "choices":["A) 3.375 N","B) 0.3375 N","C) 33.75 N","D) 0.034 N"],"answer":0,
     "topic":"SP212 — Electric Force & Field","explanation":"F=k(3×5)×10⁻¹²/0.04=9×10⁹×15×10⁻¹²/0.04=**3.375 N**."},
    {"q":"Parallel plates A=0.02m², d=1mm, ε₀=8.85×10⁻¹². Capacitance?",
     "choices":["A) 177 pF","B) 17.7 nF","C) 1.77 μF","D) 0.177 pF"],"answer":0,
     "topic":"SP212 — Capacitance & Circuits","explanation":"C=ε₀A/d=8.85×10⁻¹²(0.02)/0.001=**177 pF**."},
    {"q":"A circuit: 9V battery, R₁=3Ω in series with R₂=6Ω parallel R₃=12Ω. Total current?",
     "choices":["A) 3 A","B) 1.5 A","C) 9/7 A ≈ 1.29 A","D) 2 A"],"answer":2,
     "topic":"SP212 — Capacitance & Circuits","explanation":"R₂‖R₃=4Ω. R_eq=7Ω. I=9/7≈**1.29 A**."},
    {"q":"A proton (q=1.6×10⁻¹⁹C) moves at 3×10⁶ m/s ⊥ to B=0.2T. Force?",
     "choices":["A) 9.6×10⁻¹⁴ N","B) 9.6×10⁻¹³ N","C) 3.2×10⁻¹⁴ N","D) 4.8×10⁻¹⁴ N"],"answer":0,
     "topic":"SP212 — Magnetism","explanation":"F=qvB=1.6×10⁻¹⁹·3×10⁶·0.2=**9.6×10⁻¹⁴ N**."},
    {"q":"A loop (r=0.1m) in B=2T. Field drops to 0 in 0.5s. Induced EMF?",
     "choices":["A) 0.063 V","B) 0.126 V","C) 0.314 V","D) 1.26 V"],"answer":1,
     "topic":"SP212 — Faraday & Induction","explanation":"Φ=Bπr²=2π(0.01)=0.063 Wb. ε=ΔΦ/Δt=0.063/0.5=**0.126 V**."},
]

# ── Practice Questions ────────────────────────────────────────────────────────
PRACTICE = {
    "SP211 — Kinematics": [
        {"q":"Ball thrown up at 20m/s from h=10m. Max height above ground? (g=10)",
         "choices":["A) 20m","B) 30m","C) 25m","D) 40m"],"answer":1,
         "sol":"Δh=v₀²/(2g)=20m. Max height=10+20=**30m**."},
        {"q":"Projectile at 30°, v₀=40m/s, g=10. Time of flight?",
         "choices":["A) 2s","B) 3s","C) 4s","D) 6s"],"answer":2,
         "sol":"T=2v₀sinθ/g=2(40)(0.5)/10=**4s**."},
    ],
    "SP211 — Newton's Laws": [
        {"q":"m₁=3kg, m₂=5kg Atwood machine. Acceleration?",
         "choices":["A) 2.5 m/s²","B) 1.25 m/s²","C) 5 m/s²","D) 9.8 m/s²"],"answer":0,
         "sol":"a=(m₂−m₁)g/(m₁+m₂)=(2)(9.8)/8≈**2.45 m/s²** ≈ 2.5."},
        {"q":"Block 4kg, μ_k=0.3, F=25N horizontal. Acceleration? (g=10)",
         "choices":["A) 6.25 m/s²","B) 3.25 m/s²","C) 4 m/s²","D) 2.75 m/s²"],"answer":1,
         "sol":"f_k=μ_k mg=12N. F_net=13N. a=13/4=**3.25 m/s²**."},
    ],
    "SP211 — Work & Energy": [
        {"q":"Spring k=200N/m compressed 0.15m. Speed of 0.5kg mass released (frictionless)?",
         "choices":["A) 3 m/s","B) 2 m/s","C) 6 m/s","D) 1.5 m/s"],"answer":0,
         "sol":"½kx²=½mv² → v=x√(k/m)=0.15√400=**3 m/s**."},
        {"q":"3kg mass released at h=4m. Speed at bottom is 7m/s. Energy lost to friction?",
         "choices":["A) 46.5J","B) 20J","C) 73.5J","D) 0J"],"answer":0,
         "sol":"E_i=mgh=117.6J≈120J. E_f=½mv²=73.5J. Lost=**46.5J**."},
    ],
    "SP211 — Rotational Dynamics": [
        {"q":"Solid sphere M=2kg R=0.1m rolls from rest on 30° incline L=2m. Speed at bottom?",
         "choices":["A) 3.78 m/s","B) 4.43 m/s","C) 2 m/s","D) 3.13 m/s"],"answer":0,
         "sol":"E: Mgh=7Mv²/10 (sphere rolling). v=√(10gh/7)=√(10·10·1/7)≈**3.78 m/s**."},
    ],
    "SP211 — Simple Harmonic Motion": [
        {"q":"m=0.4kg spring k=90N/m. If released from x=0.2m, max speed?",
         "choices":["A) 3 m/s","B) 6 m/s","C) 1.5 m/s","D) 4.5 m/s"],"answer":0,
         "sol":"v_max=Aω=0.2√(90/0.4)=0.2·15=**3 m/s**."},
    ],
    "SP212 — Electric Force & Field": [
        {"q":"E = 1000N/C pointing right. Force on electron (q=−1.6×10⁻¹⁹C)?",
         "choices":["A) 1.6×10⁻¹⁶N left","B) 1.6×10⁻¹⁶N right","C) 1.6×10⁻¹³N left","D) 0N"],"answer":0,
         "sol":"F=qE=−1.6×10⁻¹⁹×1000=−1.6×10⁻¹⁶N → **1.6×10⁻¹⁶N to the left**."},
    ],
    "SP212 — Capacitance & Circuits": [
        {"q":"C=50μF charged to 100V. Energy stored?",
         "choices":["A) 0.25J","B) 5J","C) 0.5J","D) 2.5J"],"answer":0,
         "sol":"U=½CV²=½(50×10⁻⁶)(10000)=**0.25J**."},
        {"q":"RC circuit: R=10kΩ, C=100μF. Time constant τ?",
         "choices":["A) 0.1s","B) 1s","C) 10s","D) 0.01s"],"answer":1,
         "sol":"τ=RC=10⁴×10⁻⁴=**1s**."},
    ],
    "SP212 — Magnetism": [
        {"q":"Wire L=0.5m, I=3A, ⊥ to B=0.4T. Force on wire?",
         "choices":["A) 0.6N","B) 6N","C) 0.06N","D) 1.2N"],"answer":0,
         "sol":"F=BIL=0.4×3×0.5=**0.6N**."},
    ],
    "SP212 — Faraday & Induction": [
        {"q":"Rectangular loop (0.2×0.3m) enters B=0.8T at v=0.5m/s. Induced EMF?",
         "choices":["A) 0.08V","B) 0.24V","C) 0.16V","D) 0.04V"],"answer":0,
         "sol":"ε=BLv=0.8×0.2×0.5=**0.08V**."},
    ],
}

# ── Visualization Functions ───────────────────────────────────────────────────
DARK = {"figure.facecolor":"#0b1a2e","axes.facecolor":"#112240","axes.edgecolor":"#8fa8c8",
        "axes.labelcolor":"#e8eaf0","xtick.color":"#8fa8c8","ytick.color":"#8fa8c8",
        "text.color":"#e8eaf0","grid.color":"#1e3a5f","grid.alpha":0.4}

def _fig(w=7, h=4):
    for k,v in DARK.items(): plt.rcParams[k]=v
    fig, ax = plt.subplots(figsize=(w,h))
    fig.patch.set_facecolor("#0b1a2e"); ax.set_facecolor("#112240"); ax.grid(True)
    return fig, ax

def _save(fig):
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig); buf.seek(0); return buf

def plot_projectile(v0=20, angle_deg=45, g=9.8):
    fig, ax = _fig()
    θ = np.radians(angle_deg)
    T = 2*v0*np.sin(θ)/g
    t = np.linspace(0, T, 400)
    x = v0*np.cos(θ)*t; y = v0*np.sin(θ)*t - 0.5*g*t**2
    ax.plot(x, y, color="#f4c542", lw=2.5, label=f"v₀={v0}m/s, θ={angle_deg}°")
    ax.fill_between(x, 0, y, alpha=0.1, color="#f4c542")
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    ax.set_title("Projectile Motion", color="#f4c542", fontsize=11)
    ax.axhline(0, color="#8fa8c8", lw=0.8); ax.legend(fontsize=9)
    return _save(fig)

def plot_shm(A=1.0, omega=2.0):
    fig, ax = _fig()
    t = np.linspace(0, 3*np.pi/omega, 500)
    x = A*np.cos(omega*t); v = -A*omega*np.sin(omega*t)
    ax.plot(t, x, color="#f4c542", lw=2, label="x(t) = A cos(ωt)")
    ax.plot(t, v/omega, color="#4fc3f7", lw=2, ls="--", label="v(t)/ω")
    ax.set_xlabel("t (s)"); ax.set_ylabel("x (m)")
    ax.set_title("Simple Harmonic Motion", color="#f4c542", fontsize=11)
    ax.legend(fontsize=9)
    return _save(fig)

def plot_electric_field():
    fig, ax = _fig(7,6)
    y, x = np.mgrid[-2:2:20j, -2:2:20j]
    # dipole: +q at (-0.5,0), -q at (0.5,0)
    r1 = np.sqrt((x+0.5)**2+y**2)+1e-6
    r2 = np.sqrt((x-0.5)**2+y**2)+1e-6
    Ex = (x+0.5)/r1**3 - (x-0.5)/r2**3
    Ey = y/r1**3 - y/r2**3
    mag = np.sqrt(Ex**2+Ey**2)+1e-6
    ax.streamplot(x,y,Ex,Ey,color=np.log(mag),cmap="YlOrBr",linewidth=1.2,density=1.2,arrowsize=1.2)
    ax.plot([-0.5],[0],'o',color="#4fc3f7",ms=12,label="+q"); ax.plot([0.5],[0],'o',color="#f06292",ms=12,label="−q")
    ax.set_title("Electric Field of a Dipole", color="#f4c542", fontsize=11)
    ax.legend(fontsize=9); ax.set_aspect("equal")
    return _save(fig)

def plot_rc_circuit():
    fig, ax = _fig()
    tau_vals = [1.0, 2.0, 0.5]
    t = np.linspace(0, 6, 400)
    colors = ["#f4c542","#4fc3f7","#81c784"]
    for tau, c in zip(tau_vals, colors):
        q = 1 - np.exp(-t/tau)
        ax.plot(t, q, color=c, lw=2, label=f"τ = {tau}s")
    ax.axhline(0.632, color="#8fa8c8", ls=":", lw=1, label="63.2% at t=τ")
    ax.set_xlabel("t (s)"); ax.set_ylabel("q/Q_max")
    ax.set_title("RC Circuit Charging  q(t) = Q(1−e^{−t/τ})", color="#f4c542", fontsize=11)
    ax.legend(fontsize=9)
    return _save(fig)

def plot_diagnostic_results(scores: dict):
    cats = list(scores.keys()); vals = list(scores.values())
    fig, ax = _fig(7,3)
    bars = ax.barh(cats, vals, color=["#f4c542" if v>=0.6 else "#f06292" for v in vals], height=0.6)
    ax.set_xlim(0,1); ax.set_xlabel("Score")
    ax.set_title("Diagnostic Results", color="#f4c542", fontsize=11)
    for bar, val in zip(bars, vals):
        ax.text(val+0.02, bar.get_y()+bar.get_height()/2, f"{val*100:.0f}%", va="center", color="#e8eaf0", fontsize=9)
    return _save(fig)

PLOT_MAP = {
    "SP211 — Kinematics": ("projectile",),
    "SP211 — Newton's Laws": None,
    "SP211 — Work & Energy": None,
    "SP211 — Momentum & Collisions": None,
    "SP211 — Rotational Dynamics": None,
    "SP211 — Simple Harmonic Motion": ("shm",),
    "SP211 — Gravitation": None,
    "SP212 — Electric Force & Field": ("efield",),
    "SP212 — Electric Potential": ("efield",),
    "SP212 — Capacitance & Circuits": ("rc",),
    "SP212 — Magnetism": None,
    "SP212 — Faraday & Induction": None,
}

def get_plot(topic):
    from PIL import Image as PILImage
    spec = PLOT_MAP.get(topic)
    if spec is None: return None
    if spec[0]=="projectile": buf = plot_projectile()
    elif spec[0]=="shm": buf = plot_shm()
    elif spec[0]=="efield": buf = plot_electric_field()
    elif spec[0]=="rc": buf = plot_rc_circuit()
    else: return None
    return PILImage.open(buf)

DAYS_LEFT = max(0, (date(2026, 6, 21) - date.today()).days)

def generate_pathway(scores: dict) -> str:
    mech_scores = [s for t,s in scores.items() if "SP211" in t]
    em_scores   = [s for t,s in scores.items() if "SP212" in t]
    mech_avg = sum(mech_scores)/len(mech_scores) if mech_scores else 0
    em_avg   = sum(em_scores)/len(em_scores) if em_scores else 0

    md = f"## 📍 Your USNA Physics Pathway\n\n**{DAYS_LEFT} days until June 21.**\n\n"
    md += "### 📊 Area Performance\n"
    for label, avg in [("SP211 Mechanics", mech_avg), ("SP212 E&M", em_avg)]:
        bar = "█"*int(avg*10)+"░"*(10-int(avg*10))
        st  = "✅ Strong" if avg>=0.7 else ("⚠️ Review" if avg>=0.4 else "🔴 Focus Here")
        md += f"- **{label}:** {bar} {avg*100:.0f}%  {st}\n"
    md += "\n### 📅 Recommended Plan\n"
    md += "**SP211 must be validated before you can attempt SP212.**\n\n"
    if mech_avg < 0.6:
        md += "- 🔴 **SP211 needs work.** Spend most of Week 1–2 on mechanics:\n"
        md += "  Newton's laws + FBD drawings, energy conservation, momentum collisions, SHM.\n"
    else:
        md += "- ✅ SP211 looks solid. A timed practice test to confirm, then move to Calc III.\n"
    if em_avg < 0.6:
        md += "- ⚠️ **SP212 — prioritize after SP211.** Coulomb, Gauss, circuits, Faraday.\n"
    else:
        md += "- ✅ SP212 foundation looks good for review.\n"

    weak = [t for t,s in scores.items() if s < 0.5]
    if weak:
        md += "\n### ⚡ Topics Needing Immediate Attention\n"
        for t in weak: md += f"- {t}\n"
    md += "\n### 🗓️ Daily Routine\n"
    md += "- **20 min:** Concept review + cheat sheet\n- **30 min:** Practice problems\n- **10 min:** FBD practice (SP211)\n"
    return md

# ── CSS & App ─────────────────────────────────────────────────────────────────
CSS = """
.gradio-container{background:#0b1a2e!important;color:#e8eaf0!important;font-family:'Segoe UI',system-ui,sans-serif}
h1,h2,h3{color:#f4c542!important}
.gr-button-primary{background:#f4c542!important;color:#0b1a2e!important;font-weight:700!important;border:none!important}
.gr-button{border:1px solid #b89630!important;color:#f4c542!important;background:transparent!important}
.gr-box,.gr-form,.gr-panel{background:#112240!important;border-color:#1e3a5f!important}
label,p,span{color:#e8eaf0!important}
footer{display:none!important}
"""

def new_session():
    qs = DIAGNOSTIC[:]
    random.shuffle(qs)
    return {"verified":False,"diag_idx":0,"diag_scores":{},"diag_done":False,"qs":qs}

with gr.Blocks(css=CSS, title="FissionLab Physics — Dr. Preston PhD") as demo:
    state = gr.State(new_session())

    gr.Markdown("# ⚛️ FissionLab Physics Practice — Dr. Preston PhD")
    gr.Markdown("*SP211 Calculus-Based Mechanics + SP212 E&M · USNA Plebe Summer Validation Prep*")

    with gr.Tabs():
        # ── TAB 1: DIAGNOSTIC ────────────────────────────────────────────────
        with gr.Tab("🎯 Diagnostic"):
            gr.Markdown("### 14-question diagnostic → personalized SP211/SP212 pathway.")
            diag_q    = gr.Markdown("*Click Start to begin.*")
            diag_radio= gr.Radio(choices=[], label="Select your answer:", interactive=True, visible=False)
            diag_info = gr.Markdown("")
            with gr.Row():
                diag_start  = gr.Button("▶ Start Diagnostic", variant="primary")
                diag_submit = gr.Button("Submit Answer", visible=False)
                diag_next   = gr.Button("Next →", visible=False)
            diag_progress = gr.Markdown("")
            diag_result   = gr.Markdown("")
            diag_chart    = gr.Image(label="Performance Chart", visible=False, type="pil")
            diag_pathway  = gr.Markdown("")

            def start_diag(s):
                s = new_session(); s["diag_idx"]=0
                q = s["qs"][0]
                return (s,
                        gr.update(value=f"**Q1/{len(DIAGNOSTIC)}**\n\n{q['q']}"),
                        gr.update(choices=q["choices"],value=None,interactive=True,visible=True),
                        gr.update(value=""),
                        gr.update(visible=False),gr.update(visible=True),gr.update(visible=False),
                        gr.update(value="*Progress: 0/{} complete*".format(len(DIAGNOSTIC))),
                        gr.update(value=""),gr.update(visible=False),gr.update(value=""))

            def submit_diag(choice, s):
                if choice is None:
                    return s, gr.update(), gr.update(value="⚠️ Select an answer."), gr.update(visible=False)
                q = s["qs"][s["diag_idx"]]
                correct = (choice == q["choices"][q["answer"]])
                s["diag_scores"][q["topic"]] = s["diag_scores"].get(q["topic"],0)+(1 if correct else 0)
                icon = "✅ Correct!" if correct else f"❌ Incorrect. Correct: **{q['choices'][q['answer']]}**"
                return (s, gr.update(interactive=False),
                        gr.update(value=f"{icon}\n\n{q['explanation']}"),
                        gr.update(visible=True, value="Next →" if s["diag_idx"]<len(DIAGNOSTIC)-1 else "See Results →"))

            def next_diag(s):
                s["diag_idx"]+=1
                prog = f"*Progress: {s['diag_idx']}/{len(DIAGNOSTIC)} complete*"
                if s["diag_idx"]>=len(DIAGNOSTIC):
                    topic_counts = {}
                    for q in s["qs"]: topic_counts[q["topic"]]=topic_counts.get(q["topic"],0)+1
                    scores = {t: s["diag_scores"].get(t,0)/cnt for t,cnt in topic_counts.items()}
                    pathway = generate_pathway(scores)
                    area_avg = {"SP211 Mechanics": 0, "SP212 E&M": 0}
                    mc=[v for t,v in scores.items() if "SP211" in t]; em=[v for t,v in scores.items() if "SP212" in t]
                    if mc: area_avg["SP211 Mechanics"]=sum(mc)/len(mc)
                    if em: area_avg["SP212 E&M"]=sum(em)/len(em)
                    from PIL import Image as PILImage
                    buf = plot_diagnostic_results(area_avg)
                    img = PILImage.open(buf)
                    return (s, gr.update(value="## 🎉 Diagnostic Complete!"),
                            gr.update(visible=False), gr.update(value=""),
                            gr.update(visible=False),gr.update(visible=False),gr.update(visible=False),
                            gr.update(value=prog), gr.update(value=pathway),
                            gr.update(visible=True,value=img), gr.update(value=""))
                q=s["qs"][s["diag_idx"]]
                n=s["diag_idx"]+1
                return (s,gr.update(value=f"**Q{n}/{len(DIAGNOSTIC)}**\n\n{q['q']}"),
                        gr.update(choices=q["choices"],value=None,interactive=True,visible=True),
                        gr.update(value=""),
                        gr.update(visible=False),gr.update(visible=True),gr.update(visible=False),
                        gr.update(value=prog),gr.update(value=""),gr.update(visible=False),gr.update(value=""))

            diag_start.click(start_diag,[state],[state,diag_q,diag_radio,diag_info,diag_start,diag_submit,diag_next,diag_progress,diag_pathway,diag_chart,diag_result])
            diag_submit.click(submit_diag,[diag_radio,state],[state,diag_radio,diag_info,diag_next])
            diag_next.click(next_diag,[state],[state,diag_q,diag_radio,diag_info,diag_start,diag_submit,diag_next,diag_progress,diag_pathway,diag_chart,diag_result])

        # ── TAB 2: TOPIC GUIDE ───────────────────────────────────────────────
        with gr.Tab("📚 Topic Guide"):
            gr.Markdown("### Concept reviews with visualizations for SP211 and SP212.")
            topic_dd  = gr.Dropdown(choices=list(TOPICS.keys()), label="Select Topic", value=list(TOPICS.keys())[0])
            topic_exp = gr.Markdown("")
            topic_img = gr.Image(label="Visualization", visible=False, type="pil")

            def load_topic(topic):
                exp = EXPLANATIONS.get(topic,"*No explanation available.*")
                img = get_plot(topic)
                if img: return gr.update(value=exp), gr.update(visible=True, value=img)
                return gr.update(value=exp), gr.update(visible=False)

            topic_dd.change(load_topic,[topic_dd],[topic_exp,topic_img])
            demo.load(load_topic,[topic_dd],[topic_exp,topic_img])

        # ── TAB 3: PRACTICE ──────────────────────────────────────────────────
        with gr.Tab("🏋️ Practice"):
            gr.Markdown("### Graded problems with solutions.")
            prac_topics = [t for t in PRACTICE.keys()]
            prac_topic = gr.Dropdown(choices=prac_topics, label="Topic", value=prac_topics[0])
            prac_q     = gr.Markdown("")
            prac_radio = gr.Radio(choices=[], label="Your answer:", interactive=True, visible=False)
            prac_info  = gr.Markdown("")
            prac_score = gr.Markdown("")
            with gr.Row():
                prac_load   = gr.Button("Load Question", variant="primary")
                prac_submit = gr.Button("Submit", visible=False)
                prac_next   = gr.Button("Next →", visible=False)
            prac_state = gr.State({"topic":prac_topics[0],"idx":0,"score":0,"total":0})

            def load_prac(topic, ps):
                ps["topic"]=topic; ps["idx"]=0; ps["score"]=0; ps["total"]=0
                qs = PRACTICE.get(topic,[])
                if not qs: return ps,gr.update(value="*No problems for this topic yet.*"),gr.update(visible=False),gr.update(value=""),gr.update(value=""),gr.update(visible=False),gr.update(visible=False)
                q=qs[0]
                return (ps,gr.update(value=f"**Problem 1/{len(qs)}:** {q['q']}"),
                        gr.update(choices=q["choices"],value=None,interactive=True,visible=True),
                        gr.update(value=""),gr.update(value="Score: 0/0"),
                        gr.update(visible=True,value="Submit"),gr.update(visible=False))

            def submit_prac(choice, ps):
                if choice is None: return ps, gr.update(value="⚠️ Select an answer."), gr.update(visible=False)
                qs=PRACTICE.get(ps["topic"],[])
                if ps["idx"]>=len(qs): return ps,gr.update(value="Done."),gr.update(visible=False)
                q=qs[ps["idx"]]; correct=(choice==q["choices"][q["answer"]])
                if correct: ps["score"]+=1; ps["total"]+=1
                fb="✅ Correct!" if correct else f"❌ Incorrect. Correct: **{q['choices'][q['answer']]}**"
                return (ps, gr.update(value=f"{fb}\n\n**Solution:** {q['sol']}"),
                        gr.update(visible=True,value="Next →" if ps["idx"]<len(qs)-1 else "Done ✓"))

            def next_prac(ps):
                ps["idx"]+=1; qs=PRACTICE.get(ps["topic"],[])
                sc=f"Score: {ps['score']}/{ps['total']}"
                if ps["idx"]>=len(qs):
                    return ps,gr.update(value=f"**Done! {ps['score']}/{ps['total']}**"),gr.update(visible=False),gr.update(value=""),gr.update(value=sc),gr.update(visible=False),gr.update(visible=False)
                q=qs[ps["idx"]]
                return (ps,gr.update(value=f"**Problem {ps['idx']+1}/{len(qs)}:** {q['q']}"),
                        gr.update(choices=q["choices"],value=None,interactive=True,visible=True),
                        gr.update(value=""),gr.update(value=sc),
                        gr.update(visible=True,value="Submit"),gr.update(visible=False))

            prac_load.click(load_prac,[prac_topic,prac_state],[prac_state,prac_q,prac_radio,prac_info,prac_score,prac_submit,prac_next])
            prac_submit.click(submit_prac,[prac_radio,prac_state],[prac_state,prac_info,prac_next])
            prac_next.click(next_prac,[prac_state],[prac_state,prac_q,prac_radio,prac_info,prac_score,prac_submit,prac_next])

        # ── TAB 4: STUDY PLAN ────────────────────────────────────────────────
        with gr.Tab("📅 Study Plan"):
            gr.Markdown(f"### USNA Physics Prep — {DAYS_LEFT} days until June 21\n\n"
                "**Exam order:** SP211 first (required to sit SP212). Prioritize mechanics.\n\n"
                "**Week 1 (Jun 1–7) — SP211 Mechanics:**\n"
                "- Mon/Tue: Kinematics + Newton's Laws (lots of FBD practice)\n"
                "- Wed/Thu: Work-Energy theorem + Momentum + Collisions\n"
                "- Fri/Sat: Rotation (moments of inertia table) + SHM (mass-spring + pendulum)\n"
                "- Sun: Timed SP211 mock — 20 problems\n\n"
                "**Week 2 (Jun 8–14) — SP211 Review + Start SP212:**\n"
                "- Mon–Wed: SP211 weak areas from Week 1 mock\n"
                "- Thu/Fri: SP212 Coulomb, Gauss's law, electric potential\n"
                "- Sat: SP212 Capacitance, DC circuits (KVL/KCL, RC time constant)\n"
                "- Sun: Mock SP211 (final check)\n\n"
                "**Week 3 (Jun 15–21) — SP212 Focus:**\n"
                "- Mon/Tue: Magnetism — force on charge, Biot-Savart, Ampere's law\n"
                "- Wed/Thu: Faraday's law, Lenz's law, inductance, Maxwell's equations\n"
                "- Fri/Sat: Full SP212 practice exam + review wrong answers\n"
                "- Sun: Rest / light review\n\n"
                "*Use the Diagnostic tab to get your personalized version of this plan.*")

        # ── TAB 5: UNLOCK ────────────────────────────────────────────────────
        with gr.Tab("🔑 Unlock"):
            gr.Markdown("## Unlock Full Access\nEnter your FissionLab token (FLAB-XXXX-XXXX-XXXX).")
            tok_in  = gr.Textbox(label="Token", placeholder="FLAB-XXXX-XXXX-XXXX")
            tok_btn = gr.Button("Verify Token", variant="primary")
            tok_out = gr.Markdown("")
            gr.Markdown("Don't have a token? Contact **Dr_PrestonD@proton.me**")
            def verify_action(token, s):
                if verify_token(token):
                    s["verified"]=True
                    return s,"✅ **Premium unlocked!** Full access enabled."
                return s,"❌ Invalid token. Check format or contact Dr. Preston."
            tok_btn.click(verify_action,[tok_in,state],[state,tok_out])

    gr.Markdown("<div style='text-align:center;color:#8fa8c8;font-size:0.8rem;margin-top:20px'>Dr. Preston — PhD Nuclear Engineering · FissionLab · SP211/SP212 USNA Validation Prep</div>")

if __name__ == "__main__":
    demo.launch()
