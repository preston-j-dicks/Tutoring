# Calculus II — Worked Solutions

---

**1.** u = x²+1, du = 2x dx. ∫x(x²+1)^(1/2) dx = ½∫u^(1/2) du = ½·(2/3)u^(3/2) + C = **(x²+1)^(3/2)/3 + C**

**2.** IBP: u = x, dv = cos x dx → du = dx, v = sin x.
∫x cos x dx = x sin x − ∫sin x dx = **x sin x + cos x + C**

**3.** ∫sin³x dx = ∫sin²x·sin x dx = ∫(1−cos²x) sin x dx.
u = cos x, du = −sin x dx.
= −∫(1−u²) du = −u + u³/3 + C = **−cos x + cos³x/3 + C**

**4.** Long division: x²/(x²−4) = 1 + 4/(x²−4).
Partial fractions: 4/(x²−4) = 4/[(x−2)(x+2)] = A/(x−2) + B/(x+2).
4 = A(x+2) + B(x−2). x=2: A=1; x=−2: B=−1.
∫[1 + 1/(x−2) − 1/(x+2)] dx = **x + ln|x−2| − ln|x+2| + C = x + ln|(x−2)/(x+2)| + C**

**5.** x²+2x+5 = (x+1)²+4. Let u = x+1, du = dx.
∫1/[(x+1)²+4] dx = ∫1/(u²+4) du = (1/2)arctan(u/2) + C = **(1/2)arctan((x+1)/2) + C**

**6.** x = 3 sin θ, dx = 3 cos θ dθ, √(9−x²) = 3 cos θ.
∫3 cos θ·3 cos θ dθ = 9∫cos²θ dθ = (9/2)∫(1+cos 2θ) dθ = (9/2)(θ + sin 2θ/2) + C.
Back-substitute: θ = arcsin(x/3), sin 2θ = 2 sin θ cos θ = 2(x/3)(√(9−x²)/3) = 2x√(9−x²)/9.
= **(9/2)arcsin(x/3) + (x/2)√(9−x²) + C**
(This is also the area formula for a circle of radius 3.)

---

**7.** Intersection: x² = x+2 → x²−x−2 = 0 → (x−2)(x+1) = 0 → x = −1, 2.
On [−1,2]: x+2 ≥ x².
A = ∫₋₁²(x+2−x²) dx = [x²/2 + 2x − x³/3]₋₁² = (2+4−8/3) − (1/2−2+1/3) = (10/3) − (−7/6) = **9/2**

**8.** V = π∫₀²(x²)² dx = π∫₀² x⁴ dx = π[x⁵/5]₀² = **32π/5**

**9.** Shell method about y-axis: V = 2π∫₀⁴ x·√x dx = 2π∫₀⁴ x^(3/2) dx = 2π[2x^(5/2)/5]₀⁴ = 2π·(2·32/5) = **128π/5**

**10.** y' = x^(1/2). Arc length = ∫₀³√(1+x) dx. u = 1+x, du = dx.
= ∫₁⁴√u du = [2u^(3/2)/3]₁⁴ = (2·8/3) − (2/3) = **14/3**

**11.** ∫₁^∞ x⁻² dx = lim(b→∞)[−1/x]₁ᵇ = lim(0−(−1)) = **1 (converges)**

**12.** ∫₀¹ x^(−1/2) dx = lim(ε→0⁺)[2x^(1/2)]ε¹ = 2−0 = **2 (converges)**

---

**13.** f(x) = x/(x²+1) is positive and decreasing for x ≥ 1.
∫₁^∞ x/(x²+1) dx = ½[ln(x²+1)]₁^∞ = ∞. **Diverges by integral test.**

**14.** Σ 1/n²: p = 2 > 1 → **converges** (Basel problem, sum = π²/6).
Σ 1/√n = Σ n^(−1/2): p = 1/2 ≤ 1 → **diverges**.

**15.** Geometric: a = 1, r = 3/4. |r| < 1 → **converges. Sum = 1/(1−3/4) = 4.**

**16.** aₙ = n!/3ⁿ. |aₙ₊₁/aₙ| = (n+1)!/3^(n+1) · 3ⁿ/n! = (n+1)/3 → ∞ as n→∞.
L > 1 → **diverges.**

