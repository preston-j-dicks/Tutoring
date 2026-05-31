# Calculus III — Worked Solutions

---

**1.**
(a) **u**·**v** = 2(1)+(−1)(4)+3(−2) = 2−4−6 = **−8**
(b) |**u**| = √(4+1+9) = √14; |**v**| = √(1+16+4) = √21
(c) cos θ = (−8)/(√14·√21) = −8/√294; θ = arccos(−8/√294) ≈ **118.1°**
(d) **u**×**v** = |**i** **j** **k**; 2 −1 3; 1 4 −2| = **i**(2−12) − **j**(−4−3) + **k**(8+1) = **⟨−10, 7, 9⟩**
(e) **u**·(−10,7,9) = −20−7+27 = 0 ✓; **v**·(−10,7,9) = −10+28−18 = 0 ✓

**2.** Vectors in plane: **PQ** = ⟨2,−1,−1⟩, **PR** = ⟨−1,1,2⟩.
Normal: **n** = **PQ**×**PR** = ⟨(−2+1),(1−4),(2−1)⟩ = ⟨−1,−5,1⟩.
Check: ⟨(−2)(2)−(−1)(1), (−1)(−1)−(2)(2), (2)(1)−(−1)(−1)⟩ = ⟨−3, −3, 1⟩.

Let me redo carefully: **PQ** = ⟨2,−1,−1⟩, **PR** = ⟨−1,1,2⟩.
**n** = ⟨(−1)(2)−(−1)(1), (−1)(−1)−(2)(2), (2)(1)−(−1)(−1)⟩ = ⟨−2+1, 1−4, 2−1⟩ = ⟨−1,−3,1⟩.
Plane: −1(x−1) − 3(y−2) + 1(z−0) = 0 → **−x − 3y + z = −7, or x + 3y − z = 7**
Verify: P(1,2,0): 1+6−0=7 ✓; Q(3,1,−1): 3+3+1=7 ✓; R(0,3,2): 0+9−2=7 ✓

**3.** x = 2+4t, y = −1−2t, z = 3+t

**4.** Distance = |2(3)−1+2(−1)−4|/√(4+1+4) = |6−1−2−4|/3 = **|−1|/3 = 1/3**

---

**5.**
(a) fₓ = 3x²y − 2y²; f_y = x³ − 4xy + 3y²
(b) fₓₓ = 6xy; f_yy = −4x + 6y; fₓy = 3x² − 4y
Verify: f_yₓ = ∂/∂y(3x²y−2y²) = 3x²−4y = fₓy ✓

**6.**
(a) ∂f/∂x = y·e^(xy)·sin x + e^(xy)·cos x = e^(xy)(y sin x + cos x)
(b) At (π, 0): e^(0)(0·sin π + cos π) = 1·(0−1) = −1.
∂f/∂y = x·e^(xy)·sin x. At (π,0): π·1·sin π = 0.
∇f(π, 0) = **⟨−1, 0⟩**

**7.** ∇f = ⟨2xyz, x²z, x²y⟩. At (1,1,2): ∇f = ⟨4, 2, 1⟩.
Unit vector: |**v**| = √(1+4+4) = 3; **û** = ⟨1/3, 2/3, 2/3⟩.
D_**û**f = ∇f·**û** = 4/3 + 4/3 + 2/3 = **10/3**

**8.** fₓ = 2x−2y; f_y = 2y−2x. At (1,2): fₓ = 2−4 = −2; f_y = 4−2 = 2.
Tangent plane: z − 1 = −2(x−1) + 2(y−2) → **z = −2x + 2y − 1**

---

**9.** fₓ = 3x²−3 = 0 → x = ±1; f_y = 2y−2 = 0 → y = 1.
Critical points: (1,1) and (−1,1).
D = fₓₓ·f_yy − fₓy²: fₓₓ = 6x, f_yy = 2, fₓy = 0.
At (1,1): D = 6·2−0 = 12 > 0, fₓₓ = 6 > 0 → **local minimum.** f(1,1) = 1−3+1−2 = −3.
At (−1,1): D = −6·2 = −12 < 0 → **saddle point.** f(−1,1) = −1+3+1−2 = 1.

**10.** ∇f = λ∇g: ⟨2, 3⟩ = λ⟨2x, 2y⟩ → x = 1/λ, y = 3/(2λ).
Constraint: x²+y² = 1 → 1/λ² + 9/(4λ²) = 1 → 13/(4λ²) = 1 → λ = ±√13/2.
x = 2/√13, y = 3/√13 → f = 4/√13 + 9/√13 = **13/√13 = √13 (maximum)**
x = −2/√13, y = −3/√13 → f = **−√13 (minimum)**

**11.** Let x = y (square base by symmetry) and z = height. Constraint: x²z = 32 → z = 32/x².
S = x² + 4xz = x² + 4x(32/x²) = x² + 128/x.
dS/dx = 2x − 128/x² = 0 → x³ = 64 → x = 4.
z = 32/16 = 2. **Base: 4×4 cm, height: 2 cm.**

---

