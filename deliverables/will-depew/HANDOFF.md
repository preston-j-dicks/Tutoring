# HANDOFF — Will Depew Onboarding
**Prepared:** 2026-05-31 | **Session tonight:** 8:00 PM Zoom

---

## What Was Built

### Student Infrastructure
| Item | Status | Detail |
|------|--------|--------|
| FLAB Token | Generated | `FLAB-W4DP-2KXN-7MBT` |
| Student page | Created | `students/will-depew/index.html` — lives at `fissionlab.net/students/will-depew/` after push |
| Stripe pay link | SCAFFOLDED (not live) | See NEEDS DR. PRESTON — placeholder in student page |
| Railway DB entry | NOT DONE | See NEEDS DR. PRESTON |
| HF app access | NOT DONE | See NEEDS DR. PRESTON |

### Deliverables (all in `deliverables/will-depew/`)
```
concept-sheets/
  calc-i.md           — Limits, derivatives, optimization, FTC, basic integration
  calc-ii.md          — Integration techniques, series, power/Taylor, parametric/polar
  calc-iii.md         — Vectors, partial derivatives, multiple integrals, Green/Stokes/Divergence
  physics-mechanics.md — Kinematics, Newton's laws, energy, momentum, rotation, SHM, gravitation
  physics-em.md       — Coulomb, Gauss, potential, capacitance, circuits, magnetism, induction

problem-sets/
  calc-i-problems.md + calc-i-solutions.md
  calc-ii-problems.md + calc-ii-solutions.md
  calc-iii-problems.md + calc-iii-solutions.md     ← includes 2 free-response problems
  physics-mechanics-problems.md + physics-mechanics-solutions.md
  physics-em-problems.md + physics-em-solutions.md

session-plan-tonight.md   — 60-90 min tutor plan (diagnostic, priorities, study roadmap)
welcome-message.md        — Student-facing welcome, token, links, payment note
HANDOFF.md                — This file
```

### RAG Status
The `fissionlab-rag` MCP server returned a numpy pickle error on all queries (`allow_pickle=False`). Materials were generated from direct knowledge. All formulas verified manually — flag if anything needs double-checking.

Fix: run `python -c "import numpy as np; np.load('inv_vals.npy', allow_pickle=True)"` in the RAG server directory to diagnose, or re-index with `allow_pickle=True`.

---

## Links

| Item | URL |
|------|-----|
| Student page | https://fissionlab.net/students/will-depew/ |
| Portal fallback | https://web-production-202b9.up.railway.app/portal/FLAB-W4DP-2KXN-7MBT |
| Math app | https://dr-p-math-app.hf.space |
| Physics app | https://dr-p-physics-app.hf.space |
| Zoom (tonight) | https://us06web.zoom.us/j/2231043731 (passcode: Fm9si3) |
| Calendly | https://calendly.com/preston-j-dicks/1hr-session |

---

## NEEDS DR. PRESTON

- **Will's email** — NOT found anywhere in the repo. He said he submitted a request via fissionlab — check Railway admin panel / portal for any pending access request or signup record with "Depew" or "Will". Recover his email from there.

- **Rate confirmation** — Will is a returning student (previous work was essays). Standard rate for returning students appears to be ~$70/hr (same as Aarush). Confirm whether he gets a grandfathered rate or standard. Once confirmed:
  1. Create a per-student Stripe payment link via `stripe_products.py` or Stripe dashboard
  2. Replace `PLACEHOLDER_WILL_DEPEW` in `students/will-depew/index.html` with the real link

- **Railway DB registration** — The HF apps (math-app, physics-app) verify tokens against `https://web-production-202b9.up.railway.app/api/verify`. Will's token `FLAB-W4DP-2KXN-7MBT` must be inserted into the Railway PostgreSQL `students` table for the apps to work. Log in to the Railway admin console and run:
  ```sql
  INSERT INTO students (name, token, subjects, active)
  VALUES ('William Depew', 'FLAB-W4DP-2KXN-7MBT', 'Calculus (I-III), Physics', true);
  ```
  (Adjust column names to match actual schema — check Railway console.)

- **Portal deep-link** — `portal.fissionlab.net/portal/FLAB-W4DP-2KXN-7MBT` will work once token is in Railway DB. Verify whether portal.fissionlab.net DNS is resolving; if not, use fallback URL above.

- **Pending request / Calendly booking** — Will said he submitted a contact request via fissionlab. Check Railway portal for pending signup rows, and check Calendly for any booking from "Depew" or "Will" in the last 7 days. His email should be there.

- **Stripe pay link** — Per-student links follow the pattern `buy.stripe.com/[unique_id]`. Generate one via Stripe dashboard (create a payment link for a one-time session at confirmed rate) and update the student page.

---

## Tonight's Priority Order

1. Run the diagnostic (5 warm-up problems in session plan)
2. Based on results: front-load Calc I if rusty (exam is Day 1–2 of Plebe Summer)
3. Cover the study roadmap: 3.5 weeks → Calc I complete by June 7, Calc III by June 21
4. Get Will's email during the session if not recovered before

---

## Notes
- Will is a sharp kid — essay work showed strong written reasoning. Expect math to come back quickly.
- USNA uses its own versions of these exams, not AP. Calc I is apparently ~70% pass rate (relatively accessible). Calc III with free-response is the harder bar.
- Commit hash and push status logged below after Phase 5.
