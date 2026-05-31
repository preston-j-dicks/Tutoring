# Calculus III — Concept Reference
**Target:** USNA Validation Exam (MC + free response, ~Plebe Summer Week 2–3)

---

## 1. Vectors & 3D Geometry

**Vectors in R³:** **v** = ⟨a, b, c⟩

**Operations:**
- Dot product: **u**·**v** = u₁v₁ + u₂v₂ + u₃v₃ = |**u**||**v**|cos θ
- Cross product: **u** × **v** = ⟨u₂v₃−u₃v₂, u₃v₁−u₁v₃, u₁v₂−u₂v₁⟩ (use 3×3 determinant)
- |**u** × **v**| = |**u**||**v**|sin θ (magnitude = area of parallelogram)

**Key facts:**
- **u**·**v** = 0 ↔ perpendicular; **u** × **v** = **0** ↔ parallel
- Projection of **u** onto **v**: proj_**v**(**u**) = ((**u**·**v**)/|**v**|²)**v**
- Scalar projection: comp_**v**(**u**) = (**u**·**v**)/|**v**|

**Lines:** **r**(t) = **r₀** + t**d** (point + direction vector)

**Planes:** n₁(x−x₀) + n₂(y−y₀) + n₃(z−z₀) = 0, where **n** = ⟨n₁,n₂,n₃⟩ is normal vector.
- Distance from point (x₁,y₁,z₁) to plane ax+by+cz = d: |ax₁+by₁+cz₁−d| / √(a²+b²+c²)

**Quadric surfaces (recognize these):**
- Ellipsoid: x²/a² + y²/b² + z²/c² = 1
- Paraboloid: z = x²/a² + y²/b²
- Hyperboloid of one sheet: x²/a² + y²/b² − z²/c² = 1
- Cone: z² = x²/a² + y²/b²

---

## 2. Partial Derivatives

**Partial derivative ∂f/∂x:** Differentiate with respect to x, treat all other variables as constants.

**Mixed partials (Clairaut's theorem):** f_xy = f_yx (if continuous)

**Gradient:** ∇f = ⟨∂f/∂x, ∂f/∂y, ∂f/∂z⟩
- Points in direction of steepest ascent
- |∇f| = rate of steepest increase
- ∇f is perpendicular to level curves/surfaces

**Directional derivative:** D_**u**f = ∇f · **û** (unit vector **û**)
- Maximum value = |∇f| (in direction of ∇f)
- Zero in directions tangent to level curves

**Tangent plane to z = f(x,y) at (a,b):**
z − f(a,b) = fₓ(a,b)(x−a) + f_y(a,b)(y−b)

**Chain rule (multivariable):**
dz/dt = (∂z/∂x)(dx/dt) + (∂z/∂y)(dy/dt)

---

## 3. Optimization in Several Variables

**Critical points:** ∇f = **0** (both fₓ = 0 and f_y = 0)

**Second derivative test:** D = fₓₓf_yy − (fₓy)²
- D > 0, fₓₓ > 0 → local minimum
- D > 0, fₓₓ < 0 → local maximum
- D < 0 → saddle point
- D = 0 → inconclusive

**Lagrange multipliers** (constrained optimization):
Maximize/minimize f(x,y) subject to g(x,y) = 0:
∇f = λ∇g (plus constraint equation)
Set up system: fₓ = λgₓ, f_y = λg_y, g = 0. Solve for x, y, λ.

---

## 4. Multiple Integrals

**Double integral:** ∬_D f(x,y) dA

**Fubini's theorem:** ∬ f dA = ∫ₐᵇ ∫_{g₁(x)}^{g₂(x)} f(x,y) dy dx (for type I region)

**Polar coordinates:** dA = r dr dθ
∬_D f dA = ∫_α^β ∫₀^{r(θ)} f(r cos θ, r sin θ) · r dr dθ

**Triple integrals** in Cartesian, cylindrical, or spherical coordinates.

**Cylindrical:** x = r cos θ, y = r sin θ, z = z; dV = r dz dr dθ

**Spherical:** x = ρ sin φ cos θ, y = ρ sin φ sin θ, z = ρ cos φ
dV = ρ² sin φ dρ dφ dθ

**Jacobian for change of variables:**
∬_{D} f(x,y) dA = ∬_{D*} f(x(u,v), y(u,v)) |J| du dv
where J = |∂(x,y)/∂(u,v)| = |xᵤy_v − x_vy_u|

---

## 5. Line Integrals

**Scalar line integral:** ∫_C f ds = ∫ₐᵇ f(**r**(t)) |**r**'(t)| dt

**Vector line integral (work):** ∫_C **F** · d**r** = ∫ₐᵇ **F**(**r**(t)) · **r**'(t) dt

**Conservative fields:** **F** = ∇f ↔ ∮_C **F**·d**r** = 0 for all closed C
- Test: ∂P/∂y = ∂Q/∂x (in 2D)
- If conservative: ∫_C **F**·d**r** = f(end) − f(start) (path independent)

---

## 6. Green's, Stokes', and Divergence Theorems

### Green's Theorem (2D — boundary of region to area integral)
∮_C P dx + Q dy = ∬_D (∂Q/∂x − ∂P/∂y) dA

C is positively oriented (counterclockwise) simple closed curve, D is its interior.

**Use for:** Computing line integrals over closed curves by converting to double integrals (or vice versa).

### Stokes' Theorem (3D — boundary of surface to surface integral)
∮_C **F**·d**r** = ∬_S (∇×**F**)·d**S**

**F** is a vector field on surface S with boundary curve C.
- ∇×**F** (curl) = ⟨Ry−Qz, Pz−Rx, Qx−Py⟩ for **F** = ⟨P,Q,R⟩

### Divergence (Gauss's) Theorem (3D — boundary of volume to volume integral)
∯_S **F**·d**S** = ∭_E (∇·**F**) dV

E is a solid region with boundary surface S (outward normal).
- ∇·**F** (divergence) = ∂P/∂x + ∂Q/∂y + ∂R/∂z

### Surface Integrals
For surface z = g(x,y):
∬_S **F**·d**S** = ∬_D **F**·⟨−gₓ, −g_y, 1⟩ dA (upward normal)
∬_S f dS = ∬_D f √(gₓ² + g_y² + 1) dA

---

## Summary of Theorem Relationships

| Theorem | Dimension | Boundary → Interior |
|---------|-----------|---------------------|
| FTC | 1D | endpoints → interval |
| Green's | 2D | closed curve → region |
| Stokes' | 3D | closed curve → surface |
| Divergence | 3D | closed surface → volume |

---

## Common Traps on Calc III Exams
- Cross product is not commutative: **u**×**v** = −(**v**×**u**)
- For gradient: don't forget to evaluate at the given point
- Double integrals: set up limits of integration carefully from the region description
- Green's theorem: curve must be positively oriented (counterclockwise)
- Stokes': orientation of C must be consistent with normal of S (right-hand rule)
- Divergence theorem: S must be closed (complete boundary of a solid)