**17.** aₙ = xⁿ/n!. |aₙ₊₁/aₙ| = |x|/(n+1) → 0 for all x.
L = 0 < 1 for all x → **converges for all x. Interval of convergence: (−∞, ∞).**

**18.** Σ|aₙ| = Σ 1/n (harmonic series) → diverges. So NOT absolutely convergent.
Alternating series test: bₙ = 1/n is decreasing → 0. → **conditionally convergent.**

---

**19.** eˣ = 1 + x + x²/2! + x³/3! + x⁴/4! + ···
e^(0.1) ≈ 1 + 0.1 + 0.01/2 + 0.001/6 + 0.0001/24 = 1 + 0.1 + 0.005 + 0.0001667 + 0.0000042 ≈ **1.10517**

**20.** sin(u) = u − u³/6 + u⁵/120 − ··· where u = x².
sin(x²) = **x² − x⁶/6 + x¹⁰/120 − ···**

**21.** 1/(1−x) = Σxⁿ → 1/(1+x²) = Σ(−1)ⁿx^(2n) = 1 − x² + x⁴ − x⁶ + ···
Integrate: arctan(x) = ∫1/(1+x²) dx = **Σ(−1)ⁿx^(2n+1)/(2n+1) = x − x³/3 + x⁵/5 − ···** (for |x| ≤ 1)

**22.** Let h = x − π/2. f = cos(x):
f(π/2) = 0; f'(π/2) = −sin(π/2) = −1; f''(π/2) = −cos(π/2) = 0; f'''(π/2) = sin(π/2) = 1.
cos(x) = **0 − (x−π/2) + 0 + (x−π/2)³/6 − ···** = −(x−π/2) + (x−π/2)³/6 − ···

**23.** sin(x)/x = 1 − x²/6 + x⁴/120 − ···
∫₀^(0.5)(1 − x²/6) dx ≈ [x − x³/18]₀^(0.5) = 0.5 − (0.125/18) ≈ 0.5 − 0.00694 ≈ **0.4931**
(Actual value ≈ 0.4931 — excellent approximation)

---

**24.** dy/dx = (dy/dt)/(dx/dt) = (3t²−1)/(2t).
Horizontal tangent: 3t²−1 = 0 → **t = ±1/√3**
Vertical tangent: dx/dt = 2t = 0 → **t = 0**

**25.** A = ½∫₋π^π (1+cos θ)² dθ = ½∫₋π^π (1 + 2cos θ + cos²θ) dθ.
Use cos²θ = (1+cos 2θ)/2: A = ½∫₋π^π (3/2 + 2cos θ + cos 2θ/2) dθ.
= ½[3θ/2 + 2sin θ + sin 2θ/4]₋π^π = ½(3π − (−3π)) = **3π/2**

**26.** dx/dt = −sin t, dy/dt = cos t. |r'| = √(sin²t + cos²t) = 1.
L = ∫₀^(2π) 1 dt = **2π**. The curve is a **unit circle**, which has circumference 2π. ✓

---

**27.**
(a) a₁ = 1; a₂ = √3 ≈ 1.732; a₃ = √(2√3+1) ≈ √4.464 ≈ 2.113; a₄ ≈ √5.226 ≈ 2.286
(b) At the limit, L = √(2L+1) → L² = 2L+1 → L²−2L−1 = 0 → L = (2+√8)/2 = **1+√2 ≈ 2.414** (taking positive root)
(c) Sequence is increasing and bounded above by 1+√2 (show by induction); monotone bounded sequences converge. ✓

**28.**
(a) x sin x = x·(x − x³/6 + x⁵/120 − ···) = **x² − x⁴/6 + x⁶/120 − ···**
(b) x sin x − x² = −x⁴/6 + O(x⁶). Divide by x⁴: → **−1/6** as x→0.
(c) By IBP: ∫₀¹ x sin x dx = [−x cos x + sin x]₀¹ = −cos 1 + sin 1 ≈ −0.5403 + 0.8415 = **0.3012**
By series: ∫₀¹(x² − x⁴/6 + x⁶/120) dx = [x³/3 − x⁵/30 + x⁷/840]₀¹ = 1/3 − 1/30 + 1/840 = 280/840 − 28/840 + 1/840 = 253/840 ≈ **0.3012 ✓**
