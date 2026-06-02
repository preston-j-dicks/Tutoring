"""
FissionLab Math Practice App v3.0 — Dr. Preston PhD
Calculus I / II / III — USNA Validation Prep
Aligned with Stewart Early Transcendentals 8e (2015), Cengage
10 questions at a time · 20-question diagnostic · Solutions at end only
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

# ── Styling ──────────────────────────────────────────────────────────────────
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
.q-tag{color:rgba(232,234,240,0.4);font-size:0.72rem;margin-top:6px;letter-spacing:0.04em}
.correct-box{background:rgba(40,200,100,0.1);border-left:3px solid #28c864;padding:12px 16px;border-radius:0 8px 8px 0;margin:6px 0}
.wrong-box{background:rgba(255,80,80,0.08);border-left:3px solid #ff5050;padding:12px 16px;border-radius:0 8px 8px 0;margin:6px 0}
.solution-text{background:rgba(20,40,80,0.6);border:1px solid rgba(100,150,255,0.2);border-radius:8px;padding:12px 16px;margin-top:8px;font-size:0.88rem;color:rgba(232,234,240,0.85)}
.score-banner{text-align:center;padding:28px;background:rgba(201,168,76,0.08);border:1px solid rgba(201,168,76,0.25);border-radius:12px;margin-bottom:20px}
footer{display:none!important}
"""

DIVIDER = "<hr style='border:none;border-top:1px solid rgba(201,168,76,0.2);margin:18px 0'>"

# ── Formula image renderer ────────────────────────────────────────────────────
def fimg(latex: str, fs: int = 14) -> str:
    """Render LaTeX formula as base64 PNG via matplotlib mathtext."""
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

# Pre-render all formula images once at startup
_F = {
    # Calc I
    'deriv_def':   r'\dfrac{d}{dx}f = \lim_{h \to 0} \dfrac{f(x+h)-f(x)}{h}',
    'power':       r'\dfrac{d}{dx}\left[x^n\right] = n\,x^{n-1}',
    'product':     r'(fg)^\prime = f^\prime g + f\,g^\prime',
    'quotient':    r'\left(\dfrac{f}{g}\right)^\prime = \dfrac{f^\prime g - f\,g^\prime}{g^2}',
    'chain':       r'\dfrac{d}{dx}\left[f(g(x))\right] = f^\prime(g(x))\cdot g^\prime(x)',
    'lhopital':    r'\lim_{x\to a}\dfrac{f(x)}{g(x)} = \lim_{x\to a}\dfrac{f^\prime(x)}{g^\prime(x)}\quad(0/0\text{ or }\infty/\infty)',
    'ftc1':        r'\dfrac{d}{dx}\int_a^x f(t)\,dt = f(x)',
    'ftc2':        r'\int_a^b f(x)\,dx = F(b) - F(a)',
    'power_int':   r'\int x^n\,dx = \dfrac{x^{n+1}}{n+1} + C \quad (n \neq -1)',
    # Calc II
    'ibp':         r'\int u\,dv = uv - \int v\,du',
    'p_series':    r'\sum_{n=1}^{\infty}\dfrac{1}{n^p}\;\text{converges iff }p > 1',
    'ratio_test':  r'L = \lim_{n\to\infty}\left|\dfrac{a_{n+1}}{a_n}\right|;\;\;L<1\Rightarrow\text{converges}',
    'taylor':      r'f(x) = \sum_{n=0}^{\infty}\dfrac{f^{(n)}(a)}{n!}(x-a)^n',
    'maclaurin_e': r'e^x = \sum_{n=0}^{\infty}\dfrac{x^n}{n!} = 1 + x + \dfrac{x^2}{2!} + \cdots',
    'maclaurin_s': r'\sin x = x - \dfrac{x^3}{3!} + \dfrac{x^5}{5!} - \cdots',
    'maclaurin_c': r'\cos x = 1 - \dfrac{x^2}{2!} + \dfrac{x^4}{4!} - \cdots',
    # Calc III
    'gradient':    r'\nabla f = \dfrac{\partial f}{\partial x}\hat{i} + \dfrac{\partial f}{\partial y}\hat{j} + \dfrac{\partial f}{\partial z}\hat{k}',
    'directional': r'D_{\hat{u}} f = \nabla f \cdot \hat{u} \quad\text{(max rate} = |\nabla f|\text{)}',
    'greens':      r'\oint_C P\,dx + Q\,dy = \iint_D\!\!\left(\dfrac{\partial Q}{\partial x} - \dfrac{\partial P}{\partial y}\right)dA',
    'stokes':      r'\oint_C \mathbf{F}\cdot d\mathbf{r} = \iint_S (\nabla \times \mathbf{F})\cdot d\mathbf{S}',
    'divergence':  r'\iint_S \mathbf{F}\cdot d\mathbf{S} = \iiint_E (\nabla \cdot \mathbf{F})\,dV',
}
FORMULA_IMGS = {}
for key, latex in _F.items():
    FORMULA_IMGS[key] = fimg(latex)

# ── Stewart Chapter Map ───────────────────────────────────────────────────────
TOPICS = {
    "Calc I — Limits & Continuity":         {"ch": "Ch 2",  "area": "calc1"},
    "Calc I — Derivatives & Rules":         {"ch": "Ch 3",  "area": "calc1"},
    "Calc I — Applications of Derivatives": {"ch": "Ch 4",  "area": "calc1"},
    "Calc I — Integrals & FTC":             {"ch": "Ch 5",  "area": "calc1"},
    "Calc II — Integration Techniques":     {"ch": "Ch 7",  "area": "calc2"},
    "Calc II — Series & Convergence":       {"ch": "Ch 11", "area": "calc2"},
    "Calc II — Power & Taylor Series":      {"ch": "Ch 11", "area": "calc2"},
    "Calc II — Parametric & Polar":         {"ch": "Ch 10", "area": "calc2"},
    "Calc III — Vectors & 3D Geometry":     {"ch": "Ch 12", "area": "calc3"},
    "Calc III — Partial Derivatives":       {"ch": "Ch 14", "area": "calc3"},
    "Calc III — Multiple Integrals":        {"ch": "Ch 15", "area": "calc3"},
    "Calc III — Vector Calculus Theorems":  {"ch": "Ch 16", "area": "calc3"},
}

