"""
FissionLab Math Practice — USNA Calculus I-III
Dr. Preston PhD · Stewart Early Transcendentals 8e
20-question diagnostic · 10 at a time · Solutions revealed at end only
"""
import io, base64, re
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
    'deriv_def':  r'\frac{d}{dx}f = \lim_{h\to 0}\frac{f(x+h)-f(x)}{h}',
    'power':      r'\frac{d}{dx}[x^n] = nx^{n-1}',
    'product':    r'(fg)^\prime = f^\prime g + fg^\prime',
    'quotient':   r'\left(\frac{f}{g}\right)^\prime = \frac{f^\prime g - fg^\prime}{g^2}',
    'chain':      r'\frac{d}{dx}[f(g(x))] = f^\prime(g(x))\cdot g^\prime(x)',
    'lhopital':   r'\lim_{x\to a}\frac{f(x)}{g(x)} = \lim_{x\to a}\frac{f^\prime(x)}{g^\prime(x)}\quad\bigl(\tfrac{0}{0}\text{ or }\tfrac{\infty}{\infty}\bigr)',
    'ftc1':       r'\frac{d}{dx}\int_a^x f(t)\,dt = f(x)',
    'ftc2':       r'\int_a^b f(x)\,dx = F(b) - F(a)',
    'power_int':  r'\int x^n\,dx = \frac{x^{n+1}}{n+1}+C\quad(n\neq -1)',
    'ibp':        r'\int u\,dv = uv - \int v\,du\quad\text{(LIATE order for }u)',
    'p_series':   r'\sum_{n=1}^{\infty}\frac{1}{n^p}\;\text{converges iff }p > 1',
    'ratio':      r'L = \lim_{n\to\infty}\!\left|\frac{a_{n+1}}{a_n}\right|;\;L<1\Rightarrow\text{converges}',
    'taylor':     r'f(x) = \sum_{n=0}^{\infty}\frac{f^{(n)}(a)}{n!}(x-a)^n',
    'mac_e':      r'e^x = \sum_{n=0}^{\infty}\frac{x^n}{n!} = 1+x+\frac{x^2}{2!}+\cdots',
    'mac_sin':    r'\sin x = x - \frac{x^3}{3!} + \frac{x^5}{5!} - \cdots',
    'mac_cos':    r'\cos x = 1 - \frac{x^2}{2!} + \frac{x^4}{4!} - \cdots',
    'gradient':   r'\nabla f = \frac{\partial f}{\partial x}\hat{i}+\frac{\partial f}{\partial y}\hat{j}+\frac{\partial f}{\partial z}\hat{k}',
    'dir_deriv':  r'D_{\hat{u}}f = \nabla f\cdot\hat{u}',
    'greens':     r'\oint_C P\,dx+Q\,dy = \iint_D\!\!\left(\frac{\partial Q}{\partial x}-\frac{\partial P}{\partial y}\right)dA',
    'stokes':     r'\oint_C \mathbf{F}\cdot d\mathbf{r} = \iint_S(\nabla\times\mathbf{F})\cdot d\mathbf{S}',
    'divthm':     r'\iint_S \mathbf{F}\cdot d\mathbf{S} = \iiint_E(\nabla\cdot\mathbf{F})\,dV',
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
    "Calc I — Limits": _sec("Limits &amp; Continuity · Stewart Ch 2",
        "Direct substitution first. If 0/0 or ∞/∞: factor/cancel, then L'Hôpital, then squeeze.<br>"
        "Critical: lim(x→0) sin x/x = <b>1</b> · lim(x→0)(1−cos x)/x = <b>0</b> · lim(x→∞)(1+1/x)ˣ = <b>e</b><br>"
        "Continuity at a: f(a) defined, limit exists, they're equal.<br>"
        '<div class="tip-box"><strong>Trap:</strong> L\'Hôpital applies ONLY to 0/0 or ±∞/±∞.</div>',
        ['lhopital']),
    "Calc I — Derivatives": _sec("Differentiation Rules · Stewart Ch 3",
        "<b>Trig:</b> (sin x)′=cos x · (cos x)′=−sin x · (tan x)′=sec²x<br>"
        "<b>Exp/Log:</b> (eˣ)′=eˣ · (ln x)′=1/x · (arctan x)′=1/(1+x²)<br>"
        '<div class="tip-box"><strong>Most tested:</strong> Chain rule — never skip it inside trig/exp/log.</div>',
        ['deriv_def','power','product','quotient','chain']),
    "Calc I — Applications": _sec("Applications · Stewart Ch 4",
        "<b>Optimization:</b> f′(x)=0 → critical pts → 2nd deriv test or closed interval check.<br>"
        "<b>Related rates:</b> write equation → differentiate w.r.t. t → substitute last.<br>"
        "<b>L'Hôpital:</b> indeterminate 0/0 or ∞/∞ only.", []),
    "Calc I — Integrals & FTC": _sec("Integration &amp; FTC · Stewart Ch 5",
        "∫xⁿdx = xⁿ⁺¹/(n+1)+C · ∫1/x dx = ln|x|+C · ∫eˣdx = eˣ+C<br>"
        "∫sin x dx = −cos x+C · ∫cos x dx = sin x+C · ∫sec²x dx = tan x+C<br>"
        "<b>u-sub:</b> u=g(x), du=g′(x)dx — reverse chain rule.<br>"
        "<b>Chain+FTC:</b> d/dx[∫ₐᵍ⁽ˣ⁾f(t)dt] = f(g(x))·g′(x)",
        ['ftc1','ftc2','power_int']),
    "Calc II — Integration Techniques": _sec("Integration Techniques · Stewart Ch 7",
        "<b>IBP LIATE:</b> Log → Inv trig → Algebraic → Trig → Exponential<br>"
        "<b>Trig sub:</b> √(a²−x²)→x=a sinθ · √(a²+x²)→x=a tanθ · √(x²−a²)→x=a secθ<br>"
        "<b>Partial fractions:</b> factor denominator, write A/(ax+b)+B/(cx+d). Degree check first.<br>"
        "<b>p-integral:</b> ∫₁^∞ 1/xᵖ converges iff p>1.", ['ibp']),
    "Calc II — Series": _sec("Infinite Series · Stewart Ch 11",
        "<b>Tests:</b> Divergence → Geometric → p-series → Integral → Comparison → Ratio → AST<br>"
        "<b>Geometric:</b> Σarⁿ converges iff |r|<1; sum=a/(1−r).<br>"
        '<div class="tip-box"><strong>Trap:</strong> Divergence test only proves divergence. '
        'Ratio test inconclusive when L=1.</div>',
        ['p_series','ratio']),
    "Calc II — Taylor Series": _sec("Power &amp; Taylor Series · Stewart Ch 11",
        "<b>Radius R:</b> use ratio test. Converges on (a−R, a+R).<br>"
        "<b>Memorize:</b> 1/(1−x)=Σxⁿ (|x|<1) · ln(1+x)=x−x²/2+… · arctan x=x−x³/3+…",
        ['taylor','mac_e','mac_sin','mac_cos']),
    "Calc III — Vectors": _sec("Vectors &amp; 3D Geometry · Stewart Ch 12",
        "<b>Dot:</b> u·v=|u||v|cosθ. Perp ↔ u·v=0.<br>"
        "<b>Cross:</b> |u×v|=|u||v|sinθ (area of parallelogram). Not commutative.<br>"
        "<b>Line:</b> r(t)=r₀+td · <b>Plane:</b> n·(r−r₀)=0", []),
    "Calc III — Partial Derivatives": _sec("Partial Derivatives · Stewart Ch 14",
        "<b>∂f/∂x:</b> differentiate w.r.t. x, hold all other vars constant.<br>"
        "<b>2nd deriv test:</b> D=fₓₓfyy−fₓy². D>0,fₓₓ>0→min; D>0,fₓₓ<0→max; D<0→saddle.",
        ['gradient','dir_deriv']),
    "Calc III — Multiple Integrals": _sec("Multiple Integrals · Stewart Ch 15",
        "<b>Double:</b> ∬_D f dA — Fubini: switch order when needed.<br>"
        "<b>Polar:</b> dA=r dr dθ. <b>Cylindrical:</b> dV=r dz dr dθ. <b>Spherical:</b> dV=ρ²sinφ dρ dφ dθ", []),
    "Calc III — Theorems": _sec("Vector Calculus Theorems · Stewart Ch 16",
        "<b>Conservative:</b> F=∇f ↔ curl F=0 ↔ path independent.<br>"
        "<b>Pattern:</b> FTC → Green's (2D) → Stokes (3D curve→surface) → Divergence (surface→volume)",
        ['greens','stokes','divthm']),
}

