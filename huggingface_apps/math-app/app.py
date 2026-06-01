"""
FissionLab Math Practice App v2.0 — Dr. Preston PhD
Calculus I / II / III — USNA Validation Prep
Aligned with Stewart Early Transcendentals (2015), Cengage
"""
import io, json, random, re, textwrap
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
FREE_LIMIT = 5

def verify_token(token: str) -> bool:
    t = token.strip().upper()
    if not PATTERN.match(t):
        return False
    try:
        r = requests.get(PORTAL, params={"token": t}, timeout=5)
        return r.status_code == 200 and r.json().get("valid", False)
    except Exception:
        return False

# ── Stewart Chapter Map ───────────────────────────────────────────────────────
TOPICS = {
    "Calc I — Limits & Continuity":        {"ch": "Ch 2",  "area": "calc1"},
    "Calc I — Derivatives & Rules":        {"ch": "Ch 3",  "area": "calc1"},
    "Calc I — Applications of Derivatives":{"ch": "Ch 4",  "area": "calc1"},
    "Calc I — Integrals & FTC":            {"ch": "Ch 5",  "area": "calc1"},
    "Calc II — Integration Techniques":    {"ch": "Ch 7",  "area": "calc2"},
    "Calc II — Series & Convergence":      {"ch": "Ch 11", "area": "calc2"},
    "Calc II — Power & Taylor Series":     {"ch": "Ch 11", "area": "calc2"},
    "Calc II — Parametric & Polar":        {"ch": "Ch 10", "area": "calc2"},
    "Calc III — Vectors & 3D Geometry":    {"ch": "Ch 12", "area": "calc3"},
    "Calc III — Partial Derivatives":      {"ch": "Ch 14", "area": "calc3"},
    "Calc III — Multiple Integrals":       {"ch": "Ch 15", "area": "calc3"},
    "Calc III — Vector Calculus Theorems": {"ch": "Ch 16", "area": "calc3"},
}