def _topic_html(title: str, body: str, formulas: list = None) -> str:
    """Build HTML for a topic guide section with optional formula images."""
    lines = [f'<div style="max-width:860px;line-height:1.75">',
             f'<h3 style="font-family:Georgia,serif;color:#f4c542;border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:14px">{title}</h3>',
             f'<div style="color:rgba(232,234,240,0.88);font-size:0.92rem">{body}</div>']
    if formulas:
        lines.append('<div style="margin:16px 0">')
        for fi in formulas:
            lines.append(FORMULA_IMGS.get(fi, ''))
        lines.append('</div>')
    lines.append('</div>')
    return '\n'.join(lines)

TOPIC_HTML = {
    "Calc I — Limits & Continuity": _topic_html(
        "Calc I — Limits &amp; Continuity · Stewart Ch 2",
        "<b>Definition:</b> lim(x→a) f(x) = L means f(x) → L as x → a (regardless of f(a)).<br><br>"
        "<b>Key techniques:</b> Direct substitution → factor/cancel → L'Hôpital (0/0 or ∞/∞ only) → Squeeze theorem.<br><br>"
        "<b>Critical limits:</b> lim(x→0) sin(x)/x = <b>1</b> &nbsp;·&nbsp; lim(x→0)(1−cos x)/x = <b>0</b> &nbsp;·&nbsp; lim(x→∞)(1+1/x)ˣ = <b>e</b><br><br>"
        "<b>Continuity at a:</b> f(a) defined, limit exists, and they are equal.<br>"
        '<div style="background:rgba(201,168,76,0.1);border-left:3px solid #f4c542;padding:10px 14px;margin-top:12px;border-radius:0 6px 6px 0">'
        "<b>USNA trap:</b> L'Hôpital applies <em>only</em> to 0/0 or ±∞/±∞. Rewrite 0·∞ first.</div>",
        ['lhopital']),
    "Calc I — Derivatives & Rules": _topic_html(
        "Calc I — Derivatives &amp; Rules · Stewart Ch 3",
        "<b>Power:</b> d/dx[xⁿ] = nxⁿ⁻¹ &nbsp;·&nbsp; <b>Product:</b> (uv)' = u'v + uv' &nbsp;·&nbsp; <b>Quotient:</b> (u/v)' = (u'v−uv')/v²<br><br>"
        "<b>Trig:</b> (sin x)' = cos x &nbsp;·&nbsp; (cos x)' = −sin x &nbsp;·&nbsp; (tan x)' = sec²x<br>"
        "<b>Exp/Log:</b> (eˣ)' = eˣ &nbsp;·&nbsp; (ln x)' = 1/x &nbsp;·&nbsp; (arctan x)' = 1/(1+x²)<br>"
        '<div style="background:rgba(201,168,76,0.1);border-left:3px solid #f4c542;padding:10px 14px;margin-top:12px;border-radius:0 6px 6px 0">'
        "<b>Most tested:</b> Chain rule — never skip it inside trig/exp/log.</div>",
        ['deriv_def', 'chain']),
    "Calc I — Applications of Derivatives": _topic_html(
        "Calc I — Applications · Stewart Ch 4",
        "<b>Optimization:</b> 1) Write f(x). 2) f'(x)=0 → critical pts. 3) 2nd deriv test or closed interval check.<br>"
        "<b>Related rates:</b> relate quantities → differentiate both sides w.r.t. t → substitute last.<br>"
        "<b>Curve sketching:</b> sign charts for f' (inc/dec) and f'' (concavity/inflection).<br>"
        "<b>L'Hôpital:</b> indeterminate 0/0 or ∞/∞ only.",
        ['power', 'quotient']),
    "Calc I — Integrals & FTC": _topic_html(
        "Calc I — Integrals &amp; FTC · Stewart Ch 5",
        "<b>Key antiderivatives:</b> ∫xⁿdx = xⁿ⁺¹/(n+1)+C &nbsp;·&nbsp; ∫1/x dx = ln|x|+C &nbsp;·&nbsp; ∫eˣdx = eˣ+C<br>"
        "∫sin x dx = −cos x+C &nbsp;·&nbsp; ∫cos x dx = sin x+C &nbsp;·&nbsp; ∫sec²x dx = tan x+C<br><br>"
        "<b>u-Substitution:</b> Reverse chain rule. Let u = g(x), du = g'(x)dx.<br>"
        "<b>Chain+FTC:</b> d/dx[∫ₐᵍ⁽ˣ⁾f(t)dt] = f(g(x))·g'(x)",
        ['ftc1', 'ftc2', 'power_int']),
    "Calc II — Integration Techniques": _topic_html(
        "Calc II — Integration Techniques · Stewart Ch 7",
        "<b>IBP LIATE priority for u:</b> Logarithm → Inverse trig → Algebraic → Trig → Exponential<br>"
        "<b>Trig sub:</b> √(a²−x²)→x=a sinθ &nbsp;·&nbsp; √(a²+x²)→x=a tanθ &nbsp;·&nbsp; √(x²−a²)→x=a secθ<br>"
        "<b>Partial fractions:</b> factor denominator, write A/(ax+b)+B/(cx+d)+... Degree of numerator must be less.<br>"
        "<b>Improper integrals:</b> replace ∞ with b, take limit. ∫₁^∞ 1/xᵖ converges iff p>1.",
        ['ibp']),
    "Calc II — Series & Convergence": _topic_html(
        "Calc II — Series &amp; Convergence · Stewart Ch 11",
        "<b>Tests:</b> Divergence test (lim≠0→diverges) → Geometric (|r|<1) → p-series (p>1) → Integral → Comparison → Ratio → AST<br>"
        "<b>Geometric:</b> Σarⁿ converges iff |r|<1; sum = a/(1−r).<br>"
        "<b>Ratio test:</b> L=lim|aₙ₊₁/aₙ|; L<1 converges, L>1 diverges, L=1 inconclusive.<br>"
        "<b>Alternating series (AST):</b> bₙ↓0 → Σ(−1)ⁿbₙ converges. Error ≤ first omitted term.",
        ['p_series', 'ratio_test']),
    "Calc II — Power & Taylor Series": _topic_html(
        "Calc II — Power &amp; Taylor Series · Stewart Ch 11",
        "<b>Radius of convergence R:</b> use ratio test. Converges on (a−R, a+R).<br><br>"
        "<b>Memorize these Maclaurin series:</b><br>"
        "eˣ = 1+x+x²/2!+x³/3!+... (R=∞) &nbsp;·&nbsp; 1/(1−x) = 1+x+x²+... (|x|<1)<br>"
        "ln(1+x) = x−x²/2+x³/3−... &nbsp;·&nbsp; arctan x = x−x³/3+x⁵/5−...",
        ['taylor', 'maclaurin_e', 'maclaurin_s', 'maclaurin_c']),
    "Calc II — Parametric & Polar": _topic_html(
        "Calc II — Parametric &amp; Polar · Stewart Ch 10",
        "<b>Parametric:</b> dy/dx = (dy/dt)/(dx/dt) &nbsp;·&nbsp; arc length = ∫√([dx/dt]²+[dy/dt]²)dt<br>"
        "<b>Polar:</b> x=r cosθ, y=r sinθ, r²=x²+y²<br>"
        "<b>Polar area:</b> A = ½∫r²dθ &nbsp;·&nbsp; Between curves: ½∫(r₂²−r₁²)dθ<br>"
        "<b>Common curves:</b> r=a(1+cosθ) cardioid (area=3πa²/2); r=sin(nθ) rose.",
        []),
    "Calc III — Vectors & 3D Geometry": _topic_html(
        "Calc III — Vectors &amp; 3D Geometry · Stewart Ch 12",
        "<b>Dot product:</b> u·v = |u||v|cosθ. Perpendicular ↔ u·v=0.<br>"
        "<b>Cross product:</b> |u×v| = |u||v|sinθ = area of parallelogram. Not commutative.<br>"
        "<b>Projection of u onto v:</b> (u·v/|v|²)v<br>"
        "<b>Line:</b> r(t)=r₀+td &nbsp;·&nbsp; <b>Plane:</b> n·(r−r₀)=0",
        []),
    "Calc III — Partial Derivatives": _topic_html(
        "Calc III — Partial Derivatives · Stewart Ch 14",
        "<b>∂f/∂x:</b> differentiate w.r.t. x, hold all other variables constant.<br>"
        "<b>Clairaut:</b> fₓᵧ = fyₓ (if second partials continuous).<br>"
        "<b>Tangent plane at (a,b):</b> z = f(a,b)+fₓ(a,b)(x−a)+fy(a,b)(y−b)<br>"
        "<b>2nd derivative test:</b> D = fₓₓfyy−fₓy². D>0,fₓₓ>0→min; D>0,fₓₓ<0→max; D<0→saddle.<br>"
        "<b>Lagrange:</b> ∇f = λ∇g",
        ['gradient', 'directional']),
    "Calc III — Multiple Integrals": _topic_html(
        "Calc III — Multiple Integrals · Stewart Ch 15",
        "<b>Double integral:</b> ∬_D f dA — Fubini: switch order when useful.<br>"
        "<b>Polar:</b> dA = r dr dθ; ∬_D f dA = ∫∫ f(r cosθ,r sinθ)·r dr dθ<br>"
        "<b>Cylindrical:</b> dV = r dz dr dθ &nbsp;·&nbsp; <b>Spherical:</b> dV = ρ²sinφ dρ dφ dθ<br>"
        "<b>Jacobian:</b> ∬f dA = ∬f(x(u,v),y(u,v))|J| du dv",
        []),
    "Calc III — Vector Calculus Theorems": _topic_html(
        "Calc III — Vector Calculus Theorems · Stewart Ch 16",
        "<b>Conservative:</b> F=∇f ↔ curl F=0 ↔ path independent.<br>"
        "<b>Green's:</b> ∮_C P dx+Q dy = ∬_D(∂Q/∂x−∂P/∂y)dA (C = CCW boundary).<br>"
        "<b>Stokes':</b> ∮_C F·dr = ∬_S(∇×F)·dS<br>"
        "<b>Divergence:</b> ∬_S F·dS = ∭_E(∇·F)dV (S = closed outward surface).<br>"
        "<b>Pattern:</b> FTC → Green's (2D) → Stokes (3D curve→surface) → Divergence (surface→volume)",
        ['greens', 'stokes', 'divergence']),
}