# ── 20 Pre-generated questions (fixed, no shuffle) ────────────────────────────
QUESTIONS = [
    {"n":1,"area":"Calc I","text":"Evaluate: lim(x→2) (x²−4)/(x−2)",
     "choices":["A) 0","B) 2","C) 4","D) DNE"],"ans":"C)","ch":"Stewart §2.3",
     "sol":"Factor: (x+2)(x−2)/(x−2) = x+2. At x=2: <b>4</b>."},
    {"n":2,"area":"Calc I","text":"Evaluate: lim(x→0) sin(3x)/x",
     "choices":["A) 0","B) 1","C) 3","D) ∞"],"ans":"C)","ch":"Stewart §2.2",
     "sol":"3·sin(3x)/(3x) → 3·1 = <b>3</b>. Uses lim(θ→0) sinθ/θ = 1."},
    {"n":3,"area":"Calc I","text":"Find d/dx [x²·sin(x)]",
     "choices":["A) 2x sin x","B) x² cos x","C) 2x sin x + x² cos x","D) x² cos x − 2x sin x"],
     "ans":"C)","ch":"Stewart §3.2","sol":"Product rule: 2x sin x + x² cos x."},
    {"n":4,"area":"Calc I","text":"Find dy/dx if y = ln(x² + 1)",
     "choices":["A) 1/(x²+1)","B) 2x/(x²+1)","C) 2x ln(x²+1)","D) 1/(2x)"],
     "ans":"B)","ch":"Stewart §3.6","sol":"Chain rule: d/dx[ln u]=u′/u. u=x²+1, u′=2x → <b>2x/(x²+1)</b>."},
    {"n":5,"area":"Calc I","text":"Absolute maximum of f(x)=x³−3x on [−2,2]:",
     "choices":["A) −2","B) 0","C) 2","D) 4"],"ans":"C)","ch":"Stewart §4.1",
     "sol":"f′=3x²−3=0→x=±1. f(−2)=−2, f(−1)=2, f(1)=−2, f(2)=2. Max = <b>2</b>."},
    {"n":6,"area":"Calc I","text":"Evaluate: ∫₀² 3x² dx",
     "choices":["A) 6","B) 8","C) 4","D) 12"],"ans":"B)","ch":"Stewart §5.3",
     "sol":"FTC: [x³]₀² = 8 − 0 = <b>8</b>."},
    {"n":7,"area":"Calc I","text":"If G(x)=∫₁ˣ √(t³+1) dt, then G′(2)=",
     "choices":["A) 2","B) 3","C) √10","D) 9"],"ans":"B)","ch":"Stewart §5.3",
     "sol":"FTC Part 1: G′(x)=√(x³+1). G′(2)=√9 = <b>3</b>."},
    {"n":8,"area":"Calc II","text":"Evaluate: ∫ x ln(x) dx",
     "choices":["A) (ln x)²/2+C","B) (x²/2) ln x − x²/4+C","C) x ln x − x+C","D) x² ln x+C"],
     "ans":"B)","ch":"Stewart §7.1",
     "sol":"IBP: u=ln x, dv=x dx. Result: <b>(x²/2) ln x − x²/4 + C</b>."},
    {"n":9,"area":"Calc II","text":"Evaluate: ∫ x·cos(x) dx",
     "choices":["A) x sin x + cos x + C","B) x sin x − cos x + C","C) sin x + x cos x + C","D) −x sin x + cos x + C"],
     "ans":"A)","ch":"Stewart §7.1",
     "sol":"IBP: u=x, dv=cos x dx. Result: x sin x − ∫sin x dx = <b>x sin x + cos x + C</b>."},
    {"n":10,"area":"Calc II","text":"Does Σ(n=1 to ∞) 1/n² converge?",
     "choices":["A) No — p=2<1","B) No — harmonic","C) Yes — p-series p=2>1","D) Inconclusive"],
     "ans":"C)","ch":"Stewart §11.3","sol":"p-series Σ1/nᵖ converges iff p>1. p=2>1 → <b>converges</b>."},
    {"n":11,"area":"Calc II","text":"Ratio test on Σ n!/3ⁿ gives L =",
     "choices":["A) 0","B) 1/3","C) ∞","D) 1"],"ans":"C)","ch":"Stewart §11.6",
     "sol":"|a_{n+1}/a_n|=(n+1)/3→∞. L>1 → <b>diverges</b>."},
    {"n":12,"area":"Calc II","text":"Maclaurin series for eˣ starts:",
     "choices":["A) 1+x+x³/6+…","B) x+x²+x³+…","C) 1+x+x²/2!+x³/3!+…","D) x−x³/6+…"],
     "ans":"C)","ch":"Stewart §11.10","sol":"eˣ = <b>1+x+x²/2!+x³/3!+…</b> (D is sin x)."},
    {"n":13,"area":"Calc II","text":"Radius of convergence of Σ xⁿ/n!",
     "choices":["A) R=1","B) R=0","C) R=∞","D) R=e"],"ans":"C)","ch":"Stewart §11.8",
     "sol":"Ratio: |x|/(n+1)→0 for all x. R = <b>∞</b>. (This is eˣ.)"},
    {"n":14,"area":"Calc II","text":"Area between y=x² and y=x:",
     "choices":["A) 1/6","B) 1/3","C) 1/2","D) 1/4"],"ans":"A)","ch":"Stewart §6.1",
     "sol":"∫₀¹(x−x²)dx = [x²/2−x³/3]₀¹ = 1/2−1/3 = <b>1/6</b>."},
    {"n":15,"area":"Calc III","text":"∇f at (1,1) for f(x,y)=x²y+y³:",
     "choices":["A) ⟨2,4⟩","B) ⟨2,1⟩","C) ⟨1,4⟩","D) ⟨3,4⟩"],"ans":"A)","ch":"Stewart §14.6",
     "sol":"fₓ=2xy=2, fy=x²+3y²=4. ∇f(1,1) = <b>⟨2,4⟩</b>."},
    {"n":16,"area":"Calc III","text":"Directional derivative of f=x²y at (2,1) in direction ⟨3,4⟩:",
     "choices":["A) 4","B) 12/5","C) 16/5","D) 28/5"],"ans":"D)","ch":"Stewart §14.6",
     "sol":"∇f=⟨4,4⟩. Unit: ⟨3/5,4/5⟩. D_u f=4(3/5)+4(4/5) = <b>28/5</b>."},
    {"n":17,"area":"Calc III","text":"∬_D(x²+y²) dA over disk r≤2 in polar coords:",
     "choices":["A) 4π","B) 8π","C) 16π","D) 2π"],"ans":"B)","ch":"Stewart §15.3",
     "sol":"∫₀²π∫₀² r³ dr dθ = 2π·[r⁴/4]₀² = 2π·4 = <b>8π</b>."},
    {"n":18,"area":"Calc III","text":"Green's theorem converts ∮_C P dx+Q dy into:",
     "choices":["A) ∭_E(∇·F)dV","B) ∬_D(∂Q/∂x−∂P/∂y)dA","C) ∬_S(∇×F)·dS","D) A surface integral"],
     "ans":"B)","ch":"Stewart §16.4","sol":"Green's: ∮_C = ∬_D <b>(∂Q/∂x−∂P/∂y)dA</b>."},
    {"n":19,"area":"Calc III","text":"F=⟨2xy, x²+3y²⟩. Is F conservative?",
     "choices":["A) No","B) Yes — ∂P/∂y=∂Q/∂x","C) Only on simply connected regions","D) Cannot tell"],
     "ans":"B)","ch":"Stewart §16.3","sol":"∂P/∂y=2x=∂Q/∂x=2x → <b>conservative</b>."},
    {"n":20,"area":"Calc III","text":"Divergence Theorem: ∬_S F·dS for F=⟨x,y,z⟩ over unit sphere:",
     "choices":["A) π","B) 2π","C) 4π/3","D) 4π"],"ans":"D)","ch":"Stewart §16.9",
     "sol":"div F=3. ∭_E 3 dV=3·(4π/3) = <b>4π</b>."},
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

def _plt_deriv():
    fig, ax = _mkfig()
    x = np.linspace(-2.5, 2.5, 400); a = 1.5
    ax.plot(x, x**2, color="#c9a84c", lw=2.5, label="f(x)=x²")
    ax.plot(x, 2*a*(x-a)+a**2, color="#4fc3f7", lw=1.8, ls="--", label=f"Tangent at x={a}")
    ax.scatter([a], [a**2], color="#ff6b6b", s=80, zorder=5)
    ax.set_ylim(-0.5, 8); ax.legend(fontsize=9)
    ax.set_title("Derivative = Slope of Tangent Line", color="#c9a84c", fontsize=11)
    return _topil(fig)

def _plt_integral():
    fig, ax = _mkfig()
    x = np.linspace(0, 2.5, 400)
    xf = np.linspace(0.5, 2.0, 300)
    ax.fill_between(xf, xf**2, alpha=0.35, color="#c9a84c", label="∫ x² dx")
    ax.plot(x, x**2, color="#c9a84c", lw=2.5, label="f(x)=x²")
    ax.set_ylim(-0.3, 6); ax.legend(fontsize=9)
    ax.set_title("Definite Integral as Signed Area", color="#c9a84c", fontsize=11)
    return _topil(fig)

def _plt_series():
    fig, ax = _mkfig()
    ns = np.arange(1, 25); ps = np.cumsum(1/ns**2)
    ax.step(ns, ps, color="#c9a84c", lw=2, where="post", label="Partial sum Sₙ")
    ax.axhline(np.pi**2/6, color="#4fc3f7", ls="--", lw=1.5, label=f"π²/6≈{np.pi**2/6:.4f}")
    ax.set_xlabel("n"); ax.set_ylabel("Sₙ"); ax.legend(fontsize=9)
    ax.set_title("Convergence of Σ 1/n²", color="#c9a84c", fontsize=11)
    return _topil(fig)

def _plt_taylor():
    import math
    fig, ax = _mkfig()
    x = np.linspace(-np.pi, np.pi, 500)
    ax.plot(x, np.sin(x), color="#c9a84c", lw=2.5, label="sin(x)")
    ap = np.zeros_like(x)
    for k, c in enumerate(["#4fc3f7","#81c784","#ffb74d","#f06292"]):
        n = 2*k+1; ap += ((-1)**k)*x**n/math.factorial(n)
        ax.plot(x, np.clip(ap,-3,3), color=c, lw=1.5, ls="--", label=f"T{n}(x)")
    ax.set_ylim(-2.5, 2.5); ax.legend(fontsize=8)
    ax.set_title("Taylor Approximations of sin(x)", color="#c9a84c", fontsize=11)
    return _topil(fig)

def _plt_gradient():
    fig, ax = _mkfig(7, 5)
    x = np.linspace(-2, 2, 18); y = np.linspace(-2, 2, 18)
    X, Y = np.meshgrid(x, y)
    cs = ax.contour(X, Y, X**2+Y**2, levels=8, colors=["#c9a84c"], alpha=0.5)
    ax.clabel(cs, fontsize=7, fmt="%.1f", colors="#e8eaf0")
    ax.quiver(X[::2,::2], Y[::2,::2], 2*X[::2,::2], 2*Y[::2,::2], color="#4fc3f7", alpha=0.85, scale=25)
    ax.set_title("Gradient Field ∇f for f(x,y)=x²+y²", color="#c9a84c", fontsize=11)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    return _topil(fig)

def _plt_results(c1, c2, c3):
    fig, ax = _mkfig(7, 2.5)
    vals = [c1, c2, c3]; cats = ["Calc I (7Q)", "Calc II (7Q)", "Calc III (6Q)"]
    bars = ax.barh(cats, vals, color=["#c9a84c" if v>=0.6 else "#ff5050" for v in vals], height=0.5)
    ax.set_xlim(0, 1); ax.set_xlabel("Score")
    ax.set_title("Diagnostic Results by Area", color="#c9a84c", fontsize=11)
    for bar, val in zip(bars, vals):
        ax.text(val+0.02, bar.get_y()+bar.get_height()/2,
                f"{val*100:.0f}%", va="center", color="#e8eaf0", fontsize=10)
    return _topil(fig)

SHEET_PLOTS = {
    "Calc I — Derivatives": _plt_deriv,
    "Calc I — Integrals & FTC": _plt_integral,
    "Calc II — Series": _plt_series,
    "Calc II — Taylor Series": _plt_taylor,
    "Calc III — Partial Derivatives": _plt_gradient,
}

# ── Results builder ───────────────────────────────────────────────────────────
def build_results(answers: dict):
    correct = 0
    hits = {"Calc I":[0,0],"Calc II":[0,0],"Calc III":[0,0]}
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
    c1 = hits["Calc I"][0]/hits["Calc I"][1]
    c2 = hits["Calc II"][0]/hits["Calc II"][1]
    c3 = hits["Calc III"][0]/hits["Calc III"][1]
    pct = correct/20*100
    col = "#28c864" if pct>=70 else ("#c9a84c" if pct>=50 else "#ff5050")
    banner = (
        f'<div class="score-banner">'
        f'<div style="font-family:Georgia,serif;font-size:3rem;font-weight:700;color:{col}">{correct}/20</div>'
        f'<div style="color:rgba(240,235,224,0.55);margin-top:6px">{pct:.0f}% correct</div>'
        f'<div style="display:flex;gap:16px;justify-content:center;margin-top:14px;flex-wrap:wrap">'
        + ''.join(
            f'<div style="background:rgba(255,255,255,0.05);padding:8px 14px;border-radius:8px">'
            f'<div style="font-size:0.7rem;color:rgba(240,235,224,0.4)">{lb}</div>'
            f'<div style="color:#c9a84c;font-weight:700">{sc*100:.0f}%</div></div>'
            for lb, sc in [("Calc I",c1),("Calc II",c2),("Calc III",c3)]
        )
        + '</div>'
        f'<div style="color:rgba(240,235,224,0.3);font-size:0.78rem;margin-top:10px">'
        f'USNA: Calc I Day 1–2 · Calc II Week 2 MC · Calc III Week 2–3 MC+FR</div>'
        f'</div>'
    )
    try: chart = _plt_results(c1, c2, c3)
    except Exception: chart = None
    return banner + DIV + "\n".join(rows), chart, c1, c2, c3

# ── Gradio UI ─────────────────────────────────────────────────────────────────
with gr.Blocks(css=CSS, title="FissionLab Math — Dr. Preston") as demo:

    gr.HTML('<div class="app-hdr" style="display:flex;align-items:center;gap:14px">'
            '<span style="font-size:2.2rem">📐</span>'
            '<div><div style="font-family:Georgia,serif;font-size:1.4rem;font-weight:700;color:#c9a84c">'
            'FissionLab Math — USNA Calculus Prep</div>'
            '<div style="font-size:0.82rem;color:rgba(240,235,224,0.45)">'
            'Dr. Preston · Calc I–III · Stewart Early Transcendentals · 20-question diagnostic</div>'
            '</div></div>')

    with gr.Tabs():

        with gr.Tab("🎯 Diagnostic"):
            diag_state = gr.State({"page": 0, "answers": {}})

            with gr.Column(visible=True) as intro_col:
                gr.HTML(
                    '<div style="text-align:center;padding:36px 20px">'
                    '<div style="font-family:Georgia,serif;font-size:1.5rem;color:#c9a84c;margin-bottom:12px">'
                    '20-Question Diagnostic</div>'
                    '<div style="color:rgba(240,235,224,0.65);max-width:500px;margin:0 auto 24px;line-height:1.65">'
                    '7 Calc I &nbsp;·&nbsp; 7 Calc II &nbsp;·&nbsp; 6 Calc III<br>'
                    'Aligned with Stewart Early Transcendentals (2015)<br>'
                    '<b style="color:#c9a84c">10 questions visible at a time</b> — answer all 10, then click Next'
                    '</div></div>'
                )
                start_btn = gr.Button("▶ Begin Diagnostic", variant="primary", size="lg")

            with gr.Column(visible=False) as page1_col:
                gr.HTML('<div class="pg-hdr">Questions 1–10 of 20 &nbsp;·&nbsp; '
                        'Calc I (Q1–7) + Calc II start (Q8–10)</div>')
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
                next_btn = gr.Button("Next: Questions 11–20 →", variant="primary")

            with gr.Column(visible=False) as page2_col:
                gr.HTML('<div class="pg-hdr">Questions 11–20 of 20 &nbsp;·&nbsp; '
                        'Calc II (Q11–14) + Calc III (Q15–20)</div>')
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
                results_chart = gr.Image(label="Score by Area", visible=False, type="pil")
                cimgs         = [gr.Image(label="", visible=False, type="pil") for _ in range(2)]
                pathway_md    = gr.Markdown("")
                gr.HTML(DIV)
                restart_btn   = gr.Button("↺ Restart Diagnostic", variant="secondary")

        with gr.Tab("📐 Cheat Sheets"):
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
                f"### USNA Study Plan — {DAYS_LEFT} days until June 21\n\n"
                "**Exam order:** Calc I Day 1–2 (~70% pass) · Calc II Week 2 MC · Calc III Week 2–3 MC+FR\n\n"
                "---\n\n"
                "**Week 1 (Jun 2–7) — Calculus I**\n"
                "- Mon: Ch 2 Limits — direct sub → factor/cancel → L'Hôpital → squeeze\n"
                "- Tue: Ch 3 Power/product/quotient/chain rules — drill until automatic\n"
                "- Wed: Ch 3 Trig/exp/log derivatives, implicit differentiation\n"
                "- Thu: Ch 4 Optimization + related rates (substitute values LAST)\n"
                "- Fri: Ch 5 FTC Parts 1 & 2, u-substitution\n"
                "- Sat: **Mock Calc I** — 10 timed problems, review all misses\n"
                "- Sun: Light review\n\n"
                "**Week 2 (Jun 8–14) — Calculus II**\n"
                "- Mon: Ch 7 IBP (LIATE) — drill ∫x·cos(x), ∫x·ln(x)\n"
                "- Tue: Ch 7 Trig integrals + trig substitution\n"
                "- Wed: Ch 7 Partial fractions (long division if deg num ≥ denom)\n"
                "- Thu: Ch 11 Sequences, divergence test, geometric/p-series\n"
                "- Fri: Ch 11 Comparison, ratio, alternating series tests\n"
                "- Sat: Ch 11 Taylor/Maclaurin — memorize eˣ, sin, cos, 1/(1−x)\n"
                "- Sun: **Mock Calc II** — timed MC\n\n"
                "**Week 3 (Jun 15–20) — Calculus III** *(MC + free response)*\n"
                "- Mon: Ch 12 Vectors, dot/cross products, lines & planes\n"
                "- Tue: Ch 14 Partial derivatives, gradient, directional derivative\n"
                "- Wed: Ch 14 2nd deriv test, Lagrange multipliers\n"
                "- Thu: Ch 15 Double/triple integrals — switch to polar/cylindrical/spherical\n"
                "- Fri: Ch 16 Line integrals, conservative fields, Green's theorem\n"
                "- Sat: Ch 16 **Stokes + Divergence — free-response practice**\n\n"
                "**June 21 — Final Review:** Full 20-question diagnostic + targeted weak-area drill\n\n"
                "---\n*Daily: 30 min concept → 30 min problems → 15 min review misses*"
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
            'Dr. Preston · PhD · FissionLab · Stewart Calculus 8e (2015)</div>')

    # ── Diagnostic wiring ────────────────────────────────────────────────────
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
        htm, chart, c1, c2, c3 = build_results(answers)
        area_scores = {"Calc I":c1,"Calc II":c2,"Calc III":c3}
        weak = sorted(area_scores, key=lambda k: area_scores[k])[:2]
        plot_fns = {"Calc I":_plt_deriv,"Calc II":_plt_series,"Calc III":_plt_gradient}
        imgs = []
        for a in weak:
            try: imgs.append(plot_fns[a]())
            except Exception: imgs.append(None)
        while len(imgs) < 2: imgs.append(None)
        lines = [f"### Pathway — {DAYS_LEFT} days to June 21\n"]
        for lb, sc in [("Calc I",c1),("Calc II",c2),("Calc III",c3)]:
            bar = "█"*int(sc*10)+"░"*(10-int(sc*10))
            flag = "✅" if sc>=0.7 else ("⚠️" if sc>=0.4 else "🔴")
            lines.append(f"- **{lb}:** {bar} {sc*100:.0f}% {flag}")
        return ({"page":3,"answers":answers},
                gr.update(visible=False), gr.update(visible=False),
                gr.update(visible=False), gr.update(visible=True),
                gr.update(value=htm),
                gr.update(visible=chart is not None, value=chart),
                gr.update(visible=imgs[0] is not None, value=imgs[0]),
                gr.update(visible=imgs[1] is not None, value=imgs[1]),
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