EXPLANATIONS = {
    "Calc I — Limits & Continuity": """
**Stewart Ch 2 — Limits and Continuity**

The limit lim(x→a) f(x) = L means f(x) → L as x → a (regardless of f(a)).

**Key techniques:**
- Direct substitution → try first
- Factor/cancel: (x²−4)/(x−2) = (x+2)(x−2)/(x−2) → x+2 as x→2
- L'Hôpital's Rule (0/0 or ∞/∞ only): lim f/g = lim f'/g'
- Squeeze theorem: g≤f≤h and lim g=lim h=L → lim f=L

**Critical limits (Stewart §2.2, 2.6):**
- lim(x→0) sin x/x = **1**
- lim(x→0) (1−cos x)/x = **0**
- lim(x→∞) (1+1/x)^x = **e**

**Continuity at a:** f(a) defined, lim exists, and they equal each other.

**Common trap:** L'Hôpital applies *only* to 0/0 or ±∞/±∞ — rewrite 0·∞ first.
""",
    "Calc I — Derivatives & Rules": """
**Stewart Ch 3 — Differentiation Rules**

f'(x) = lim(h→0) [f(x+h)−f(x)]/h

| Rule | Formula |
|------|---------|
| Power | d/dx[xⁿ] = nxⁿ⁻¹ |
| Product | (uv)' = u'v + uv' |
| Quotient | (u/v)' = (u'v − uv')/v² |
| Chain | d/dx[f(g(x))] = f'(g(x))·g'(x) |

**Trig:** (sin x)' = cos x, (cos x)' = −sin x, (tan x)' = sec²x
**Exp/Log:** (eˣ)' = eˣ, (ln x)' = 1/x
**Inverse trig:** (arctan x)' = 1/(1+x²), (arcsin x)' = 1/√(1−x²)
**Implicit:** differentiate both sides; treat y as a function of x.

**Stewart §3.4–3.6 — chain rule is the most tested rule. Never skip it.**
""",
    "Calc I — Applications of Derivatives": """
**Stewart Ch 4 — Applications of Differentiation**

**Critical points:** f'(x) = 0 or DNE. Use 2nd derivative test: f''>0 min, f''<0 max.
**Curve sketching:** sign charts for f' (inc/dec) and f'' (concavity). Inflection where f'' changes sign.
**Related rates:** relate quantities → differentiate both sides w.r.t. t → plug in known rates.
**Optimization (§4.7):**
1. Write objective as one-variable function
2. Find critical points
3. Verify with 2nd derivative test or closed interval check

**L'Hôpital (§4.4):** Indeterminate 0/0 or ∞/∞ → lim f/g = lim f'/g'.

**Stewart §4.7 box:** "Substitute specific values AFTER differentiating."
""",
    "Calc I — Integrals & FTC": """
**Stewart Ch 5 — Integrals**

**FTC Part 1:** d/dx ∫ₐˣ f(t) dt = f(x)
**FTC Part 2:** ∫ₐᵇ f dx = F(b)−F(a), where F'=f

**Key antiderivatives:**
∫xⁿ dx = xⁿ⁺¹/(n+1)+C, ∫1/x dx = ln|x|+C, ∫eˣ dx = eˣ+C
∫sin x dx = −cos x+C, ∫cos x dx = sin x+C, ∫sec²x dx = tan x+C

**u-Substitution:** reverse chain rule. Set u = g(x), du = g'(x)dx.

**Definite integral = net signed area.** ∫ₐᵇ = ∫ₐᶜ + ∫ᶜᵇ for any c.

**Chain + FTC extension (Stewart §5.4):**
d/dx ∫ₐᵍ⁽ˣ⁾ f(t) dt = f(g(x))·g'(x)
""",
    "Calc II — Integration Techniques": """
**Stewart Ch 7 — Techniques of Integration**

**Integration by Parts (§7.1):** ∫u dv = uv − ∫v du
LIATE priority for u: Log · Inverse trig · Algebraic · Trig · Exp

**Trig integrals (§7.2):** odd sin power → save sin x, convert rest via sin²=1−cos², u=cos x
Even powers → half-angle: sin²x = (1−cos2x)/2

**Trig substitution (§7.3):**
| √(a²−x²) | x = a sinθ |
| √(a²+x²) | x = a tanθ |
| √(x²−a²) | x = a secθ |

**Partial fractions (§7.4):** factor denominator → write A/(ax+b)+B/(cx+d)+...
Requires deg numerator < deg denominator (use long division first if not).

**Improper integrals (§7.8):** replace ∞ with b and take limit. p-integral ∫₁^∞ 1/xᵖ converges iff p>1.
""",
    "Calc II — Series & Convergence": """
**Stewart Ch 11 — Infinite Series**

**Divergence test (§11.2):** if lim aₙ ≠ 0, series diverges. If lim aₙ = 0, test is inconclusive.
**Geometric:** Σarⁿ converges iff |r|<1; sum = a/(1−r).
**p-series:** Σ1/nᵖ converges iff p>1.
**Integral test (§11.3):** ∫ f(x)dx converges ↔ Σf(n) converges (f positive, decreasing).
**Comparison (§11.4):** aₙ≤bₙ, Σbₙ converges → Σaₙ converges.
**Limit comparison:** lim aₙ/bₙ = c>0 → same convergence.
**Ratio test (§11.6):** L = lim|aₙ₊₁/aₙ|; L<1 converges, L>1 diverges, L=1 inconclusive.
**Alternating series (§11.5):** bₙ↓0 → Σ(−1)ⁿbₙ converges. Error ≤ first omitted term.
**Absolute convergence (§11.6):** Σ|aₙ| converges → Σaₙ absolutely converges.
""",
    "Calc II — Power & Taylor Series": """
**Stewart §11.9–11.10 — Power and Taylor Series**

**Power series** Σcₙ(x−a)ⁿ: radius R found by ratio test. Converges on (a−R, a+R).
**Taylor series:** f(x) = Σ f⁽ⁿ⁾(a)/n! · (x−a)ⁿ

**Maclaurin series (memorize):**
- eˣ = Σ xⁿ/n! = 1 + x + x²/2! + x³/3! + ... (R=∞)
- sin x = Σ (−1)ⁿ x²ⁿ⁺¹/(2n+1)! = x − x³/6 + x⁵/120 − ... (R=∞)
- cos x = Σ (−1)ⁿ x²ⁿ/(2n)! = 1 − x²/2 + x⁴/24 − ... (R=∞)
- 1/(1−x) = Σ xⁿ = 1+x+x²+... (|x|<1)
- ln(1+x) = Σ (−1)ⁿ⁺¹ xⁿ/n = x−x²/2+... (|x|≤1)
- arctan x = Σ (−1)ⁿ x²ⁿ⁺¹/(2n+1) = x−x³/3+... (|x|≤1)

**Use:** approximate functions, compute limits, integrate without antiderivative.
""",
    "Calc II — Parametric & Polar": """
**Stewart Ch 10 — Parametric and Polar**

**Parametric (§10.1–10.2):**
dy/dx = (dy/dt)/(dx/dt)
Arc length = ∫√([dx/dt]²+[dy/dt]²) dt
Area under parametric curve = ∫y dx = ∫ g(t)f'(t) dt

**Polar (§10.3–10.4):**
Convert: x = r cosθ, y = r sinθ; r² = x²+y²
Area enclosed: A = ½∫ r² dθ
Area between curves: A = ½∫(r₂²−r₁²) dθ
Arc length = ∫√(r²+(dr/dθ)²) dθ

**Common curves:** r=a (circle), r=a(1+cosθ) (cardioid, area=3πa²/2), r=sin(nθ) (rose).
""",
    "Calc III — Vectors & 3D Geometry": """
**Stewart Ch 12 — Vectors and the Geometry of Space**

**Dot product:** u·v = Σuᵢvᵢ = |u||v|cosθ. Perpendicular ↔ u·v=0.
**Cross product:** u×v = determinant formula; |u×v|=|u||v|sinθ = area of parallelogram. NOT commutative.
**Projection of u onto v:** (u·v/|v|²)v

**Lines:** r(t) = r₀ + t·d (parametric)
**Planes:** n·(r−r₀)=0 or ax+by+cz=d. Distance to point = |ax₁+by₁+cz₁−d|/|n|.

**Quadric surfaces (§12.6):** ellipsoid, paraboloid, hyperboloid — recognize from equation.
Ellipsoid: x²/a²+y²/b²+z²/c²=1. Paraboloid: z=x²+y². Cone: z²=x²+y².
""",
    "Calc III — Partial Derivatives": """
**Stewart Ch 14 — Partial Derivatives**

**∂f/∂x:** differentiate w.r.t. x, treat all other variables as constants.
**Clairaut's theorem:** fₓᵧ = f_yx (if second partials are continuous).
**Gradient:** ∇f = ⟨∂f/∂x, ∂f/∂y, ∂f/∂z⟩ — points toward steepest ascent, ⊥ level curves.
**Directional derivative:** D_û f = ∇f·û; max rate = |∇f| in direction of ∇f.
**Tangent plane at (a,b):** z = f(a,b) + fₓ(a,b)(x−a) + f_y(a,b)(y−b)
**Chain rule:** dz/dt = (∂z/∂x)(dx/dt) + (∂z/∂y)(dy/dt)

**Critical points:** ∇f = 0. Second derivative test: D = fₓₓf_yy − fₓy².
D>0, fₓₓ>0 → min. D>0, fₓₓ<0 → max. D<0 → saddle.
**Lagrange multipliers:** ∇f = λ∇g with constraint g=0.
""",
    "Calc III — Multiple Integrals": """
**Stewart Ch 15 — Multiple Integrals**

**Double integral:** ∬_D f dA — integrate in order. Fubini: switch order of integration when useful.
**Polar:** dA = r dr dθ; ∬_D f dA = ∫∫ f(r cosθ, r sinθ)·r dr dθ
**Triple integral:** in Cartesian, cylindrical (dV=r dz dr dθ), or spherical (dV=ρ² sinφ dρ dφ dθ).

**Cylindrical:** x=r cosθ, y=r sinθ, z=z
**Spherical:** x=ρ sinφ cosθ, y=ρ sinφ sinθ, z=ρ cosφ

**Jacobian for change of variables:** ∬ f dA = ∬ f(x(u,v),y(u,v))|J| du dv
where J = |∂(x,y)/∂(u,v)| = xᵤy_v − x_vy_u
""",
    "Calc III — Vector Calculus Theorems": """
**Stewart Ch 16 — Vector Calculus**

**Line integrals:** ∫_C f ds = ∫ f(r(t))|r'(t)| dt (scalar); ∫_C F·dr = ∫ F(r(t))·r'(t) dt (work)
**Conservative:** F=∇f ↔ curl F=0 ↔ path independent. Find f by integrating components.

**Green's Theorem (§16.4):**
∮_C P dx+Q dy = ∬_D (∂Q/∂x−∂P/∂y) dA  (C positively oriented = CCW)

**Stokes' Theorem (§16.8):**
∮_C F·dr = ∬_S (∇×F)·dS
Curl F = ⟨Ry−Qz, Pz−Rx, Qx−Py⟩

**Divergence Theorem (§16.9):**
∯_S F·dS = ∭_E (∇·F) dV  (S closed, outward normal)
Div F = ∂P/∂x+∂Q/∂y+∂R/∂z

**Pattern:** FTC → Green's (2D boundary→area) → Stokes (3D curve→surface) → Divergence (surface→volume)
""",
}