# ── 20 Diagnostic Questions ───────────────────────────────────────────────────
# 7 Calc I · 7 Calc II · 6 Calc III
DIAGNOSTIC = [
    # ─ Calc I ─
    {"q": "Evaluate: lim(x→2) (x²−4)/(x−2)",
     "choices": ["A) 0", "B) 2", "C) 4", "D) DNE"],
     "answer": "C)", "topic": "Calc I — Limits & Continuity", "ch": "Stewart §2.3",
     "solution": "Factor: (x+2)(x−2)/(x−2) → x+2. At x=2: **4**."},
    {"q": "Evaluate: lim(x→0) sin(3x) / x",
     "choices": ["A) 0", "B) 1", "C) 3", "D) ∞"],
     "answer": "C)", "topic": "Calc I — Limits & Continuity", "ch": "Stewart §2.2",
     "solution": "Rewrite: 3·sin(3x)/(3x). As x→0: 3·1 = **3**. Uses lim(θ→0) sin(θ)/θ = 1."},
    {"q": "Find d/dx[x²·sin(x)]",
     "choices": ["A) 2x sin x", "B) x² cos x", "C) 2x sin x + x² cos x", "D) x² cos x − 2x sin x"],
     "answer": "C)", "topic": "Calc I — Derivatives & Rules", "ch": "Stewart §3.2",
     "solution": "Product rule: (x²)'sin x + x²(sin x)' = 2x sin x + x² cos x."},
    {"q": "Find dy/dx if y = ln(x² + 1)",
     "choices": ["A) 1/(x²+1)", "B) 2x/(x²+1)", "C) 2x·ln(x²+1)", "D) 1/(2x)"],
     "answer": "B)", "topic": "Calc I — Derivatives & Rules", "ch": "Stewart §3.6",
     "solution": "Chain rule: d/dx[ln(u)] = u'/u. Here u=x²+1, u'=2x. So dy/dx = **2x/(x²+1)**."},
    {"q": "The absolute maximum of f(x) = x³ − 3x on [−2, 2] is:",
     "choices": ["A) −2", "B) 2", "C) 0", "D) 4"],
     "answer": "B)", "topic": "Calc I — Applications of Derivatives", "ch": "Stewart §4.1",
     "solution": "f'=3x²−3=0 → x=±1. f(−2)=−2, f(−1)=2, f(1)=−2, f(2)=2. Max = **2**."},
    {"q": "∫₀² 3x² dx =",
     "choices": ["A) 6", "B) 8", "C) 4", "D) 12"],
     "answer": "B)", "topic": "Calc I — Integrals & FTC", "ch": "Stewart §5.3",
     "solution": "[x³]₀² = 8 − 0 = **8**."},
    {"q": "If G(x) = ∫₁ˣ √(t³+1) dt, then G'(2) =",
     "choices": ["A) 2", "B) 3", "C) √10", "D) 9"],
     "answer": "B)", "topic": "Calc I — Integrals & FTC", "ch": "Stewart §5.3",
     "solution": "FTC Part 1: G'(x) = √(x³+1). G'(2) = √(8+1) = √9 = **3**."},
    # ─ Calc II ─
    {"q": "∫ x ln(x) dx =",
     "choices": ["A) (ln x)²/2+C", "B) (x²/2)ln x − x²/4+C", "C) x ln x − x+C", "D) x²ln x+C"],
     "answer": "B)", "topic": "Calc II — Integration Techniques", "ch": "Stewart §7.1",
     "solution": "IBP: u=ln x, dv=x dx → du=dx/x, v=x²/2. Result: (x²/2)ln x − ∫(x/2)dx = **(x²/2)ln x − x²/4 + C**."},
    {"q": "∫ x·cos(x) dx =",
     "choices": ["A) x·sin(x) + cos(x) + C", "B) x·sin(x) − cos(x) + C",
                 "C) sin(x) + x·cos(x) + C", "D) −x·sin(x) + cos(x) + C"],
     "answer": "A)", "topic": "Calc II — Integration Techniques", "ch": "Stewart §7.1",
     "solution": "IBP: u=x, dv=cos(x)dx → du=dx, v=sin(x). Result: x sin(x) − ∫sin(x)dx = **x sin(x) + cos(x) + C**."},
    {"q": "Does Σ_{n=1}^∞ 1/n² converge?",
     "choices": ["A) No — p-series p=2<1", "B) No — harmonic series",
                 "C) Yes — p-series p=2>1", "D) Inconclusive"],
     "answer": "C)", "topic": "Calc II — Series & Convergence", "ch": "Stewart §11.3",
     "solution": "p-series Σ1/nᵖ converges iff p>1. p=2>1 → **converges** (sum = π²/6)."},
    {"q": "The ratio test on Σ n!/3ⁿ gives L =",
     "choices": ["A) 0", "B) 1/3", "C) ∞", "D) 1"],
     "answer": "C)", "topic": "Calc II — Series & Convergence", "ch": "Stewart §11.6",
     "solution": "|aₙ₊₁/aₙ| = (n+1)/3 → ∞. L>1 → **diverges**."},
    {"q": "The Maclaurin series for eˣ starts:",
     "choices": ["A) 1+x+x³/6+...", "B) x+x²+x³+...",
                 "C) 1+x+x²/2!+x³/3!+...", "D) x−x³/6+..."],
     "answer": "C)", "topic": "Calc II — Power & Taylor Series", "ch": "Stewart §11.10",
     "solution": "eˣ = **1 + x + x²/2! + x³/3! + ...** (option D is sin x)."},
    {"q": "Find the radius of convergence of Σ xⁿ/n!",
     "choices": ["A) R = 1", "B) R = 0", "C) R = ∞", "D) R = e"],
     "answer": "C)", "topic": "Calc II — Power & Taylor Series", "ch": "Stewart §11.8",
     "solution": "Ratio: |x|/(n+1) → 0 as n→∞ for all x. R = **∞**."},
    {"q": "Area enclosed by the cardioid r = 1 + cos θ is:",
     "choices": ["A) π", "B) 3π/2", "C) 2π", "D) π/2"],
     "answer": "B)", "topic": "Calc II — Parametric & Polar", "ch": "Stewart §10.4",
     "solution": "A = ½∫₋π^π (1+cosθ)² dθ = ½·3π = **3π/2**."},
    # ─ Calc III ─
    {"q": "∇f at (1,1) for f(x,y) = x²y + y³",
     "choices": ["A) ⟨2, 4⟩", "B) ⟨2, 1⟩", "C) ⟨1, 4⟩", "D) ⟨3, 4⟩"],
     "answer": "A)", "topic": "Calc III — Partial Derivatives", "ch": "Stewart §14.6",
     "solution": "fₓ=2xy=2, fy=x²+3y²=1+3=4. ∇f(1,1) = **⟨2, 4⟩**."},
    {"q": "Find the directional derivative of f(x,y) = x²y at (2,1) in direction ⟨3,4⟩.",
     "choices": ["A) 4", "B) 12/5", "C) 16/5", "D) 28/5"],
     "answer": "D)", "topic": "Calc III — Partial Derivatives", "ch": "Stewart §14.6",
     "solution": "∇f=⟨2xy,x²⟩=⟨4,4⟩. Unit vector: ⟨3/5,4/5⟩. D_u f = 4(3/5)+4(4/5) = 12/5+16/5 = **28/5**."},
    {"q": "∬_D (x²+y²) dA over disk r ≤ 2 in polar coordinates equals:",
     "choices": ["A) 4π", "B) 8π", "C) 16π", "D) 2π"],
     "answer": "B)", "topic": "Calc III — Multiple Integrals", "ch": "Stewart §15.3",
     "solution": "∫₀^{2π}∫₀² r²·r dr dθ = 2π·[r⁴/4]₀² = 2π·4 = **8π**."},
    {"q": "Green's theorem converts ∮_C P dx + Q dy into:",
     "choices": ["A) ∭_E (∇·F) dV", "B) ∬_D (∂Q/∂x−∂P/∂y) dA",
                 "C) ∬_S (∇×F)·dS", "D) A line integral over a larger curve"],
     "answer": "B)", "topic": "Calc III — Vector Calculus Theorems", "ch": "Stewart §16.4",
     "solution": "Green's: ∮_C P dx+Q dy = ∬_D **(∂Q/∂x−∂P/∂y) dA** (C positively oriented = CCW)."},
    {"q": "F(x,y) = ⟨2xy, x²+3y²⟩. Is F conservative?",
     "choices": ["A) No", "B) Yes — ∂P/∂y = ∂Q/∂x",
                 "C) Only on simply connected regions", "D) Cannot tell"],
     "answer": "B)", "topic": "Calc III — Vector Calculus Theorems", "ch": "Stewart §16.3",
     "solution": "∂P/∂y = 2x = ∂Q/∂x = 2x. Equal → **F is conservative**."},
    {"q": "By the Divergence Theorem, ∬_S F·dS for F=⟨x,y,z⟩ over the unit sphere equals:",
     "choices": ["A) π", "B) 2π", "C) 4π/3", "D) 4π"],
     "answer": "D)", "topic": "Calc III — Vector Calculus Theorems", "ch": "Stewart §16.9",
     "solution": "div F = 1+1+1 = 3. ∭_E 3 dV = 3·(4π/3) = **4π**."},
]
assert len(DIAGNOSTIC) == 20, f"Expected 20 questions, got {len(DIAGNOSTIC)}"

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