**12.** Region: 0 ≤ x ≤ 2, 0 ≤ y ≤ 2−x.
∫₀²∫₀^(2−x)(x+y) dy dx = ∫₀²[xy + y²/2]₀^(2−x) dx = ∫₀²[x(2−x) + (2−x)²/2] dx
= ∫₀²[(2−x)(x + (2−x)/2)] dx = ∫₀²(2−x)(x+1−x/2) dx = ∫₀²(2−x)(1+x/2) dx
= ∫₀²(2 + x − x − x²/2) dx = ∫₀²(2 − x²/2) dx = [2x − x³/6]₀² = 4 − 8/6 = **8/3**

**13.** Polar: x = r cos θ, y = r sin θ; 0 ≤ r ≤ 2, 0 ≤ θ ≤ 2π.
∬ r²·r dr dθ = ∫₀^(2π) ∫₀² r³ dr dθ = 2π·[r⁴/4]₀² = 2π·4 = **8π**

**14.** Region: x²+y² ≤ z ≤ 4, above z=0. Use cylindrical.
z ranges 0 to 4−r², r from 0 to 2 (where 4−r²=0).
∭ z dV = ∫₀^(2π)∫₀²∫₀^(4−r²) z·r dz dr dθ = 2π∫₀²r[z²/2]₀^(4−r²) dr
= π∫₀²r(4−r²)² dr = π∫₀²r(16−8r²+r⁴) dr = π[8r²−2r⁴+r⁶/6]₀² = π(32−32+64/6) = **32π/3**

**15.** ∫₀^(π/2)∫₀³ e^(−r²)·r dr dθ = (π/2)·[−e^(−r²)/2]₀³ = (π/2)·(−e⁻⁹/2 + 1/2) = **π(1−e⁻⁹)/4**

---

**16.**
(a) ∂P/∂y = 2x = ∂Q/∂x → **conservative** ✓
(b) f = ∫2xy dx = x²y + g(y). f_y = x² + g'(y) = x²+3y² → g'(y) = 3y² → g = y³.
**f(x,y) = x²y + y³**
(c) ∫_C **F**·d**r** = f(2,1) − f(0,0) = (4·1+1) − 0 = **5**

**17.** ∂(2xy)/∂x = 2y = ∂(y²)/∂y → wait, let P = y², Q = 2xy.
∂P/∂y = 2y; ∂Q/∂x = 2y → **conservative!** Potential: f = xy² + C.
∫_C = f(−1,0) − f(1,0) = 0 − 0 = **0**

**18.** Green's theorem: ∮ P dx + Q dy = ∬(∂Q/∂x − ∂P/∂y) dA.
∂Q/∂x = 1; ∂P/∂y = 0. Integrand = 1.
∬_D 1 dA = Area of rectangle = 3·2 = **6**

**19.** ∇·**F** = 2x + 2y + 2z.
∭_E (2x+2y+2z) dV = 2∫₀²∫₀²∫₀²(x+y+z) dx dy dz.
By symmetry: each of ∫∫∫x, ∫∫∫y, ∫∫∫z = 8·(∫₀²x dx)/(2) = 8·[x²/2]₀² = 8·2 = 16.

Actually: ∫₀²∫₀²∫₀²x dV = (∫₀²x dx)(∫₀²dy)(∫₀²dz) = 2·2·2 = 8. Same for y and z.
Total = 2(8+8+8) = **48**

---

**FR-1.**
(a) Domain: all (x,y) ∈ R²; Range: z ≤ 4 (since −x²−y² ≤ 0).
Level curves: 4−x²−y² = k → x²+y² = 4−k (circles of radius √(4−k) for k < 4).

(b) ∇f = ⟨−2x, −2y⟩. At (1,1): ∇f = **⟨−2, −2⟩**.
Direction of steepest increase: ⟨−2, −2⟩ (or unit vector ⟨−1/√2, −1/√2⟩).
Maximum rate of increase: |∇f| = **2√2**.

(c) Tangent plane: z − 2 = −2(x−1) − 2(y−1) → **z = −2x − 2y + 6**

(d) In polar: z = 4 − r² ≥ 0 → r ≤ 2. Volume:
V = ∫₀^(2π)∫₀² (4−r²)·r dr dθ

**FR-2.**
(a) ∇·**F** = z + z + 0 = wait: ∂(xz)/∂x = z, ∂(yz)/∂y = z, ∂(−(x²+y²)/2)/∂z = 0.
∇·**F** = **z + z = 2z**

Curl: ∇×**F** = ⟨∂(−(x²+y²)/2)/∂y − ∂(yz)/∂z, ∂(xz)/∂z − ∂(−(x²+y²)/2)/∂x, ∂(yz)/∂x − ∂(xz)/∂y⟩
= ⟨−y − y, x − x, 0 − 0⟩ = **⟨−2y, 0, 0⟩**

(b) Divergence theorem: ∯_S **F**·d**S** = ∭_E ∇·**F** dV = ∭_E 2z dV.
On sphere of radius 2 in spherical coords:
= ∫₀^(2π)∫₀^π∫₀² 2ρcos φ · ρ²sin φ dρ dφ dθ
= 2π · ∫₀^π sin φ cos φ dφ · ∫₀² 2ρ³ dρ
= 2π · [sin²φ/2]₀^π · [ρ⁴/2]₀² = 2π · 0 · 8 = **0**

(c) ∇×**F** = ⟨−2y, 0, 0⟩ ≠ **0** → **F** is **NOT conservative**.