# ── Diagnostic Questions ──────────────────────────────────────────────────────
DIAGNOSTIC = [
    # Calc I
    {"q":"lim(x→2) (x²−4)/(x−2) equals:", "choices":["A) 0","B) 2","C) 4","D) DNE"],
     "answer":2, "topic":"Calc I — Limits & Continuity", "ch":"Stewart §2.3",
     "explanation":"Factor: (x+2)(x-2)/(x-2) → x+2. At x=2: **4**."},
    {"q":"d/dx[x²·sin(x)] =", "choices":["A) 2x sin x","B) x² cos x","C) 2x sin x + x² cos x","D) x² cos x − 2x sin x"],
     "answer":2, "topic":"Calc I — Derivatives & Rules", "ch":"Stewart §3.2",
     "explanation":"Product rule: (x²)'sin x + x²(sin x)' = 2x sin x + x² cos x."},
    {"q":"The absolute maximum of f(x)=x³−3x on [−2,2] is:", "choices":["A) 2","B) −2","C) 0","D) 1"],
     "answer":0, "topic":"Calc I — Applications of Derivatives", "ch":"Stewart §4.1",
     "explanation":"f'=3x²−3=0 → x=±1. f(−2)=−2, f(−1)=2, f(1)=−2, f(2)=2. Max = **2**."},
    {"q":"∫₀² 3x² dx =", "choices":["A) 6","B) 8","C) 4","D) 12"],
     "answer":1, "topic":"Calc I — Integrals & FTC", "ch":"Stewart §5.3",
     "explanation":"[x³]₀² = 8 − 0 = **8**."},
    {"q":"If G(x) = ∫₁ˣ √(t³+1) dt, then G'(2) =", "choices":["A) 2","B) 3","C) √9 = 3","D) 9"],
     "answer":1, "topic":"Calc I — Integrals & FTC", "ch":"Stewart §5.3",
     "explanation":"FTC Part 1: G'(x) = √(x³+1). G'(2) = √(8+1) = √9 = **3**."},
    # Calc II
    {"q":"∫ x ln(x) dx =", "choices":["A) ln(x)²/2+C","B) (x²/2)ln x − x²/4+C","C) x ln x − x+C","D) x²ln x+C"],
     "answer":1, "topic":"Calc II — Integration Techniques", "ch":"Stewart §7.1",
     "explanation":"IBP: u=ln x, dv=x dx → du=dx/x, v=x²/2. Result: (x²/2)ln x − ∫x/2 dx = **(x²/2)ln x − x²/4 + C**."},
    {"q":"Does Σ_{n=1}^∞ 1/n² converge?", "choices":["A) No — p-series p=2<1","B) No — harmonic series","C) Yes — p-series p=2>1","D) Inconclusive"],
     "answer":2, "topic":"Calc II — Series & Convergence", "ch":"Stewart §11.3",
     "explanation":"p-series Σ1/nᵖ converges iff p>1. Here p=2>1 → **converges** (sum = π²/6)."},
    {"q":"The ratio test on Σ n!/3ⁿ gives L =", "choices":["A) 0","B) 1/3","C) ∞","D) 1"],
     "answer":2, "topic":"Calc II — Series & Convergence", "ch":"Stewart §11.6",
     "explanation":"|aₙ₊₁/aₙ| = (n+1)!/3^{n+1} · 3ⁿ/n! = (n+1)/3 → ∞. L>1 → **diverges**."},
    {"q":"The Maclaurin series for eˣ starts:", "choices":["A) 1+x+x³/6+...","B) x+x²+x³+...","C) 1+x+x²/2!+x³/3!+...","D) x−x³/6+..."],
     "answer":2, "topic":"Calc II — Power & Taylor Series", "ch":"Stewart §11.10",
     "explanation":"eˣ = **1 + x + x²/2! + x³/3! + ...** converges for all x."},
    {"q":"Area enclosed by the cardioid r = 1+cos θ is:", "choices":["A) π","B) 3π/2","C) 2π","D) π/2"],
     "answer":1, "topic":"Calc II — Parametric & Polar", "ch":"Stewart §10.4",
     "explanation":"A = ½∫₋π^π (1+cosθ)² dθ = ½·3π = **3π/2**."},
    # Calc III
    {"q":"∇f at (1,1) for f(x,y)=x²y+y³:", "choices":["A) ⟨2,4⟩","B) ⟨2,1⟩","C) ⟨1,4⟩","D) ⟨2,4⟩"],
     "answer":0, "topic":"Calc III — Partial Derivatives", "ch":"Stewart §14.6",
     "explanation":"fₓ=2xy=2, f_y=x²+3y²=1+3=4. ∇f(1,1) = **⟨2,4⟩**."},
    {"q":"∬_D (x²+y²) dA over disk r≤2 in polar coordinates equals:", "choices":["A) 4π","B) 8π","C) 16π","D) 2π"],
     "answer":1, "topic":"Calc III — Multiple Integrals", "ch":"Stewart §15.3",
     "explanation":"∫₀^{2π}∫₀² r²·r dr dθ = 2π·[r⁴/4]₀² = 2π·4 = **8π**."},
    {"q":"F(x,y)=⟨2xy, x²+3y²⟩. Is F conservative?", "choices":["A) No","B) Yes — ∂P/∂y=∂Q/∂x","C) Only on simply connected regions","D) Cannot tell"],
     "answer":1, "topic":"Calc III — Vector Calculus Theorems", "ch":"Stewart §16.3",
     "explanation":"∂P/∂y = 2x = ∂Q/∂x = 2x. Equal → **F is conservative**."},
    {"q":"Green's theorem turns ∮_C P dx+Q dy into:", "choices":["A) A line integral over a larger curve","B) ∬_D (∂Q/∂x−∂P/∂y) dA","C) ∭_E (∇·F) dV","D) ∬_S (∇×F)·dS"],
     "answer":1, "topic":"Calc III — Vector Calculus Theorems", "ch":"Stewart §16.4",
     "explanation":"Green's theorem: ∮_C P dx+Q dy = ∬_D **(∂Q/∂x−∂P/∂y) dA**."},
    {"q":"The Divergence theorem converts ∯_S F·dS (closed S) to:", "choices":["A) ∮_C F·dr","B) ∬_D curl F dA","C) ∭_E (∇·F) dV","D) ∫_C f ds"],
     "answer":2, "topic":"Calc III — Vector Calculus Theorems", "ch":"Stewart §16.9",
     "explanation":"Divergence (Gauss) theorem: ∯_S F·dS = ∭_E **(∇·F) dV**."},
]

