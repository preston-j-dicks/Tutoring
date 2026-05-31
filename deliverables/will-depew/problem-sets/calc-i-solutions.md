# Calculus I — Worked Solutions

---

**1.** lim(x→3) (x²−9)/(x−3) = lim (x+3)(x−3)/(x−3) = lim (x+3) = **6**

**2.** lim(x→0) sin(5x)/(3x) = (5/3)·lim sin(5x)/(5x) = (5/3)·1 = **5/3**

**3.** f(x) = (x+2)(x−2)/(x−2) = x+2 for x ≠ 2. The limit exists (= 4), but f(2) is undefined. **Removable discontinuity** at x = 2.

**4.** Form ∞/∞; apply L'Hôpital (or divide by x²): lim (3 + 1/x²)/(5 − 2/x²) = **3/5**

**5.** Denominator = 0 at x = 1 and x = −2. Since numerator ≠ 0 at these points: **infinite (vertical asymptote) discontinuities at x = 1 and x = −2.**

---

**6.** f'(x) = **12x² − 14x + 2**

**7.** Product rule: d/dx[sin(x²)] = 2x cos(x²).
f'(x) = 2x cos(x²)·eˣ + sin(x²)·eˣ = **eˣ[2x cos(x²) + sin(x²)]**

**8.** f'(x) = [(6x)(x+4) − (3x²−1)(1)] / (x+4)²
= [6x² + 24x − 3x² + 1] / (x+4)²
= **(3x² + 24x + 1) / (x+4)²**

**9.** d/dx[arctan(u)] = u'/(1+u²), u = 2x, u' = 2.
f'(x) = **2/(1 + 4x²)**

**10.** Differentiate: 2x + 2y(dy/dx) = 0 → dy/dx = −x/y
At (3, 4): dy/dx = **−3/4**

---

**11.** V = 4/3 π r³; dV/dt = 4πr²·(dr/dt) = 4π(25)(2) = **200π cm³/s ≈ 628 cm³/s**

**12.** x² + y² = 100. Differentiate: 2x(dx/dt) + 2y(dy/dt) = 0.
When x = 6: y = √(100−36) = 8.
dy/dt = −x(dx/dt)/y = −6(1)/8 = **−3/4 m/s** (top slides down at 0.75 m/s)

**13.** By similar triangles, r/h = 4/12 → r = h/3.
V = ⅓π r²h = ⅓π(h/3)²h = πh³/27
dV/dt = (π/9)h² · dh/dt
−2 = (π/9)(36) dh/dt → dh/dt = **−18/(36π) = −1/(2π) ≈ −0.159 m/min**

---

**14.** Let 2x, 2y be sides of rectangle inscribed in circle of radius 5. Constraint: x² + y² = 25.
Area A = (2x)(2y) = 4xy. Maximize xy subject to x²+y²=25.
Using AM-GM or Lagrange: maximum when x = y = 5/√2.
Dimensions: **2x = 2y = 5√2 ≈ 7.07 m** (it's a square)

**15.** Let width = x (perpendicular to river), length = y. Constraint: 2x + y = 300 → y = 300−2x.
A = xy = x(300−2x) = 300x − 2x²
A' = 300 − 4x = 0 → x = 75, y = 150.
**Width = 75 m, length = 150 m. Maximum area = 11,250 m²**

**16.** f'(x) = 3x² − 3 = 3(x−1)(x+1) = 0 → x = ±1.
f(−2) = −8+6 = −2; f(−1) = −1+3 = 2; f(1) = 1−3 = −2; f(2) = 8−6 = 2.
**Absolute maximum = 2 (at x = −1 and x = 2). Absolute minimum = −2 (at x = −2 and x = 1).**

**17.** Let x = side of cut squares. Box dimensions: (12−2x) × (12−2x) × x.
V(x) = x(12−2x)² = x(144 − 48x + 4x²) = 144x − 48x² + 4x³
V'(x) = 144 − 96x + 12x² = 12(x² − 8x + 12) = 12(x−2)(x−6)
x = 2 (valid, since 0 < x < 6) or x = 6 (gives 0 volume).
**Cut squares of side x = 2 cm. Volume = 2·(8)² = 128 cm³**

---

**18.** ∫(3x²−4x+1) dx = **x³ − 2x² + x + C**

**19.** ∫₀³(x²−2x+1) dx = ∫₀³(x−1)² dx = [(x−1)³/3]₀³ = (8/3) − (−1/3) = **3**

**20.** u = x², du = 2x dx → (1/2)∫sin(u) du = (−1/2)cos(u) + C = **−½cos(x²) + C**

**21.** By FTC Part 1: G'(x) = √(x³+1).
G'(2) = √(8+1) = √9 = **3**

**22.** Intersection: x² = 2x → x = 0, 2. On [0,2], 2x ≥ x².
A = ∫₀²(2x−x²) dx = [x² − x³/3]₀² = 4 − 8/3 = **4/3**

---

**23.** Let x = distance from base to person, s = shadow length.
By similar triangles: 8/(x+s) = 1.8/s → 8s = 1.8(x+s) → 6.2s = 1.8x → s = 1.8x/6.2 = 9x/31.
ds/dt = (9/31)(dx/dt) = (9/31)(1.2) = **10.8/31 ≈ 0.348 m/s**

(Shadow grows at ≈ 0.35 m/s, independent of position.)

**24.** Let sides be a, b with 2(a+b) = P → b = P/2 − a.
Area = a(P/2−a) = Pa/2 − a². A' = P/2 − 2a = 0 → a = P/4.
Then b = P/4 = a. A'' = −2 < 0 → maximum. QED, square maximizes area.

**25.** f(x) = x⁴ − 4x³
f'(x) = 4x³ − 12x² = 4x²(x−3) = 0 → x = 0 (neither ext.), x = 3 (min)
f''(x) = 12x² − 24x = 12x(x−2) = 0 → inflection points at x = 0 and x = 2

Behavior:
- Decreasing on (−∞, 3) except at x = 0 (f' changes sign only at x = 3)
  [more precisely: f' < 0 on (−∞,0), f' < 0 on (0,3), f' > 0 on (3,∞)]
- Concave up: (−∞,0) and (2,∞); concave down: (0,2)
- f(−1) = 1+4 = 5; f(0) = 0; f(3) = 81−108 = −27; f(4) = 256−256 = 0

On [−1,4]: **Absolute max = 5 at x = −1; absolute min = −27 at x = 3**
Local min at x = 3 (no local max in open interior).
Inflection points at (0,0) and (2, −16).
