# Physics — Electromagnetism (SP212-track)
**Target:** USNA SP212 Validation (requires SP211 first) — lighter section, flagged accordingly

> **SP212 prerequisite note:** Will needs SP211 validated before sitting SP212. This section is for awareness and long-range prep. Focus sessions on SP211 mechanics first.

---

## 1. Electric Force & Field (Coulomb's Law)

**Coulomb's Law:**
F = k|q₁||q₂|/r²
where k = 1/(4πε₀) = 8.99×10⁹ N·m²/C², ε₀ = 8.85×10⁻¹² C²/(N·m²)

Direction: like charges repel, unlike charges attract (along line joining charges).

**Electric field E** (force per unit positive test charge):
**E** = **F**/q = k|q|/r² r̂ (radially outward for +q)

For multiple charges: **E**_total = Σ**Eᵢ** (vector sum — superposition)

**Electric field lines:** start at +, end at −; never cross; closer = stronger field.

---

## 2. Electric Potential

**Electric potential V** (scalar, energy per charge):
V = kq/r (single point charge)
V = U/q (potential energy per charge)

**Relation to field:** E = −dV/dx (1D); **E** = −∇V (3D)
- Field points from high V to low V

**Work done by field moving charge q:** W = q(V_A − V_B) = −ΔU

**Equipotential surfaces** are perpendicular to field lines.

---

## 3. Gauss's Law

∮ **E**·d**A** = Q_enc/ε₀

**Use for high-symmetry geometries:**
- Spherical symmetry: E = kQ/r² (outside sphere), E = kQr/R³ (inside uniform sphere)
- Infinite line charge (λ): E = λ/(2πε₀r)
- Infinite plane (σ): E = σ/(2ε₀)

---

## 4. Capacitance

**Definition:** C = Q/V (units: Farads = C/V)

**Parallel-plate capacitor:** C = ε₀A/d

**With dielectric:** C = κε₀A/d (κ = dielectric constant > 1)

**Energy stored:** U = ½CV² = Q²/(2C) = ½QV

**Series:** 1/C_eq = 1/C₁ + 1/C₂ + ··· (same Q, voltages add)
**Parallel:** C_eq = C₁ + C₂ + ··· (same V, charges add)

---

## 5. DC Circuits

**Ohm's Law:** V = IR (R = resistance, units: Ohms)

**Resistivity:** R = ρL/A

**Power dissipated:** P = IV = I²R = V²/R

**Kirchhoff's Laws:**
- **KVL (loop):** Sum of voltage drops around any closed loop = 0
- **KCL (node):** Sum of currents into a node = sum out

**Series:** R_eq = R₁ + R₂ + ··· (same I)
**Parallel:** 1/R_eq = 1/R₁ + 1/R₂ + ··· (same V)

**RC circuits:**
- Charging: q(t) = Cε(1 − e^{−t/τ}); τ = RC
- Discharging: q(t) = q₀ e^{−t/τ}
- At t = τ: reaches ~63% of final (charging) or drops to ~37% (discharging)

---

## 6. Magnetic Fields

**Magnetic force on moving charge:**
**F** = q**v** × **B** (magnitude: F = qvB sin θ)

**Magnetic force on current-carrying wire:**
**F** = I**L** × **B** (magnitude: F = BIL sin θ)

**No work done by magnetic force** (always perpendicular to velocity).

**Circular motion in magnetic field:** qvB = mv²/r → r = mv/(qB)

**Biot-Savart Law:** d**B** = (μ₀/4π) (I d**L** × r̂)/r²

**Ampere's Law:** ∮ **B**·d**L** = μ₀ I_enc
- Infinite wire: B = μ₀I/(2πr)
- Solenoid: B = μ₀nI (n = turns/length; inside only)

μ₀ = 4π×10⁻⁷ T·m/A

---

## 7. Faraday's Law & Induction

**Magnetic flux:** Φ_B = ∬ **B**·d**A** = BA cos θ (uniform B through area A)

**Faraday's Law:** ε = −dΦ_B/dt (induced EMF equals negative rate of flux change)

**Lenz's Law:** Induced current opposes the change in flux (determines direction).

**Motional EMF:** ε = BLv (conductor of length L moving at speed v perpendicular to B)

**Inductance:** L = NΦ_B/I (Henry); solenoid: L = μ₀n²V = μ₀N²A/ℓ

**RL circuit:** time constant τ = L/R; I(t) = (ε/R)(1 − e^{−t/τ})

---

## Maxwell's Equations (Summary)
1. Gauss (E): ∮ **E**·d**A** = Q_enc/ε₀
2. Gauss (B): ∮ **B**·d**A** = 0 (no magnetic monopoles)
3. Faraday: ∮ **E**·d**L** = −dΦ_B/dt
4. Ampere-Maxwell: ∮ **B**·d**L** = μ₀(I + ε₀ dΦ_E/dt)

---

## Common Traps on SP212 Exams
- Coulomb's law: force direction from the line joining charges, direction depends on sign product
- Capacitors in series: 1/C_eq (NOT just sum); parallel: add directly
- V at a point from multiple charges: scalar sum (not vector)
- Magnetic force does NO work
- Faraday's law: the NEGATIVE sign is Lenz's law — direction matters
- RC/RL time constants: at t = τ, NOT fully charged/discharged