# ── Practice Questions ────────────────────────────────────────────────────────
PRACTICE = {
    "Calc I — Limits & Continuity": [
        {"q":"lim(x→0) sin(5x)/(3x) =","choices":["A) 1","B) 5/3","C) 3/5","D) 0"],"answer":1,
         "sol":"Rewrite: (5/3)·sin(5x)/(5x) → (5/3)·1 = **5/3**."},
        {"q":"lim(x→∞) (3x²+1)/(5x²−2) =","choices":["A) 3","B) 0","C) 3/5","D) ∞"],"answer":2,
         "sol":"Divide by x²: (3+1/x²)/(5−2/x²) → **3/5**."},
        {"q":"f(x)=(x²−4)/(x−2) has what kind of discontinuity at x=2?","choices":["A) Infinite","B) Jump","C) Removable","D) Continuous"],"answer":2,
         "sol":"Limit = 4 exists; f(2) undefined → **removable** discontinuity."},
    ],
    "Calc I — Derivatives & Rules": [
        {"q":"d/dx [arctan(2x)] =","choices":["A) 1/(1+4x²)","B) 2/(1+4x²)","C) 2/(1+2x²)","D) 1/(1+2x)"],"answer":1,
         "sol":"Chain rule: 1/(1+(2x)²) · 2 = **2/(1+4x²)**."},
        {"q":"d/dx [eˢⁱⁿˣ] =","choices":["A) eˢⁱⁿˣ","B) cos x · eˢⁱⁿˣ","C) sin x · eˢⁱⁿˣ","D) eᶜᵒˢˣ"],"answer":1,
         "sol":"Chain rule: eˢⁱⁿˣ · cos x = **cos x · eˢⁱⁿˣ**."},
    ],
    "Calc II — Integration Techniques": [
        {"q":"∫ sin³x dx =","choices":["A) −cos x+cos³x/3+C","B) 3sin²x cos x+C","C) −cos³x/3+C","D) sin²x·(−cos x)+C"],"answer":0,
         "sol":"Write sin²x·sin x = (1−cos²x)sin x. Sub u=cos x → **−cos x + cos³x/3 + C**."},
        {"q":"∫ 1/(x²+4) dx =","choices":["A) ln(x²+4)+C","B) arctan(x/2)/2+C","C) arctan(x)+C","D) −1/(x²+4)+C"],"answer":1,
         "sol":"Matches ∫1/(u²+a²)du = arctan(u/a)/a. Here a=2: **(1/2)arctan(x/2)+C**."},
    ],
    "Calc II — Series & Convergence": [
        {"q":"Does Σ 1/√n converge?","choices":["A) Yes — p>1","B) No — harmonic","C) No — p=1/2 ≤ 1","D) Inconclusive"],"answer":2,
         "sol":"p-series with p=1/2 < 1 → **diverges**."},
        {"q":"Does Σ (−1)ⁿ/n converge absolutely, conditionally, or diverge?","choices":["A) Absolutely","B) Diverges","C) Conditionally","D) Conditionally and absolutely"],"answer":2,
         "sol":"Σ|1/n| = harmonic = diverges (not absolute). AST: 1/n↓0 → converges. → **Conditionally convergent**."},
    ],
    "Calc III — Partial Derivatives": [
        {"q":"For f(x,y)=x³y−2xy², fₓy =","choices":["A) 3x²−4y","B) 6xy−4y","C) 3x²y","D) x³−4xy"],"answer":0,
         "sol":"fₓ = 3x²y−2y², then ∂/∂y: **3x² − 4y**."},
        {"q":"Tangent plane to z=x²+y² at (1,2,5): z =","choices":["A) 2x+4y−5","B) 2x+4y+5","C) x+2y","D) 2(x−1)+4(y−2)+5"],"answer":3,
         "sol":"fₓ(1,2)=2, f_y(1,2)=4. Plane: z−5=2(x−1)+4(y−2) → **z=2(x−1)+4(y−2)+5**."},
    ],
    "Calc III — Multiple Integrals": [
        {"q":"∫₀¹∫₀²  xy dy dx =","choices":["A) 1","B) 2","C) 1/2","D) 4"],"answer":0,
         "sol":"Inner ∫₀² xy dy = x[y²/2]₀² = 2x. Outer ∫₀¹ 2x dx = [x²]₀¹ = **1**."},
    ],
}

