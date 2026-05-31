# Calculus I — Concept Reference
**Target:** USNA Validation Exam (SP211-track, Plebe Summer Day 1–2)

---

## 1. Limits & Continuity

**Definition:** lim(x→a) f(x) = L means f(x) approaches L as x approaches a (regardless of f(a)).

**Key techniques:**
- Direct substitution (try first)
- Factor and cancel (0/0 forms)
- L'Hôpital's Rule: if lim f/g = 0/0 or ∞/∞, then lim f/g = lim f'/g'
- Squeeze theorem: if g(x) ≤ f(x) ≤ h(x) and lim g = lim h = L, then lim f = L

**Continuity at x = a:** f is continuous iff (1) f(a) exists, (2) lim exists, (3) they're equal.

**Important limits:**
- lim(x→0) sin(x)/x = 1
- lim(x→0) (1 − cos x)/x = 0
- lim(x→∞) (1 + 1/x)^x = e

**Common trap:** L'Hôpital applies ONLY to 0/0 or ±∞/±∞. Don't apply it to 0/∞ directly — rewrite first.

---

## 2. Derivatives

**Definition:** f'(x) = lim(h→0) [f(x+h) − f(x)] / h

**Rules (must be automatic):**

| Rule | Formula |
|------|---------|
| Power | d/dx[xⁿ] = nxⁿ⁻¹ |
| Product | (uv)' = u'v + uv' |
| Quotient | (u/v)' = (u'v − uv') / v² |
| Chain | d/dx[f(g(x))] = f'(g(x)) · g'(x) |

**Trig derivatives:**
- d/dx[sin x] = cos x
- d/dx[cos x] = −sin x
- d/dx[tan x] = sec²x
- d/dx[sec x] = sec x tan x
- d/dx[csc x] = −csc x cot x
- d/dx[cot x] = −csc²x

**Inverse trig:**
- d/dx[arcsin x] = 1/√(1−x²)
- d/dx[arctan x] = 1/(1+x²)

**Exponential/Log:**
- d/dx[eˣ] = eˣ
- d/dx[ln x] = 1/x
- d/dx[aˣ] = aˣ ln a

**Implicit differentiation:** Differentiate both sides with respect to x; treat y as a function of x, so d/dx[y] = dy/dx. Solve for dy/dx.

---

## 3. Related Rates

**Method:**
1. Draw a diagram, label all quantities
2. Write an equation relating the quantities
3. Differentiate both sides with respect to t
4. Substitute known rates and values, solve for unknown rate

**Common equations:** Pythagorean theorem, similar triangles, volume formulas, trig relations.

**Trap:** Don't substitute specific values until AFTER differentiating.

---

## 4. Optimization

**Method:**
1. Write objective function f(x) to maximize/minimize
2. Write constraint and use it to reduce to one variable
3. Find critical points: f'(x) = 0
4. Use second derivative test (f'' > 0: min; f'' < 0: max) or check endpoints
5. Answer the question (include units)

**Closed interval method:** f attains its absolute extrema at critical points or endpoints of [a, b].

---

## 5. Curve Sketching

Use: domain, intercepts, symmetry, asymptotes, intervals of increase/decrease (f' sign), concavity (f'' sign), inflection points (f'' = 0 or DNE).

- f' > 0: increasing; f' < 0: decreasing
- f'' > 0: concave up; f'' < 0: concave down
- Inflection point: f'' changes sign

---

## 6. Fundamental Theorem of Calculus

**FTC Part 1:** If F(x) = ∫ₐˣ f(t) dt, then F'(x) = f(x).

**FTC Part 2:** ∫ₐᵇ f(x) dx = F(b) − F(a), where F is any antiderivative of f.

**Chain rule extension:** d/dx[∫ₐᵍ⁽ˣ⁾ f(t) dt] = f(g(x)) · g'(x)

---

## 7. Integration Basics

**Basic antiderivatives:**
- ∫xⁿ dx = xⁿ⁺¹/(n+1) + C, n ≠ −1
- ∫1/x dx = ln|x| + C
- ∫eˣ dx = eˣ + C
- ∫sin x dx = −cos x + C
- ∫cos x dx = sin x + C
- ∫sec²x dx = tan x + C

**u-substitution:** Reverse chain rule. Let u = inner function, compute du, rewrite integral in u, integrate, back-substitute.

**Definite integral = signed area** under curve from a to b.

---

## Common Traps on Calc I Exams
- Forgetting + C on indefinite integrals
- Chain rule in derivatives (especially nested trig/exp)
- L'Hôpital on forms that aren't 0/0 or ∞/∞
- Related rates: differentiating before substituting values
- Optimization: not checking whether a critical point is actually max/min
