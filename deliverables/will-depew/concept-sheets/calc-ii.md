# Calculus II — Concept Reference
**Target:** USNA Validation Exam (multiple-choice, ~Plebe Summer Week 2)

---

## 1. Integration Techniques

### u-Substitution
Replace inner function with u, rewrite entire integral in u. Works when the integrand has f(g(x))·g'(x) form.
- ∫2x(x²+1)⁴ dx: u = x²+1, du = 2x dx → ∫u⁴ du = u⁵/5 + C

### Integration by Parts (IBP)
∫u dv = uv − ∫v du

**LIATE priority for u:** Logarithms, Inverse trig, Algebraic, Trig, Exponential

Classic examples:
- ∫x eˣ dx: u = x, dv = eˣ dx → x eˣ − eˣ + C
- ∫x ln x dx: u = ln x, dv = x dx → (x²/2) ln x − x²/4 + C
- ∫eˣ sin x dx: IBP twice, then solve algebraically

### Trigonometric Integrals

**∫sinᵐx cosⁿx dx:**
- Odd power of sin: save one sin x, convert rest via sin²x = 1−cos²x, use u = cos x
- Odd power of cos: save one cos x, convert rest via cos²x = 1−sin²x, use u = sin x
- Both even: use half-angle identities: sin²x = (1−cos 2x)/2, cos²x = (1+cos 2x)/2

**Trig substitution:**
| Form | Sub | Identity used |
|------|-----|---------------|
| √(a²−x²) | x = a sin θ | 1−sin²θ = cos²θ |
| √(a²+x²) | x = a tan θ | 1+tan²θ = sec²θ |
| √(x²−a²) | x = a sec θ | sec²θ−1 = tan²θ |

### Partial Fractions
For rational functions P(x)/Q(x) where deg P < deg Q:
- Factor denominator completely
- Linear factor (ax+b): A/(ax+b)
- Repeated linear (ax+b)²: A/(ax+b) + B/(ax+b)²
- Irreducible quadratic (ax²+bx+c): (Ax+B)/(ax²+bx+c)
- Multiply both sides, compare coefficients or plug in roots

---

## 2. Applications of Integration

**Area between curves:** A = ∫ₐᵇ [f(x) − g(x)] dx, where f(x) ≥ g(x)

**Volumes of revolution:**
- **Disk method** (axis is boundary): V = π∫ₐᵇ [f(x)]² dx
- **Washer method** (gap between curves): V = π∫ₐᵇ ([R(x)]² − [r(x)]²) dx
- **Shell method** (parallel to axis): V = 2π∫ₐᵇ x·f(x) dx (rotation about y-axis)

**Arc length:** L = ∫ₐᵇ √(1 + [f'(x)]²) dx

**Trap:** Disk/washer vs shell — draw a picture. Disk/washer: rectangles perpendicular to axis. Shell: rectangles parallel to axis.

---

## 3. Improper Integrals

**Type I** (infinite limit): ∫₁^∞ f(x) dx = lim(b→∞) ∫₁ᵇ f(x) dx

**Type II** (discontinuity in [a,b]): ∫₀¹ 1/√x dx = lim(ε→0⁺) ∫ε¹ 1/√x dx

**Converges** if limit exists and is finite; **diverges** otherwise.

**p-integral:** ∫₁^∞ 1/xᵖ dx converges iff p > 1. ∫₀¹ 1/xᵖ dx converges iff p < 1.

---

## 4. Sequences & Series

**Sequence** {aₙ}: converges if lim(n→∞) aₙ = L (finite).

**Series** Σaₙ: converges if partial sums Sₙ → finite limit.

**Convergence Tests:**

| Test | When to use | Condition for convergence |
|------|-------------|--------------------------|
| Divergence test | Always check first | lim aₙ ≠ 0 → diverges |
| Geometric series | aₙ = arⁿ | |r| < 1; sum = a/(1−r) |
| p-series | aₙ = 1/nᵖ | p > 1 |
| Integral test | f decreasing, positive | ∫ f converges |
| Comparison | aₙ ≤ bₙ | bₙ converges → aₙ converges |
| Limit comparison | similar aₙ, bₙ | lim aₙ/bₙ = c > 0: same behavior |
| Ratio test | factorials, exponentials | L = lim|aₙ₊₁/aₙ|; L < 1 converges |
| Root test | aₙ = [bₙ]ⁿ | L = lim|aₙ|^(1/n); L < 1 converges |
| Alternating series | (−1)ⁿ bₙ, bₙ > 0 | bₙ decreasing → 0: converges |

**Absolute vs conditional convergence:** Σ|aₙ| converges → Σaₙ absolutely converges (stronger). Alternating series can converge conditionally.

---

## 5. Power Series, Taylor & Maclaurin

**Power series:** Σcₙ(x−a)ⁿ converges on interval |x−a| < R (radius of convergence R found by ratio test).

**Key Maclaurin series (memorize these):**

| Function | Series | Radius |
|----------|--------|--------|
| eˣ | Σ xⁿ/n! = 1 + x + x²/2! + x³/3! + ··· | ∞ |
| sin x | Σ (−1)ⁿx^(2n+1)/(2n+1)! = x − x³/6 + x⁵/120 − ··· | ∞ |
| cos x | Σ (−1)ⁿx^(2n)/(2n)! = 1 − x²/2 + x⁴/24 − ··· | ∞ |
| 1/(1−x) | Σ xⁿ = 1 + x + x² + ··· | |x| < 1 |
| ln(1+x) | Σ (−1)ⁿ⁺¹xⁿ/n = x − x²/2 + x³/3 − ··· | |x| ≤ 1 |
| arctan x | Σ (−1)ⁿx^(2n+1)/(2n+1) = x − x³/3 + x⁵/5 − ··· | |x| ≤ 1 |

**Taylor series at a:** f(x) = Σ f⁽ⁿ⁾(a)/n! · (x−a)ⁿ

**Error bound (alternating series):** |error| ≤ first omitted term

---

## 6. Parametric Curves

Curve defined by x = f(t), y = g(t).

- **Slope:** dy/dx = (dy/dt)/(dx/dt)
- **Second derivative:** d²y/dx² = [d/dt(dy/dx)] / (dx/dt)
- **Arc length:** L = ∫ₐᵇ √([dx/dt]² + [dy/dt]²) dt
- **Area:** A = ∫ y dx = ∫ₐᵇ g(t) f'(t) dt

---

## 7. Polar Coordinates

Convert: x = r cos θ, y = r sin θ; r² = x² + y²

- **Area** enclosed: A = ½∫ₐᵇ r² dθ
- **Area between two curves:** A = ½∫ₐᵇ (r_outer² − r_inner²) dθ
- **Arc length:** L = ∫ₐᵇ √(r² + (dr/dθ)²) dθ

Common curves: r = a (circle), r = a cos θ (circle through origin), r = 1 + cos θ (cardioid), r = sin(nθ) (rose: 2n petals if n even, n petals if n odd).

---

## Common Traps on Calc II Exams
- Forgetting IBP needs to be done twice for eˣ sin x
- Trig sub: don't forget to convert the answer back to x
- Partial fractions: make sure degree of numerator < denominator (if not, do polynomial long division first)
- Series: Divergence test only proves divergence, never convergence
- Ratio test is inconclusive when L = 1 — try another test