# ── Visualization Functions ───────────────────────────────────────────────────
DARK = {"figure.facecolor":"#0b1a2e","axes.facecolor":"#112240","axes.edgecolor":"#8fa8c8",
        "axes.labelcolor":"#e8eaf0","xtick.color":"#8fa8c8","ytick.color":"#8fa8c8",
        "text.color":"#e8eaf0","grid.color":"#1e3a5f","grid.alpha":0.4}

def _fig():
    fig, ax = plt.subplots(figsize=(7,4))
    for k,v in DARK.items(): plt.rcParams[k]=v
    fig.patch.set_facecolor("#0b1a2e"); ax.set_facecolor("#112240"); ax.grid(True)
    return fig, ax

def plot_derivative(func_name="x²"):
    fig, ax = _fig()
    x = np.linspace(-3, 3, 400)
    if func_name == "x²":
        y = x**2; a = 1.5; fa = a**2; m = 2*a
    elif func_name == "sin(x)":
        y = np.sin(x); a = 1.0; fa = np.sin(a); m = np.cos(a)
    else:
        y = x**3 - 3*x; a = 1.0; fa = a**3-3*a; m = 3*a**2-3
    tang = m*(x - a) + fa
    ax.plot(x, y, color="#f4c542", lw=2.5, label=f"f(x) = {func_name}")
    ax.plot(x, tang, color="#4fc3f7", lw=1.8, ls="--", label=f"Tangent at x={a}")
    ax.scatter([a],[fa], color="#f06292", s=80, zorder=5)
    ax.set_ylim(-5, 10); ax.legend(fontsize=9)
    ax.set_title(f"Derivative as Slope of Tangent Line", color="#f4c542", fontsize=11)
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

def plot_integral(func_name="x²"):
    fig, ax = _fig()
    x = np.linspace(0, 3, 400)
    y = x**2 if func_name == "x²" else np.sin(x)
    a, b = (0.5, 2.5)
    xf = np.linspace(a, b, 300); yf = xf**2 if func_name=="x²" else np.sin(xf)
    ax.fill_between(xf, yf, alpha=0.35, color="#f4c542", label=f"∫_{a}^{b} f dx")
    ax.plot(x, y, color="#f4c542", lw=2.5, label=f"f(x) = {func_name}")
    ax.set_ylim(-0.5, 10); ax.legend(fontsize=9)
    ax.set_title("Definite Integral as Area", color="#f4c542", fontsize=11)
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

def plot_series(n_terms=8):
    fig, ax = _fig()
    ns = np.arange(1, n_terms+1)
    partial = np.cumsum(1/ns**2)
    exact = np.pi**2/6
    ax.step(ns, partial, color="#f4c542", lw=2, where="post", label="Partial sum Sₙ = Σ1/k²")
    ax.axhline(exact, color="#4fc3f7", ls="--", lw=1.5, label=f"Limit = π²/6 ≈ {exact:.4f}")
    ax.set_xlabel("n"); ax.set_ylabel("Sₙ"); ax.legend(fontsize=9)
    ax.set_title("Series Convergence: Σ 1/n²", color="#f4c542", fontsize=11)
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

def plot_taylor(n_terms=5):
    fig, ax = _fig()
    x = np.linspace(-np.pi, np.pi, 500)
    ax.plot(x, np.sin(x), color="#f4c542", lw=2.5, label="sin(x)")
    approx = np.zeros_like(x)
    colors = ["#4fc3f7","#81c784","#ffb74d","#f06292","#ba68c8"]
    for k in range(n_terms):
        n = 2*k+1
        approx += ((-1)**k) * x**n / np.math.factorial(n)
        ax.plot(x, np.clip(approx,-3,3), color=colors[k%len(colors)], lw=1.5,
                ls="--", label=f"T_{n}(x)")
    ax.set_ylim(-2.5, 2.5); ax.legend(fontsize=7)
    ax.set_title("Taylor Polynomial Approximations of sin(x)", color="#f4c542", fontsize=11)
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

def plot_gradient():
    fig, ax = _fig()
    x = np.linspace(-2, 2, 20); y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    F = X**2 + Y**2
    Fx, Fy = 2*X, 2*Y
    cs = ax.contour(X, Y, F, levels=8, colors=["#f4c542"], alpha=0.5, linewidths=1)
    ax.clabel(cs, fontsize=7, fmt="%.1f", colors="#e8eaf0")
    ax.quiver(X[::2,::2], Y[::2,::2], Fx[::2,::2], Fy[::2,::2],
              color="#4fc3f7", alpha=0.85, scale=25)
    ax.set_title("Gradient Field of f(x,y) = x²+y²", color="#f4c542", fontsize=11)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

def plot_diagnostic_results(scores: dict):
    cats = list(scores.keys()); vals = list(scores.values())
    fig, ax = _fig()
    bars = ax.barh(cats, vals, color=["#f4c542" if v>=0.6 else "#f06292" for v in vals])
    ax.set_xlim(0, 1); ax.set_xlabel("Score")
    ax.set_title("Diagnostic Results by Area", color="#f4c542", fontsize=11)
    for bar, val in zip(bars, vals):
        ax.text(val+0.02, bar.get_y()+bar.get_height()/2, f"{val*100:.0f}%",
                va="center", color="#e8eaf0", fontsize=9)
    buf=io.BytesIO(); fig.savefig(buf,format="png",dpi=100,bbox_inches="tight"); plt.close(fig)
    buf.seek(0); return buf

PLOT_MAP = {
    "Calc I — Limits & Continuity": None,
    "Calc I — Derivatives & Rules": ("derivative","x²"),
    "Calc I — Applications of Derivatives": ("derivative","x³−3x"),
    "Calc I — Integrals & FTC": ("integral","x²"),
    "Calc II — Integration Techniques": ("integral","sin(x)"),
    "Calc II — Series & Convergence": ("series",8),
    "Calc II — Power & Taylor Series": ("taylor",5),
    "Calc II — Parametric & Polar": None,
    "Calc III — Vectors & 3D Geometry": None,
    "Calc III — Partial Derivatives": ("gradient",),
    "Calc III — Multiple Integrals": None,
    "Calc III — Vector Calculus Theorems": None,
}

