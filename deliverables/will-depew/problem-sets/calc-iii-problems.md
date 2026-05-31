# Calculus III — Problem Set
**USNA Validation Prep** | Includes free-response style problems (mirrors Calc III exam format)

---

## Section 1: Vectors & 3D Geometry (Easy)

**1.** Let **u** = ⟨2, −1, 3⟩ and **v** = ⟨1, 4, −2⟩.
(a) Compute **u**·**v**.
(b) Find |**u**| and |**v**|.
(c) Find the angle between **u** and **v**.
(d) Compute **u** × **v**.
(e) Verify **u** × **v** is perpendicular to both **u** and **v**.

**2.** Find the equation of the plane through the points P(1, 2, 0), Q(3, 1, −1), R(0, 3, 2).

**3.** Find the parametric equations of the line through (2, −1, 3) parallel to **v** = ⟨4, −2, 1⟩.

**4.** Find the distance from the point (3, 1, −1) to the plane 2x − y + 2z = 4.

---

## Section 2: Partial Derivatives & Gradients (Medium)

**5.** For f(x, y) = x³y − 2xy² + y³:
(a) Find fₓ, f_y.
(b) Find fₓₓ, f_yy, fₓy.
(c) Verify Clairaut's theorem: fₓy = f_yₓ.

**6.** For f(x, y) = e^(xy) sin(x):
(a) Find ∂f/∂x.
(b) Find the gradient ∇f at (π, 0).

**7.** Find the directional derivative of f(x, y, z) = x²yz at (1, 1, 2) in the direction of **v** = ⟨1, 2, 2⟩.

**8.** Find the tangent plane to the surface z = x² + y² − 2xy at the point (1, 2, 1).

---

## Section 3: Optimization (Medium)

**9.** Find and classify all critical points of f(x, y) = x³ − 3x + y² − 2y.

**10.** Find the maximum and minimum values of f(x, y) = 2x + 3y subject to the constraint x² + y² = 1 using Lagrange multipliers.

**11.** A rectangular box (no top) is to have volume 32 cm³. Find the dimensions that minimize surface area.

---

## Section 4: Multiple Integrals (Medium–Hard)

**12.** Evaluate ∬_D (x + y) dA where D is the triangle with vertices (0,0), (2,0), (0,2).

**13.** Evaluate ∬_D x² + y² dA where D is the disk x² + y² ≤ 4 (use polar coordinates).

**14.** Set up and evaluate the triple integral ∭_E z dV where E is the region under z = 4 − x² − y² and above the xy-plane.

**15.** Convert to polar and evaluate: ∬_D e^(−x²−y²) dA where D is the quarter disk x ≥ 0, y ≥ 0, x² + y² ≤ 9.

---

## Section 5: Vector Calculus (Hard)

**16.** Let **F**(x, y) = ⟨2xy, x² + 3y²⟩.
(a) Show **F** is conservative.
(b) Find a potential function f such that **F** = ∇f.
(c) Evaluate ∫_C **F**·d**r** where C is any path from (0,0) to (2,1).

**17.** Evaluate ∫_C y² dx + 2xy dy where C is the upper half of the unit circle from (1,0) to (−1,0). (Hint: check if conservative, then choose a simpler path or use Green's theorem.)

**18.** Use Green's theorem to evaluate ∮_C (y²) dx + (x + 2y) dy, where C is the boundary of the rectangle [0,3] × [0,2] oriented counterclockwise.

**19.** Let **F** = ⟨x², y², z²⟩. Use the Divergence theorem to compute ∯_S **F**·d**S** where S is the closed surface bounding the cube [0,2]³.

---

## Free-Response Style (Mirrors USNA Calc III Exam)

**FR-1.** (20 points)
Let f(x, y) = 4 − x² − y².

(a) [4 pts] Find the domain and range of f. Describe the level curves.

(b) [4 pts] Compute ∇f at the point (1, 1). In what direction is f increasing most rapidly from (1, 1)? What is the maximum rate of increase?

(c) [6 pts] Find the equation of the tangent plane to the surface z = f(x,y) at (1, 1, 2).

(d) [6 pts] Set up but do not evaluate the integral for the volume of the region below z = f(x, y) and above the xy-plane, using polar coordinates.

**FR-2.** (20 points)
Let **F**(x, y, z) = ⟨xz, yz, −(x² + y²)/2⟩.

(a) [6 pts] Compute ∇·**F** (divergence) and ∇×**F** (curl).

(b) [8 pts] Use the Divergence theorem to compute ∯_S **F**·d**S** where S is the sphere x² + y² + z² = 4.

(c) [6 pts] Is **F** conservative? Justify your answer using the curl test.