def plot_derivative(label="x²"):
    fig, ax = _fig()
    x = np.linspace(-3, 3, 400)
    y = x**2; a = 1.5; fa = a**2; m = 2*a
    tang = m*(x-a)+fa
    ax.plot(x, y, color="#f4c542", lw=2.5, label=f"f(x) = {label}")
    ax.plot(x, tang, color="#4fc3f7", lw=1.8, ls="--", label=f"Tangent at x={a}")
    ax.scatter([a], [fa], color="#f06292", s=80, zorder=5)
    ax.set_ylim(-1, 12); ax.legend(fontsize=9)
    ax.set_title("Derivative = Slope of Tangent Line", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_integral():
    fig, ax = _fig()
    x = np.linspace(0, 3, 400); y = x**2
    xf = np.linspace(0.5, 2.5, 300); yf = xf**2
    ax.fill_between(xf, yf, alpha=0.35, color="#f4c542", label="∫₀·₅²·⁵ x² dx")
    ax.plot(x, y, color="#f4c542", lw=2.5, label="f(x) = x²")
    ax.set_ylim(-0.5, 10); ax.legend(fontsize=9)
    ax.set_title("Definite Integral as Signed Area", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_series():
    fig, ax = _fig()
    ns = np.arange(1, 20); partial = np.cumsum(1/ns**2)
    ax.step(ns, partial, color="#f4c542", lw=2, where="post", label="Partial sum Sₙ")
    ax.axhline(np.pi**2/6, color="#4fc3f7", ls="--", lw=1.5, label=f"π²/6 ≈ {np.pi**2/6:.4f}")
    ax.set_xlabel("n"); ax.set_ylabel("Sₙ"); ax.legend(fontsize=9)
    ax.set_title("Series Convergence: Σ 1/n²", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_taylor():
    fig, ax = _fig()
    x = np.linspace(-np.pi, np.pi, 500)
    ax.plot(x, np.sin(x), color="#f4c542", lw=2.5, label="sin(x)")
    approx = np.zeros_like(x); colors = ["#4fc3f7","#81c784","#ffb74d","#f06292"]
    import math
    for k in range(4):
        n = 2*k+1; approx += ((-1)**k)*x**n/math.factorial(n)
        ax.plot(x, np.clip(approx,-3,3), color=colors[k], lw=1.5, ls="--", label=f"T{n}(x)")
    ax.set_ylim(-2.5, 2.5); ax.legend(fontsize=8)
    ax.set_title("Taylor Approximations of sin(x)", color="#f4c542", fontsize=11)
    return _save(fig)

def plot_gradient():
    fig, ax = _fig(7, 5)
    x = np.linspace(-2, 2, 20); y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y); F = X**2+Y**2
    cs = ax.contour(X, Y, F, levels=8, colors=["#f4c542"], alpha=0.5)
    ax.clabel(cs, fontsize=7, fmt="%.1f", colors="#e8eaf0")
    ax.quiver(X[::2,::2], Y[::2,::2], 2*X[::2,::2], 2*Y[::2,::2], color="#4fc3f7", alpha=0.85, scale=25)
    ax.set_title("Gradient Field ∇f for f(x,y)=x²+y²", color="#f4c542", fontsize=11)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return _save(fig)

def plot_results(area_scores: dict):
    fig, ax = _fig(7, 3)
    cats = list(area_scores.keys()); vals = list(area_scores.values())
    bars = ax.barh(cats, vals, color=["#f4c542" if v >= 0.6 else "#f06292" for v in vals], height=0.5)
    ax.set_xlim(0, 1); ax.set_xlabel("Score")
    ax.set_title("Diagnostic Results by Area", color="#f4c542", fontsize=11)
    for bar, val in zip(bars, vals):
        ax.text(val+0.02, bar.get_y()+bar.get_height()/2, f"{val*100:.0f}%",
                va="center", color="#e8eaf0", fontsize=9)
    return _save(fig)

PLOT_MAP = {
    "Calc I — Derivatives & Rules": plot_derivative,
    "Calc I — Applications of Derivatives": lambda: plot_derivative("x³−3x"),
    "Calc I — Integrals & FTC": plot_integral,
    "Calc II — Series & Convergence": plot_series,
    "Calc II — Power & Taylor Series": plot_taylor,
    "Calc III — Partial Derivatives": plot_gradient,
}

# ── Pathway generator ─────────────────────────────────────────────────────────
DAYS_LEFT = max(0, (date(2026, 6, 21) - date.today()).days)

def generate_pathway(scores: dict) -> str:
    areas = {"calc1": [], "calc2": [], "calc3": []}
    for t, s in scores.items():
        areas[TOPICS[t]["area"]].append(s)
    avg = {k: (sum(v)/len(v) if v else 0) for k, v in areas.items()}
    md = f"## 📍 Your USNA Validation Pathway\n\n**{DAYS_LEFT} days until June 21 — I-Day is June 25.**\n\n"
    md += "### Performance by Area\n"
    for area, label in [("calc1","Calculus I"),("calc2","Calculus II"),("calc3","Calculus III")]:
        a = avg[area]; bar = "█"*int(a*10)+"░"*(10-int(a*10))
        st = "✅ Strong" if a>=0.7 else ("⚠️ Review" if a>=0.4 else "🔴 Focus Here")
        md += f"- **{label}:** {bar} {a*100:.0f}%  {st}\n"
    md += "\n### Recommended Plan\n"
    md += ("- **Week 1 (Jun 2–7): 🔴 Calc I** — Ch 2–5 Stewart. Limits, derivatives, FTC. (~70% pass rate)\n"
           if avg["calc1"] < 0.6 else
           "- **Week 1:** ✅ Calc I solid — quick review then shift to Calc II integration (Ch 7).\n")
    md += ("- **Week 2 (Jun 8–14): 🔴 Calc II** — IBP, partial fractions, series + Taylor.\n"
           if avg["calc2"] < 0.6 else
           "- **Week 2:** ✅ Calc II looking good. Start Calc III vectors and partial derivatives.\n")
    md += ("- **Week 3 (Jun 15–21): 🔴 Calc III** — Green's, Stokes, Divergence. Free-response practice.\n"
           if avg["calc3"] < 0.6 else
           "- **Week 3:** ✅ Calc III solid. Full timed practice exams.\n")
    weak = [t for t, s in scores.items() if s < 0.5]
    if weak:
        md += "\n### ⚡ Immediate Focus\n" + "".join(f"- {t} ({TOPICS[t]['ch']})\n" for t in weak)
    return md

# ── Build results HTML from answers ──────────────────────────────────────────
def build_results(answers: dict) -> tuple:
    """Returns (results_html, score_tuple, area_scores_dict)."""
    correct_count = 0
    html_parts = []
    topic_hits = {}
    topic_total = {}
    for i, q in enumerate(DIAGNOSTIC):
        chosen = answers.get(i, "")
        correct = q["answer"]
        is_right = (chosen.startswith(correct) if chosen else False)
        if is_right:
            correct_count += 1
        t = q["topic"]
        topic_total[t] = topic_total.get(t, 0) + 1
        topic_hits[t] = topic_hits.get(t, 0) + (1 if is_right else 0)

        icon = "✅" if is_right else "❌"
        box_class = "correct-box" if is_right else "wrong-box"
        chosen_txt = chosen if chosen else "(no answer)"
        sol_block = (f'<div class="solution-text"><b>Solution:</b> {q["solution"]}</div>' if not is_right else
                     f'<div class="solution-text" style="opacity:0.7"><b>Correct!</b> {q["solution"]}</div>')
        html_parts.append(
            f'<div class="q-block">'
            f'<div class="q-label">Q{i+1} · {q["topic"]} · {q["ch"]}</div>'
            f'<div style="color:#f0ebe0;margin-bottom:8px">{q["q"]}</div>'
            f'<div class="{box_class}">{icon} Your answer: <b>{chosen_txt}</b> &nbsp;·&nbsp; Correct: <b>{correct}</b></div>'
            f'{sol_block}</div>'
        )

    scores = {t: topic_hits.get(t, 0)/topic_total[t] for t in topic_total}
    pct = correct_count / 20 * 100
    color = "#28c864" if pct >= 70 else ("#f4c542" if pct >= 50 else "#ff5050")

    banner = (f'<div class="score-banner">'
              f'<div style="font-family:Georgia,serif;font-size:3rem;font-weight:700;color:{color}">'
              f'{correct_count} / 20</div>'
              f'<div style="color:rgba(232,234,240,0.6);margin-top:6px">{pct:.0f}% correct</div>'
              f'<div style="color:rgba(232,234,240,0.4);font-size:0.8rem;margin-top:4px">'
              f'USNA target: Calc I Day 1–2 · Calc II Week 2 · Calc III Week 2–3</div>'
              f'</div>')
    full_html = banner + DIVIDER + "\n".join(html_parts)

    area_scores = {}
    for t, sc in scores.items():
        a = TOPICS[t]["area"]
        area_scores[a] = area_scores.get(a, []) + [sc]
    area_avg = {"Calc I": sum(v)/len(v) if v else 0
                for a, v in area_scores.items()
                for _ in [(None,)]
                if a == "calc1"}
    area_avg_full = {
        "Calc I":   sum(area_scores.get("calc1",[])) / len(area_scores.get("calc1",[1])),
        "Calc II":  sum(area_scores.get("calc2",[])) / len(area_scores.get("calc2",[1])),
        "Calc III": sum(area_scores.get("calc3",[])) / len(area_scores.get("calc3",[1])),
    }
    return full_html, scores, area_avg_full

# ── Gradio app ────────────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="FissionLab Math — Dr. Preston PhD") as demo:

    gr.HTML("""<div style="background:rgba(201,168,76,0.08);border-bottom:1px solid rgba(201,168,76,0.2);
    padding:16px 24px;border-radius:12px;margin-bottom:16px;display:flex;align-items:center;gap:14px">
    <span style="font-size:2.2rem">📐</span>
    <div>
      <div style="font-family:Georgia,serif;font-size:1.4rem;font-weight:700;color:#f4c542">
        FissionLab Math — USNA Calculus Prep</div>
      <div style="font-size:0.82rem;color:rgba(232,234,240,0.5)">
        Dr. P · Calc I–III · Stewart Early Transcendentals · 20-question diagnostic</div>
    </div></div>""")

    with gr.Tabs():

        # ── TAB 1: DIAGNOSTIC ────────────────────────────────────────────────
        with gr.Tab("🎯 Diagnostic"):
            diag_state = gr.State({"page": 0, "answers": {}})

            # Intro
            with gr.Column(visible=True) as intro_col:
                gr.HTML("""<div style="text-align:center;padding:32px 20px">
                <h2 style="font-family:Georgia,serif;color:#f4c542;margin-bottom:12px">20-Question Diagnostic</h2>
                <p style="color:rgba(232,234,240,0.7);max-width:500px;margin:0 auto 24px">
                7 Calc I · 7 Calc II · 6 Calc III · Aligned with Stewart Early Transcendentals<br>
                10 questions at a time · Solutions revealed at the end only</p></div>""")
                start_btn = gr.Button("▶ Begin Diagnostic", variant="primary", size="lg")

            # Page 1: Q1-10
            with gr.Column(visible=False) as page1_col:
                gr.HTML('<div style="font-family:Georgia,serif;font-size:1.2rem;color:#f4c542;'
                        'border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:16px">'
                        'Questions 1–10 of 20</div>')
                radios_p1 = []
                for i, q in enumerate(DIAGNOSTIC[:10]):
                    gr.HTML(f'<div class="q-block"><div class="q-label">Q{i+1} · {q["ch"]}</div>'
                            f'<div style="color:#f0ebe0;font-size:0.96rem;margin-bottom:8px">{q["q"]}</div>'
                            f'<div class="q-tag">Topic: {q["topic"]} · USNA: Calc {q["topic"][5:6] if "Calc" in q["topic"] else "?"}</div></div>')
                    r = gr.Radio(choices=q["choices"], label="Your answer:", value=None, interactive=True)
                    radios_p1.append(r)
                next_btn = gr.Button("Next: Questions 11–20 →", variant="primary")

            # Page 2: Q11-20
            with gr.Column(visible=False) as page2_col:
                gr.HTML('<div style="font-family:Georgia,serif;font-size:1.2rem;color:#f4c542;'
                        'border-bottom:1px solid rgba(201,168,76,0.3);padding-bottom:8px;margin-bottom:16px">'
                        'Questions 11–20 of 20</div>')
                radios_p2 = []
                for i, q in enumerate(DIAGNOSTIC[10:]):
                    gr.HTML(f'<div class="q-block"><div class="q-label">Q{i+11} · {q["ch"]}</div>'
                            f'<div style="color:#f0ebe0;font-size:0.96rem;margin-bottom:8px">{q["q"]}</div>'
                            f'<div class="q-tag">Topic: {q["topic"]}</div></div>')
                    r = gr.Radio(choices=q["choices"], label="Your answer:", value=None, interactive=True)
                    radios_p2.append(r)
                submit_btn = gr.Button("Submit &amp; See Results →", variant="primary")

            # Results
            with gr.Column(visible=False) as results_col:
                results_html = gr.HTML("")
                pathway_md   = gr.Markdown("")
                results_img  = gr.Image(label="Performance Chart", visible=False, type="pil")
                concept_imgs = [gr.Image(label="", visible=False, type="pil") for _ in range(3)]
                restart_btn  = gr.Button("↺ Restart Diagnostic", variant="secondary")

        # ── TAB 2: TOPIC GUIDE ───────────────────────────────────────────────
        with gr.Tab("📚 Topic Guide"):
            topic_dd  = gr.Dropdown(choices=list(TOPICS.keys()), label="Select Topic",
                                    value=list(TOPICS.keys())[0])
            topic_out = gr.HTML("")
            topic_img = gr.Image(label="Visualization", visible=False, type="pil")

            def load_topic(topic):
                html = TOPIC_HTML.get(topic, "<p>No content yet.</p>")
                fn = PLOT_MAP.get(topic)
                if fn:
                    try:
                        img = fn()
                        return gr.update(value=html), gr.update(visible=True, value=img)
                    except Exception:
                        pass
                return gr.update(value=html), gr.update(visible=False)

            topic_dd.change(load_topic, [topic_dd], [topic_out, topic_img])
            demo.load(load_topic, [topic_dd], [topic_out, topic_img])

        # ── TAB 3: STUDY PLAN ────────────────────────────────────────────────
        with gr.Tab("📅 Study Plan"):
            gr.Markdown(f"### USNA Validation Study Plan — {DAYS_LEFT} days until June 21\n\n"
                "**Exam timeline:** Calc I Day 1–2 · Calc II Week 2 (MC only) · Calc III Week 2–3 (MC + free response)\n\n"
                "---\n\n"
                "**Week 1: June 2–7 — Calculus I Mastery** *(~70% pass rate — front-load this)*\n"
                "- Mon: Stewart Ch 2 — Limits (direct sub, factor/cancel, L'Hôpital, squeeze theorem)\n"
                "- Tue: Stewart Ch 3 — Power, product, quotient, chain rules. Drill until automatic.\n"
                "- Wed: Stewart Ch 3 — Trig/exp/log derivatives. Implicit differentiation.\n"
                "- Thu: Stewart Ch 4 — Optimization + related rates (most tested applications)\n"
                "- Fri: Stewart Ch 5 — FTC Parts 1 & 2, u-substitution\n"
                "- Sat: **Mock Calc I** — 10 timed problems. Review all misses.\n"
                "- Sun: Light review / rest\n\n"
                "**Week 2: June 8–14 — Calculus II** *(MC only at USNA)*\n"
                "- Mon: Stewart Ch 7 — Integration by parts (LIATE). Drill ∫x·cos(x), ∫x·ln(x).\n"
                "- Tue: Stewart Ch 7 — Trig integrals + trig substitution\n"
                "- Wed: Stewart Ch 7 — Partial fractions (make sure deg num < deg denom)\n"
                "- Thu: Stewart Ch 11 — Sequences, series, divergence test, geometric/p-series\n"
                "- Fri: Stewart Ch 11 — Integral, comparison, ratio, AST tests\n"
                "- Sat: Stewart Ch 11 — Power series, Taylor/Maclaurin (memorize eˣ, sin, cos, 1/(1-x))\n"
                "- Sun: **Mock Calc II** — timed MC practice\n\n"
                "**Week 3: June 15–20 — Calculus III** *(Hardest exam — MC + free response)*\n"
                "- Mon: Stewart Ch 12 — Vectors, dot/cross products, lines & planes in 3D\n"
                "- Tue: Stewart Ch 14 — Partial derivatives, gradient, directional derivative, tangent plane\n"
                "- Wed: Stewart Ch 14 — 2nd derivative test, Lagrange multipliers\n"
                "- Thu: Stewart Ch 15 — Double/triple integrals (switch to polar/cylindrical/spherical)\n"
                "- Fri: Stewart Ch 16 — Line integrals, conservative fields, Green's theorem\n"
                "- Sat: Stewart Ch 16 — Stokes' + Divergence theorem. **Free-response practice.**\n\n"
                "**June 21: Final Review Day** — Full 20-question diagnostic + targeted weak-area drill\n\n"
                "---\n*Daily minimum: 30 min concept → 30 min problems → 15 min review wrong answers.*")

        # ── TAB 4: UNLOCK ────────────────────────────────────────────────────
        with gr.Tab("🔑 Unlock"):
            gr.Markdown("## Unlock Full Access\nEnter your FissionLab token.")
            tok_in  = gr.Textbox(label="Token", placeholder="FLAB-XXXX-XXXX-XXXX")
            tok_btn = gr.Button("Verify Token", variant="primary")
            tok_out = gr.Markdown("")
            gr.Markdown("No token? Contact **Dr_PrestonD@proton.me**")

            def verify_action(token, s):
                if verify_token(token):
                    s["verified"] = True
                    return s, "✅ **Premium access unlocked!**"
                return s, "❌ Invalid token. Contact Dr. Preston."
            tok_btn.click(verify_action, [tok_in, diag_state], [diag_state, tok_out])

    gr.HTML("<div style='text-align:center;color:#8fa8c8;font-size:0.78rem;padding:16px 0'>Dr. Preston · PhD · FissionLab · Stewart Early Transcendentals 8e</div>")

    # ── Diagnostic wiring ────────────────────────────────────────────────────
    def on_start(s):
        s = {"page": 1, "answers": {}}
        return s, gr.update(visible=False), gr.update(visible=True), gr.update(visible=False), gr.update(visible=False)

    def on_next(s, *radio_vals):
        answers = dict(s.get("answers", {}))
        for i, v in enumerate(radio_vals):
            if v is not None:
                answers[i] = v
        s = {"page": 2, "answers": answers}
        return s, gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=False)

    def on_submit(s, *radio_vals):
        answers = dict(s.get("answers", {}))
        for i, v in enumerate(radio_vals):
            if v is not None:
                answers[i + 10] = v
        s = {"page": 3, "answers": answers}

        results_htm, scores, area_avg = build_results(answers)
        pathway = generate_pathway(scores)

        try:
            chart = plot_results(area_avg)
        except Exception:
            chart = None

        weak_topics = [t for t, sc in scores.items() if sc < 0.5]
        concept_figs = []
        for t in weak_topics[:3]:
            fn = PLOT_MAP.get(t)
            if fn:
                try:
                    concept_figs.append(fn())
                except Exception:
                    concept_figs.append(None)
            else:
                concept_figs.append(None)

        while len(concept_figs) < 3:
            concept_figs.append(None)

        return (s,
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=True),
                gr.update(value=results_htm),
                gr.update(value=pathway),
                gr.update(visible=(chart is not None), value=chart),
                gr.update(visible=(concept_figs[0] is not None), value=concept_figs[0]),
                gr.update(visible=(concept_figs[1] is not None), value=concept_figs[1]),
                gr.update(visible=(concept_figs[2] is not None), value=concept_figs[2]))

    def on_restart(s):
        s = {"page": 0, "answers": {}}
        return s, gr.update(visible=True), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False)

    col_outs = [diag_state, intro_col, page1_col, page2_col, results_col]
    start_btn.click(on_start, [diag_state], col_outs)
    next_btn.click(on_next, [diag_state] + radios_p1, col_outs)
    submit_btn.click(on_submit, [diag_state] + radios_p2,
                     col_outs + [results_html, pathway_md, results_img] + concept_imgs)
    restart_btn.click(on_restart, [diag_state], col_outs)

if __name__ == "__main__":
    demo.launch()