def get_plot(topic):
    spec = PLOT_MAP.get(topic)
    if spec is None: return None
    if spec[0]=="derivative": return plot_derivative(spec[1])
    if spec[0]=="integral": return plot_integral(spec[1])
    if spec[0]=="series": return plot_series(spec[1])
    if spec[0]=="taylor": return plot_taylor(spec[1])
    if spec[0]=="gradient": return plot_gradient()
    return None

# ── Pathway Generator ─────────────────────────────────────────────────────────
DAYS_LEFT = (date(2026, 6, 21) - date.today()).days

def generate_pathway(scores: dict) -> str:
    areas = {"calc1": [], "calc2": [], "calc3": []}
    for topic, score in scores.items():
        area = TOPICS[topic]["area"]
        areas[area].append(score)
    area_avg = {k: (sum(v)/len(v) if v else 0) for k, v in areas.items()}
    ranked = sorted(area_avg.items(), key=lambda x: x[0])  # ordered calc1→3

    md = f"## 📍 Your USNA Validation Pathway\n\n"
    md += f"**{DAYS_LEFT} days until June 21 — exam window opens ~June 25 (I-Day).**\n\n"
    md += "### 📊 Area Scores\n"
    for area, avg in area_avg.items():
        label = {"calc1":"Calculus I","calc2":"Calculus II","calc3":"Calculus III"}[area]
        bar = "█"*int(avg*10) + "░"*(10-int(avg*10))
        status = "✅ Strong" if avg>=0.7 else ("⚠️ Review" if avg>=0.4 else "🔴 Focus Here")
        md += f"- **{label}:** {bar} {avg*100:.0f}%  {status}\n"

    md += "\n### 📅 Recommended 3-Week Plan\n"
    # Build around weak areas first, but respect Calc I→II→III sequence
    if area_avg["calc1"] < 0.6:
        md += "- **Week 1 (Jun 1–7):** 🔴 Prioritize Calc I — Ch 2–5 Stewart. Limits, derivatives, FTC, u-sub. Do all Calc I practice problems.\n"
    else:
        md += "- **Week 1 (Jun 1–7):** ✅ Calc I solid. Quick review + move to Calc II techniques (Ch 7 IBP, trig sub, partial fractions).\n"
    if area_avg["calc2"] < 0.6:
        md += "- **Week 2 (Jun 8–14):** 🔴 Focus Calc II — Ch 7 integration techniques + Ch 11 series. Drill convergence tests daily.\n"
    else:
        md += "- **Week 2 (Jun 8–14):** ✅ Calc II OK. Start Calc III vectors + partial derivatives (Ch 12, 14).\n"
    if area_avg["calc3"] < 0.6:
        md += "- **Week 3 (Jun 15–21):** 🔴 Calc III is the hardest exam. Focus Green's/Stokes/Divergence. Do ALL free-response style problems.\n"
    else:
        md += "- **Week 3 (Jun 15–21):** ✅ Calc III looks solid. Final timed practice exams + review any flagged topics.\n"

    weak_topics = [t for t,s in scores.items() if s < 0.5]
    if weak_topics:
        md += f"\n### ⚡ Immediate Focus Topics\n"
        for t in weak_topics:
            md += f"- **{t}** ({TOPICS[t]['ch']}) — review concept sheet, do all practice problems\n"

    md += "\n### 🗓️ Daily Routine Suggestion\n"
    md += "- **30 min:** Read Stewart section + concept sheet\n"
    md += "- **30 min:** Practice problems (use FissionLab Practice tab)\n"
    md += "- **15 min:** Review any wrong answers + re-read explanations\n"
    md += "\n*Calc I exams around June 25–26. Calc II exam Week 2 of Plebe Summer. Calc III Week 2–3.*"
    return md

# ── Gradio App ────────────────────────────────────────────────────────────────
CSS = """
.gradio-container{background:#0b1a2e!important;color:#e8eaf0!important;font-family:'Segoe UI',system-ui,sans-serif}
h1,h2,h3{color:#f4c542!important}
.gr-button-primary{background:#f4c542!important;color:#0b1a2e!important;font-weight:700!important;border:none!important}
.gr-button{border:1px solid #b89630!important;color:#f4c542!important;background:transparent!important}
.gr-box,.gr-form,.gr-panel{background:#112240!important;border-color:#1e3a5f!important}
label,p,span{color:#e8eaf0!important}
.token-display{font-family:monospace;letter-spacing:0.08em;color:#f4c542}
footer{display:none!important}
"""

def new_session():
    qs = DIAGNOSTIC[:]
    random.shuffle(qs)
    return {"verified":False,"free_used":0,"diag_idx":0,"diag_scores":{},"diag_done":False,"qs":qs}

