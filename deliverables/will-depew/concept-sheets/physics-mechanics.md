# Physics — Calculus-Based Mechanics (SP211)
**Target:** USNA SP211 Validation Exam — prioritized

---

## 1. Kinematics

**1D uniform acceleration (constant a):**
- v = v₀ + at
- x = x₀ + v₀t + ½at²
- v² = v₀² + 2a(x − x₀)
- x = x₀ + ½(v₀ + v)t

**Calculus connection:** v = dx/dt, a = dv/dt = d²x/dt². For non-constant acceleration: x = ∫v dt, v = ∫a dt.

**2D Projectile motion (a_x = 0, a_y = −g):**
- x(t) = x₀ + v₀cos(θ) t
- y(t) = y₀ + v₀sin(θ) t − ½g t²
- Range (level ground): R = v₀²sin(2θ)/g (max at θ = 45°)
- Time of flight: T = 2v₀sin(θ)/g
- Max height: H = v₀²sin²(θ)/(2g)

**Circular motion:**
- Centripetal acceleration: aₓ = v²/r (directed toward center)
- For uniform circular motion: |**a**| = ω²r, v = ωr

---

## 2. Newton's Laws

**First:** Σ**F** = 0 ↔ constant velocity (including rest)
**Second:** Σ**F** = m**a** (vector equation — apply component by component)
**Third:** **F**₁₂ = −**F**₂₁ (action-reaction pairs act on DIFFERENT objects)

**Common forces:**
- Weight: W = mg (downward, g = 9.8 m/s² ≈ 10 m/s²)
- Normal force: perpendicular to surface
- Friction: f_k = μ_k N; f_s ≤ μ_s N
- Tension: magnitude along rope/string
- Spring: F = −kx (Hooke's law, restoring force)

**Atwood machine, inclined planes, connected objects:** draw free-body diagram per object, write Newton's 2nd for each, solve simultaneously.

**Trap:** Normal force does NOT always equal mg. On an incline: N = mg cos θ.

---

## 3. Work, Energy, Power

**Work:** W = **F**·**d** = Fd cos θ (dot product)
- For variable force: W = ∫ F(x) dx

**Kinetic energy:** K = ½mv²

**Work-energy theorem:** W_net = ΔK = K_f − K_i

**Potential energy:**
- Gravitational: U_g = mgh (reference at h = 0)
- Spring: U_s = ½kx²

**Conservation of mechanical energy** (no friction/non-conservative forces):
E = K + U = constant → K_i + U_i = K_f + U_f

**Non-conservative forces:** W_nc = ΔE = ΔK + ΔU

**Power:** P = dW/dt = **F**·**v** = Fv cos θ (units: Watts = J/s)

---

## 4. Momentum & Collisions

**Linear momentum:** **p** = m**v**

**Impulse-momentum theorem:** **J** = Δ**p** = ∫**F** dt = **F**_avg · Δt

**Conservation of momentum:** If Σ**F**_ext = 0, then **p**_total = constant.

**Types of collisions:**
- **Elastic:** both momentum AND kinetic energy conserved
  - For 1D equal masses: velocities exchange
  - General 1D: v₁' = (m₁−m₂)v₁/(m₁+m₂), v₂' = 2m₁v₁/(m₁+m₂)
- **Perfectly inelastic:** momentum conserved, objects stick; (m₁+m₂)v_f = m₁v₁ + m₂v₂
- **Inelastic:** momentum conserved, KE not conserved

**Center of mass:** **r**_cm = Σmᵢ**rᵢ** / M; **v**_cm = Σmᵢ**vᵢ** / M

---

## 5. Rotational Dynamics

**Analogies with linear motion:**

| Linear | Rotational |
|--------|-----------|
| x (position) | θ (angle) |
| v = dx/dt | ω = dθ/dt |
| a = dv/dt | α = dω/dt |
| F = ma | τ = Iα |
| KE = ½mv² | KE_rot = ½Iω² |
| p = mv | L = Iω |

**Torque:** τ = r × F = rF sin θ (r from pivot to point of application)

**Moment of inertia:** I = Σmᵢrᵢ² = ∫r² dm
- Solid disk/cylinder: I = ½MR²
- Hollow cylinder/ring: I = MR²
- Solid sphere: I = 2/5 MR²
- Thin rod (about center): I = 1/12 ML²
- Thin rod (about end): I = 1/3 ML²

**Parallel axis theorem:** I = I_cm + Md²

**Angular momentum:** **L** = I**ω** = **r** × **p**; τ_net = dL/dt

**Conservation of L:** If τ_net = 0, L = constant. (Ice skater pulling in arms: I decreases, ω increases.)

**Rolling without slipping:** v_cm = ωR, a_cm = αR
Total KE = ½mv_cm² + ½Iω²

---

## 6. Simple Harmonic Motion (SHM)

**Condition:** Restoring force F = −kx (linear restoring force)

**Solution:** x(t) = A cos(ωt + φ)

**Key quantities:**
- ω = 2π/T = 2πf (angular frequency)
- A = amplitude
- T = 2π/ω (period)
- v(t) = −Aω sin(ωt + φ); v_max = Aω
- a(t) = −Aω² cos(ωt + φ) = −ω²x

**Mass-spring:** ω = √(k/m); T = 2π√(m/k)

**Simple pendulum (small angle):** ω = √(g/L); T = 2π√(L/g)

**Energy in SHM:** E = ½kA² = ½mv_max² (constant)
At position x: K = ½m ω²(A²−x²), U = ½kx²

---

## 7. Gravitation

**Newton's law of gravitation:** F = Gm₁m₂/r² (G = 6.674×10⁻¹¹ N·m²/kg²)

**Gravitational potential energy:** U = −Gm₁m₂/r (zero at r = ∞)

**Orbital mechanics (circular orbit):** Gravitational force = centripetal force
Gm₁m₂/r² = m₂v²/r → v = √(Gm₁/r)

**Escape velocity:** v_esc = √(2GM/R) (KE = |U|)

**Kepler's laws:**
1. Elliptical orbits, sun at one focus
2. Equal areas in equal times (conservation of L)
3. T² ∝ a³: T²/a³ = 4π²/(GM) (a = semi-major axis)

---

## Constants & Conversions
- g = 9.8 m/s² (use 10 for quick estimates)
- G = 6.674×10⁻¹¹ N·m²/kg²
- 1 rev = 2π rad; 1 rpm = 2π/60 rad/s

## Common Traps on SP211 Exams
- Newton's 3rd: action-reaction pairs are on DIFFERENT objects — don't add them
- Energy conservation: only valid with no non-conservative forces (friction, applied force)
- Rotational KE: rolling objects have BOTH translational AND rotational KE
- Moment of inertia: always depends on axis choice
- SHM period: does NOT depend on amplitude (for ideal systems)