with gr.Blocks(css=CSS, title="FissionLab Math — Dr. Preston PhD") as demo:
    state = gr.State(new_session())

    gr.Markdown("# 📐 FissionLab Math Practice — Dr. Preston PhD")
    gr.Markdown(
        "*Calculus I / II / III — Aligned with Stewart Early Transcendentals (2015) · "
        "USNA Validation Prep*",
    )

    with gr.Tabs():
        # ── TAB 1: DIAGNOSTIC ────────────────────────────────────────────────
        with gr.Tab("🎯 Diagnostic"):
            gr.Markdown("### Take the 15-question diagnostic to get your personalized study pathway.")
            diag_q    = gr.Markdown("*Click Start Diagnostic to begin.*")
            diag_radio= gr.Radio(choices=[], label="Select your answer:", interactive=True, visible=False)
            diag_info = gr.Markdown("")
            with gr.Row():
                diag_start  = gr.Button("▶ Start Diagnostic", variant="primary")
                diag_submit = gr.Button("Submit Answer", visible=False)
                diag_next   = gr.Button("Next Question →", visible=False)
            diag_progress = gr.Markdown("")
            diag_result   = gr.Markdown("")
            diag_chart    = gr.Image(label="Performance Chart", visible=False, type="pil")
            diag_pathway  = gr.Markdown("")

            def start_diag(s):
                s = new_session(); s["diag_idx"] = 0
                q = s["qs"][0]
                return (s,
                        gr.update(value=f"**Q1 / {len(DIAGNOSTIC)}** [{q['ch']}]\n\n{q['q']}"),
                        gr.update(choices=q["choices"], value=None, interactive=True, visible=True),
                        gr.update(value=""),
                        gr.update(visible=False),
                        gr.update(visible=True, value="Submit Answer"),
                        gr.update(visible=False),
                        gr.update(value=f"*Progress: 0/{len(DIAGNOSTIC)} complete*"),
                        gr.update(value=""), gr.update(visible=False), gr.update(value=""))

            def submit_diag(choice, s):
                if choice is None:
                    return s, gr.update(), gr.update(value="⚠️ Please select an answer first."), gr.update(visible=False)
                q = s["qs"][s["diag_idx"]]
                correct_str = q["choices"][q["answer"]]
                correct = (choice == correct_str)
                s["diag_scores"][q["topic"]] = s["diag_scores"].get(q["topic"],0) + (1 if correct else 0)
                icon = "✅ Correct!" if correct else f"❌ Incorrect. Correct: **{correct_str}**"
                feedback = f"{icon}\n\n{q['explanation']}"
                return (s, gr.update(interactive=False),
                        gr.update(value=feedback),
                        gr.update(visible=True, value="Next Question →" if s["diag_idx"]<len(DIAGNOSTIC)-1 else "See My Results →"))

            def next_diag(s):
                s["diag_idx"] += 1
                prog = f"*Progress: {s['diag_idx']}/{len(DIAGNOSTIC)} complete*"
                if s["diag_idx"] >= len(DIAGNOSTIC):
                    # Build score per topic
                    raw = s["diag_scores"]
                    # normalise: each topic may appear once
                    topic_counts = {}
                    for q in s["qs"]:
                        topic_counts[q["topic"]] = topic_counts.get(q["topic"],0)+1
                    scores = {t: raw.get(t,0)/cnt for t,cnt in topic_counts.items()}
                    s["diag_done"] = True
                    pathway = generate_pathway(scores)
                    area_scores = {}
                    area_counts = {}
                    for t,sc in scores.items():
                        a = TOPICS[t]["area"]
                        area_scores[a] = area_scores.get(a,0)+sc
                        area_counts[a] = area_counts.get(a,0)+1
                    area_avg = {{"calc1":"Calc I","calc2":"Calc II","calc3":"Calc III"}[k]: v/area_counts[k]
                                for k,v in area_scores.items()}
                    buf = plot_diagnostic_results(area_avg)
                    from PIL import Image as PILImage
                    img = PILImage.open(buf)
                    return (s,
                            gr.update(value="## 🎉 Diagnostic Complete!"),
                            gr.update(choices=[], visible=False),
                            gr.update(value=""),
                            gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                            gr.update(value=prog),
                            gr.update(value=pathway),
                            gr.update(visible=True, value=img),
                            gr.update(value=""))
                q = s["qs"][s["diag_idx"]]
                n = s["diag_idx"]+1
                return (s,
                        gr.update(value=f"**Q{n} / {len(DIAGNOSTIC)}** [{q['ch']}]\n\n{q['q']}"),
                        gr.update(choices=q["choices"], value=None, interactive=True, visible=True),
                        gr.update(value=""),
                        gr.update(visible=False),
                        gr.update(visible=True, value="Submit Answer"),
                        gr.update(visible=False),
                        gr.update(value=prog),
                        gr.update(value=""), gr.update(visible=False), gr.update(value=""))

            diag_start.click(start_diag, [state],
                [state,diag_q,diag_radio,diag_info,diag_start,diag_submit,diag_next,diag_progress,diag_pathway,diag_chart,diag_result])
            diag_submit.click(submit_diag, [diag_radio,state],
                [state,diag_radio,diag_info,diag_next])
            diag_next.click(next_diag, [state],
                [state,diag_q,diag_radio,diag_info,diag_start,diag_submit,diag_next,diag_progress,diag_pathway,diag_chart,diag_result])

        # ── TAB 2: TOPIC GUIDE ───────────────────────────────────────────────
        with gr.Tab("📚 Topic Guide"):
            gr.Markdown("### Stewart-aligned concept reviews with visualizations.")
            topic_dd  = gr.Dropdown(choices=list(TOPICS.keys()), label="Select Topic", value=list(TOPICS.keys())[0])
            topic_exp = gr.Markdown("")
            topic_img = gr.Image(label="Visualization", visible=False, type="pil")

            def load_topic(topic):
                from PIL import Image as PILImage
                exp = EXPLANATIONS.get(topic,"*No explanation available.*")
                buf = get_plot(topic)
                if buf:
                    img = PILImage.open(buf)
                    return gr.update(value=exp), gr.update(visible=True, value=img)
                return gr.update(value=exp), gr.update(visible=False)

            topic_dd.change(load_topic, [topic_dd], [topic_exp, topic_img])
            demo.load(load_topic, [topic_dd], [topic_exp, topic_img])

        # ── TAB 3: PRACTICE ──────────────────────────────────────────────────
        with gr.Tab("🏋️ Practice"):
            gr.Markdown("### Graded problems with worked solutions. Token required for full access.")
            practice_topics = [t for t in PRACTICE.keys()]
            prac_topic = gr.Dropdown(choices=practice_topics, label="Topic", value=practice_topics[0])
            prac_q     = gr.Markdown("")
            prac_radio = gr.Radio(choices=[], label="Your answer:", interactive=True, visible=False)
            prac_info  = gr.Markdown("")
            prac_score = gr.Markdown("")
            with gr.Row():
                prac_load   = gr.Button("Load Question", variant="primary")
                prac_submit = gr.Button("Submit", visible=False)
                prac_next   = gr.Button("Next →", visible=False)
            prac_state = gr.State({"topic":practice_topics[0],"idx":0,"score":0,"total":0,"verified":False,"free_used":0})

            def load_prac(topic, ps):
                ps["topic"]=topic; ps["idx"]=0; ps["score"]=0; ps["total"]=0
                qs = PRACTICE.get(topic,[])
                if not qs: return ps,gr.update(value="*No problems yet for this topic.*"),gr.update(visible=False),gr.update(value=""),gr.update(value=""),gr.update(visible=False),gr.update(visible=False)
                q = qs[0]
                return (ps,gr.update(value=f"**Problem 1/{len(qs)}:** {q['q']}"),
                        gr.update(choices=q["choices"],value=None,interactive=True,visible=True),
                        gr.update(value=""),gr.update(value=f"Score: 0/0"),
                        gr.update(visible=True,value="Submit"),gr.update(visible=False))

            def submit_prac(choice, ps):
                if choice is None:
                    return ps, gr.update(value="⚠️ Select an answer."), gr.update(visible=False)
                qs = PRACTICE.get(ps["topic"],[])
                if ps["idx"] >= len(qs):
                    return ps, gr.update(value="Quiz complete."), gr.update(visible=False)
                q = qs[ps["idx"]]
                correct = (choice == q["choices"][q["answer"]])
                if correct: ps["score"]+=1
                ps["total"]+=1
                feedback = ("✅ Correct!" if correct else f"❌ Incorrect. Correct: **{q['choices'][q['answer']]}**")
                return (ps,
                        gr.update(value=f"{feedback}\n\n**Solution:** {q['sol']}"),
                        gr.update(visible=True,value="Next →" if ps["idx"]<len(qs)-1 else "Done ✓"))

            def next_prac(ps):
                ps["idx"]+=1
                qs = PRACTICE.get(ps["topic"],[])
                sc = f"Score: {ps['score']}/{ps['total']}"
                if ps["idx"]>=len(qs):
                    return ps,gr.update(value=f"**Done! Final score: {ps['score']}/{ps['total']}**"),gr.update(visible=False),gr.update(value=""),gr.update(value=sc),gr.update(visible=False),gr.update(visible=False)
                q=qs[ps["idx"]]
                return (ps,gr.update(value=f"**Problem {ps['idx']+1}/{len(qs)}:** {q['q']}"),
                        gr.update(choices=q["choices"],value=None,interactive=True,visible=True),
                        gr.update(value=""),gr.update(value=sc),
                        gr.update(visible=True,value="Submit"),gr.update(visible=False))

            prac_load.click(load_prac,[prac_topic,prac_state],[prac_state,prac_q,prac_radio,prac_info,prac_score,prac_submit,prac_next])
            prac_submit.click(submit_prac,[prac_radio,prac_state],[prac_state,prac_info,prac_next])
            prac_next.click(next_prac,[prac_state],[prac_state,prac_q,prac_radio,prac_info,prac_score,prac_submit,prac_next])

        # ── TAB 4: STUDY PLAN ────────────────────────────────────────────────
        with gr.Tab("📅 3-Week Plan"):
            gr.Markdown(f"### USNA Validation Study Plan — {DAYS_LEFT} days until June 21")
            gr.Markdown("""
**Exam Schedule (approximate):**
- 📌 **Calc I:** Day 1–2 of Plebe Summer (~June 25–26)
- 📌 **Calc II:** Plebe Summer Week 2 (~July 1–3, multiple choice)
- 📌 **Calc III:** Plebe Summer Week 2–3 (MC + free response)

---

**Week 1: June 1–7 — Calculus I Mastery**
- Mon: Stewart Ch 2 — Limits. Do all limit practice problems here.
- Tue: Stewart Ch 3 — Derivative rules (power, product, quotient, chain).
- Wed: Stewart Ch 3 — Trig, exp, log derivatives + implicit differentiation.
- Thu: Stewart Ch 4 — Optimization + related rates (most tested applications).
- Fri: Stewart Ch 5 — FTC Parts 1 & 2 + u-substitution.
- Sat: **Mock Calc I** — 20 problems timed, review all wrong answers.
- Sun: Rest / light review.

**Week 2: June 8–14 — Calculus II**
- Mon: Stewart Ch 7 — Integration by parts + trig integrals.
- Tue: Stewart Ch 7 — Trig substitution + partial fractions.
- Wed: Stewart Ch 11 — Sequences, series, divergence test, geometric/p-series.
- Thu: Stewart Ch 11 — Integral test, comparison, ratio, alternating series.
- Fri: Stewart Ch 11 — Power series, Taylor/Maclaurin (memorize 6 key series).
- Sat: Stewart Ch 10 — Parametric + polar (area formula).
- Sun: **Mock Calc II** — timed MC practice.

**Week 3: June 15–21 — Calculus III (Hardest Exam)**
- Mon: Stewart Ch 12 — Vectors, dot/cross product, lines & planes in 3D.
- Tue: Stewart Ch 14 — Partial derivatives, gradient, directional derivative, tangent plane.
- Wed: Stewart Ch 14 — Optimization, Lagrange multipliers.
- Thu: Stewart Ch 15 — Double/triple integrals in Cartesian + polar/cylindrical/spherical.
- Fri: Stewart Ch 16 — Line integrals, conservative fields, Green's theorem.
- Sat: Stewart Ch 16 — Stokes' theorem, Divergence theorem (free-response practice).
- Sun: **Mock Calc III** — full timed practice with free-response problems.

---
*Use the Diagnostic tab to get your personalized version of this plan.*
""")

        # ── TAB 5: UNLOCK ────────────────────────────────────────────────────
        with gr.Tab("🔑 Unlock"):
            gr.Markdown("## Unlock Full Access\nEnter your FissionLab token (FLAB-XXXX-XXXX-XXXX).")
            tok_in  = gr.Textbox(label="Token", placeholder="FLAB-XXXX-XXXX-XXXX")
            tok_btn = gr.Button("Verify Token", variant="primary")
            tok_out = gr.Markdown("")
            gr.Markdown("Don't have a token? Contact **Dr_PrestonD@proton.me**")

            def verify_action(token, s):
                if verify_token(token):
                    s["verified"] = True
                    return s, "✅ **Premium unlocked!** Full access to all topics and unlimited practice."
                return s, "❌ Invalid token. Check format (FLAB-XXXX-XXXX-XXXX) or contact Dr. Preston."
            tok_btn.click(verify_action, [tok_in, state], [state, tok_out])

    gr.Markdown("<div style='text-align:center;color:#8fa8c8;font-size:0.8rem;margin-top:20px'>Dr. Preston — PhD Nuclear Engineering · FissionLab · Aligned with Stewart Calculus Early Transcendentals 8e (2015)</div>")

if __name__ == "__main__":
    demo.launch()
