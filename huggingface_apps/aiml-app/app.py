# HuggingFace Space: Dr-P/aiml-app
# Live URL: https://dr-p-aiml-app.hf.space
# Rebuilt: OTS Commission Roadmap + AI/ML Technical Foundation

import os
import re
import random
import requests
import gradio as gr

PORTAL_VERIFY_URL = "https://web-production-202b9.up.railway.app/api/verify"
TOKEN_PATTERN = re.compile(r"^FLAB-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", re.IGNORECASE)
FREE_Q_LIMIT = 10

try:
    import anthropic
    ANTHROPIC_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
    HAS_ANTHROPIC = bool(ANTHROPIC_KEY)
except ImportError:
    HAS_ANTHROPIC = False

OTS_SYSTEM_PROMPT = (
    "You are Dr. Preston's AI assistant helping a student prepare for a commission via "
    "Officer Training School (OTS). Answer questions about AFSC selection using the Air Force "
    "Officer Classification Directory (AFOCD), OTS application requirements, competitive package "
    "components, AFOQT preparation, and AI/ML concepts. Be specific — give real score benchmarks, "
    "real timelines, real eligibility requirements. If you don't know a current figure, say so "
    "and tell the user where to verify it (afpc.af.mil, af.mil). Never fabricate statistics."
)

def verify_token(token: str) -> bool:
    token = token.strip().upper()
    if not TOKEN_PATTERN.match(token):
        return False
    try:
        r = requests.post(PORTAL_VERIFY_URL, json={"token": token}, timeout=5)
        if r.status_code == 200 and r.json().get("valid"):
            return True
    except Exception:
        pass
    return False

# ── AI/ML Quiz Bank ────────────────────────────────────────────────────────────
ML_QUESTIONS = [
    {"q": "Which best describes the bias-variance tradeoff?",
     "choices": ["A) High bias = overfit; high variance = underfit",
                 "B) High bias = underfit; high variance = overfit",
                 "C) Both decrease with more data",
                 "D) Bias and variance always move together"],
     "answer": 1, "topic": "ML Fundamentals",
     "explanation": "High bias = underfitting (model too simple). High variance = overfitting (model too complex)."},
    {"q": "k-fold cross-validation with k=5 and 1000 samples: how many samples per validation fold?",
     "choices": ["A) 50", "B) 100", "C) 200", "D) 500"],
     "answer": 2, "topic": "ML Fundamentals",
     "explanation": "1000/5 = 200 samples per fold. 4 folds train, 1 fold validates."},
    {"q": "L1 regularization (Lasso) produces what kind of model?",
     "choices": ["A) Many small weights", "B) Sparse model with zero weights",
                 "C) Equal-magnitude weights", "D) Outlier-resistant model"],
     "answer": 1, "topic": "ML Fundamentals",
     "explanation": "L1 adds |w| penalty, driving many weights to exactly zero — useful for feature selection."},
    {"q": "Confusion matrix: TP=80, FP=20, FN=10, TN=90. What is precision?",
     "choices": ["A) 0.80", "B) 0.89", "C) 0.75", "D) 0.88"],
     "answer": 0, "topic": "ML Fundamentals",
     "explanation": "Precision = TP/(TP+FP) = 80/100 = 0.80."},
    {"q": "Which algorithm makes no assumptions about data distribution?",
     "choices": ["A) Linear Regression", "B) Logistic Regression",
                 "C) K-Nearest Neighbors", "D) Naive Bayes"],
     "answer": 2, "topic": "ML Fundamentals",
     "explanation": "KNN is non-parametric — predictions based on proximity without assuming functional form."},
    {"q": "PCA finds directions of maximum:",
     "choices": ["A) Mean", "B) Variance", "C) Correlation", "D) Covariance with labels"],
     "answer": 1, "topic": "ML Fundamentals",
     "explanation": "PCA finds orthogonal directions of maximum variance for dimensionality reduction."},
    {"q": "Vanishing gradient problem means:",
     "choices": ["A) Gradients explode to infinity",
                 "B) Gradients become very small, slowing early-layer learning",
                 "C) Model forgets earlier examples",
                 "D) Weights oscillate without converging"],
     "answer": 1, "topic": "Deep Learning",
     "explanation": "Gradients shrink exponentially through many layers, making early layers learn very slowly."},
    {"q": "Softmax output for inputs [2, 1, 0] (approximate)?",
     "choices": ["A) [0.67, 0.24, 0.09]", "B) [0.50, 0.25, 0.25]",
                 "C) [1.0, 0.5, 0.0]", "D) [0.33, 0.33, 0.33]"],
     "answer": 0, "topic": "Deep Learning",
     "explanation": "exp(2)≈7.39, exp(1)≈2.72, exp(0)=1. Sum≈11.11. Outputs≈[0.665, 0.245, 0.090]."},
    {"q": "Convolution: input 32×32×3, kernel 5×5×3, 16 filters, no padding. Output shape?",
     "choices": ["A) 28×28×16", "B) 32×32×16", "C) 28×28×3", "D) 30×30×16"],
     "answer": 0, "topic": "Deep Learning",
     "explanation": "(32-5+1)=28. With 16 filters: output is 28×28×16."},
    {"q": "Transformer attention scores computed as:",
     "choices": ["A) softmax(Q·Kᵀ/√d_k)·V", "B) softmax(Q·V/√d_k)·K",
                 "C) Q·Kᵀ·V", "D) sigmoid(Q+K)·V"],
     "answer": 0, "topic": "Deep Learning",
     "explanation": "Scaled dot-product attention: Attention(Q,K,V) = softmax(QKᵀ/√d_k)V."},
    {"q": "np.dot(A, B) where A is (3,4) and B is (4,2) returns shape:",
     "choices": ["A) (3,4)", "B) (3,2)", "C) (4,4,2)", "D) scalar"],
     "answer": 1, "topic": "Python/NumPy",
     "explanation": "Matrix multiplication: (3,4)·(4,2) = (3,2)."},
    {"q": "np.array([1,2,3,4,5])[::2] returns:",
     "choices": ["A) [1,3,5]", "B) [2,4]", "C) [1,2]", "D) [3,4,5]"],
     "answer": 0, "topic": "Python/NumPy",
     "explanation": "Step-2 slice: indices 0,2,4 → [1,3,5]."},
    {"q": "Set membership x in my_set time complexity:",
     "choices": ["A) O(n)", "B) O(log n)", "C) O(1) average", "D) O(n²)"],
     "answer": 2, "topic": "Python/NumPy",
     "explanation": "Python sets use hash tables — O(1) average for membership testing."},
    {"q": "P(A|B) by Bayes' theorem equals:",
     "choices": ["A) P(B|A)·P(A)/P(B)", "B) P(A)·P(B)",
                 "C) P(A∩B)/P(A)", "D) P(B|A)/P(A)"],
     "answer": 0, "topic": "Probability & Statistics",
     "explanation": "Bayes: P(A|B) = P(B|A)·P(A)/P(B). Fundamental to probabilistic ML."},
    {"q": "Best metric for 99%/1% class imbalance:",
     "choices": ["A) Accuracy", "B) F1 Score", "C) MSE", "D) R-squared"],
     "answer": 1, "topic": "Probability & Statistics",
     "explanation": "F1 handles imbalance better — accuracy is misleadingly high predicting only majority class."},
]

# ── OTS Module Content ─────────────────────────────────────────────────────────
MODULE_CONTENT = {
    "Module 1: Is OTS Right for You?": """
## Is OTS Right for You?

### Commissioning Path Comparison

| Path | Duration | Best For |
|------|----------|----------|
| **OTS** | 9.5 weeks (Maxwell AFB) | College graduates with prior experience |
| **ROTC** | 4 years | Students currently in college |
| **Academy** | 4 years | Competitive HS grads wanting full military education |

### OTS Eligibility (as of 2025–2026)
- **Age**: 18–39 (varies by component; waivers possible)
- **Degree**: Bachelor's degree from accredited institution
- **GPA**: No minimum, but competitive packages typically 3.0+
- **Medical**: Must pass MEPS; DQ conditions reviewed case by case
- **Citizenship**: U.S. citizen

### Typical Timeline (application to commissioning)
1. **AFOQT** (can take months to schedule): ~2–4 months before applying
2. **Package assembly**: 3–6 months (LORs, transcripts, personal statement)
3. **Board review**: Boards convene several times per year; wait 2–4 months for results
4. **OTS class date**: Typically 3–9 months after selection
5. **OTS itself**: 9.5 weeks at Maxwell AFB, Alabama
6. **TFOT → commissioning**: Receive commission as second lieutenant (O-1)

### What Makes a Competitive Package in 2026
- **Degree**: STEM degrees are highly competitive, especially for technical AFSCs
- **GPA**: 3.5+ is competitive; 3.0–3.4 is average
- **AFOQT scores**: PCSM matters for pilot; Verbal + Quantitative matter for most others
- **LORs**: Officers > civilians; people who know your work > people who know your name
- **Personal statement**: Specific, honest, shows you understand what you're getting into
- **Community involvement / leadership**: Concrete examples beat vague claims

Use the **Q&A tab** to ask Dr. Preston's AI assistant specific questions about your situation.
""",
    "Module 2: AFSC Selection": """
## AFSC Selection via the AFOCD

The Air Force Officer Classification Directory (AFOCD) is the authoritative source for AFSC requirements.
**Find the latest version at**: afpc.af.mil → Officer Assignments → AFOCD

### How to Read an AFOCD Entry
Each AFSC entry contains:
- **Specialty Summary**: What officers in this AFSC actually do
- **Mandatory Qualifications**: Hard requirements (degree type, clearance, medical)
- **Desired Qualifications**: Competitive differentiators
- **Physical Requirements**: Vision, fitness standards
- **Special Experience Identifiers (SEIs)**: Advanced quals you can earn post-commission

### Top AFSCs for STEM / AI/ML Backgrounds

| AFSC | Title | Why It Fits |
|------|-------|-------------|
| **61D** | Developmental Scientist | Research & development; PhD highly valued |
| **62E** | Developmental Engineer | Engineering project management |
| **17D** | Cyberspace Operations | Software/network background |
| **13S** | Space Operations | Physics/math heavy; growing field |
| **14N** | Intelligence | Analytical, data-driven |
| **61A** | Physicist | Basic research; matches physics PhD track |

### Interactive AFSC Recommender
Use the **Q&A tab** to describe your degree, GPA, and interests.
Ask: *"I have a BS in Physics with a 3.7 GPA and am interested in AI research — what AFSCs should I target?"*

The assistant will walk you through the AFOCD logic and recommend 3–5 AFSCs to research.
""",
    "Module 3: Building Your Package": """
## Building a Competitive OTS Package

### The Non-Negotiables
- **Official transcripts** from every college attended (even transfer credits)
- **AFOQT scores** (sent directly from testing center — allow 4–6 weeks)
- **Birth certificate / passport** (citizenship verification)
- **Medical records** if you have any flagged conditions

### Letters of Recommendation
Boards want to know: *Can this person lead people under stress?*

**Best LOR sources (ranked):**
1. Current active-duty or reserve officer who has observed your work
2. Senior civilian supervisor / faculty who can speak to leadership
3. Community leader or coach who observed character under pressure

**What to give your LOR writers:**
- Your resume and personal statement (so they can align messaging)
- Specific stories you want them to reference
- The AFSC you're targeting (they can speak to fit)

### Personal Statement / Biographical Sketch
- **Length**: Typically 1 page, single-spaced
- **What boards want**: Why this specific branch, why OTS, what you bring, what you know about the commitment
- **What kills packages**: Generic statements, vague claims, no evidence of research into military life

Use the **Q&A tab** to draft and iterate your personal statement with AI assistance.
Ask: *"Here is my draft personal statement: [paste it]. What should I strengthen?"*

### Fitness Test Standards
OTS requires passing the Air Force Fitness Assessment (FA). Current standards vary by age/gender — verify at **af.mil/Fitness** for the most current scorecard. Training for OTS: functional strength, 1.5-mile run, pushups, situps/crunches.
""",
    "Module 4: AFOQT Preparation": """
## AFOQT Preparation

The AFOQT has 12 subtests. Which scores matter depends on your target AFSC.

### Key Score Composites

| Composite | Subtests Included | Matters For |
|-----------|-------------------|-------------|
| **Verbal** | Verbal Analogies + Reading Comprehension | All officers |
| **Quantitative** | Arithmetic Reasoning + Math Knowledge | All officers; critical for technical AFSCs |
| **Academic Aptitude** | Verbal + Quantitative | All officers |
| **Pilot** | Math Knowledge + Instrument + Table Reading + Aviation + Verbal Analogies | Pilot candidates |
| **PCSM** | Pilot composite + flight hours + TBAS | Pilot selection (separate from AFOQT) |
| **Navigator** | Math + Instrument + Table Reading + Physical Science | CSO candidates |

### Competitive Score Benchmarks (by AFSC type)
*These are community benchmarks, not official minimums — verify with your recruiter.*

| Target | Verbal | Quantitative |
|--------|--------|--------------|
| Technical AFSC (61D/62E/17D) | 70+ | 70+ |
| Competitive package (any AFSC) | 60+ | 60+ |
| Minimum (general) | 50 | 50 |

### Access Dr. Preston's AFOQT Practice App
**→ [Open AFOQT Practice App](https://dr-p-afoqt-app.hf.space)**
*(Enter your FissionLab token for unlimited access)*

### 8-Week Study Plan
See the **8-Week Plan** sub-tab for a structured daily schedule.

Use the **Q&A tab** to ask: *"Which AFOQT subtests matter most for 61D (Developmental Scientist)?"*
""",
    "Module 5: OTS Experience": """
## What to Expect at OTS

Officer Training School is at **Maxwell AFB, Alabama**. Current program: ~9.5 weeks (verify at aetc.af.mil).

### Program Structure
**Weeks 1–2 (Transition Phase)**
- In-processing, uniforms, initial PT assessment
- Introduction to military customs and courtesies
- Significant adjustment period — intentional stress, sleep deprivation

**Weeks 3–5 (Academic Phase)**
- Leadership in Air and Space Power doctrine
- Laws of Armed Conflict, Air Force history
- Written exams and leadership practicums

**Weeks 6–8 (Leadership Phase)**
- Officer Trainees take on leadership roles within the flight
- Your peers evaluate you; the cadre evaluate how you lead
- Leadership reaction course, scenario-based exercises

**Week 9+ (Final Phase)**
- Graduation ceremonies
- Commission as Second Lieutenant (O-1)
- Report date for follow-on training (Undergraduate Pilot Training, tech school, etc.)

### What Distinguishes Honor Graduates
- Consistent academic performance (not a single peak)
- Leadership that other OTs actually trust — not just compliance
- PT scores in the upper range throughout, not just at baseline
- Composed under the intentional chaos of the program

### Life as a Newly Commissioned O-1
- Pay starts on commission date (O-1: ~$3,900/month base, 2025 scale — verify at militarypay.defense.gov)
- Follow-on training orders come before graduation
- Housing allowance (BAH) kicks in based on duty station zip code

Use the **Q&A tab** for specific questions about what to expect.
""",
    "Module 6: AI/ML Technical Foundation": """
## AI/ML Technical Foundation for Technical Officers

This module covers the AI and ML concepts most relevant to technical AFSCs (17D Cyber, 61D Scientist, 62E Engineer, 13S Space).

### Why ML Matters for Technical Officers
Modern defense systems are increasingly AI/ML-driven:
- **ISR systems**: Automated target recognition
- **Cyber**: Anomaly detection, threat classification
- **Space**: Satellite health monitoring, conjunction analysis
- **Logistics**: Predictive maintenance, supply chain optimization

### Core Concepts You Should Own

**Linear Algebra**
- Vectors as physical quantities (not just arrays of numbers)
- Matrix multiplication as transformation (not just dot products)
- Eigendecomposition — why PCA works

**Calculus for ML**
- Gradient as steepest-ascent direction — descent flips the sign
- Chain rule as backpropagation — the math isn't hard, the notation is
- Hessian — second-order information for optimization

**Probability**
- Bayes' theorem as the foundation of inference
- Maximum likelihood estimation
- Softmax = Boltzmann distribution (stat mech in disguise)

**Practice**
Use the **AI/ML Quiz tab** to test your knowledge across ML fundamentals, deep learning, Python/NumPy, and statistics.

**Go deeper**: Visit the [AI/ML Physics Intuition page](https://fissionlab.net/community/ai-ml/) on FissionLab.net for Dr. Preston's long-form explainers.
""",
}

CSS = """
body, .gradio-container { background: #0a1628 !important; color: #f0ebe0 !important; font-family: 'Georgia', serif; }
h1, h2, h3, h4 { color: #c9a84c !important; }
table { border-collapse: collapse; width: 100%; }
th { background: #0d1f3c; color: #c9a84c; padding: 8px; }
td { padding: 8px; border-bottom: 1px solid rgba(201,168,76,0.15); }
.gr-button-primary { background: #c9a84c !important; color: #0a1628 !important; font-weight: bold; border: none; }
.gr-button { border: 1px solid #c9a84c !important; color: #c9a84c !important; background: transparent !important; }
.gr-textbox, .gr-radio, .gr-box { background: #0d1f3c !important; color: #f0ebe0 !important; border-color: #c9a84c !important; }
label { color: #f0ebe0 !important; }
.authority { color: #c9a84c; font-size: 0.85em; text-align: center; margin-top: 4px; }
"""

EIGHT_WEEK_PLAN = """
## 8-Week AFOQT Study Plan

Weighted toward subtests critical for technical AFSCs (Verbal Analogies, Arithmetic Reasoning, Math Knowledge, Physical Science, Table Reading).

| Week | Focus | Daily Target (45–60 min) |
|------|-------|--------------------------|
| **1** | Baseline + Verbal Analogies | 30 analogies/day; identify weak patterns |
| **2** | Arithmetic Reasoning | 20 word problems/day; speed drill |
| **3** | Math Knowledge | 25 problems/day; algebra, geometry |
| **4** | Physical Science | 20 questions/day; kinematics, E&M, waves |
| **5** | Table Reading + Instrument Comprehension | 50 table lookups + 20 instrument reads/day |
| **6** | Verbal: Reading Comprehension + Word Knowledge | 2 passages + 30 word knowledge/day |
| **7** | Full mixed-subtest practice | 90-min timed section per day |
| **8** | Timed full-length practice tests | Rest 2 days before test day |

**Key resources:**
- [AFOQT Practice App — Dr. Preston](https://dr-p-afoqt-app.hf.space) (enter your FissionLab token)
- Barron's AFOQT Study Guide (print — most current)
- Khan Academy for Arithmetic Reasoning and Math Knowledge gaps

**Track your progress**: Take a baseline score on Day 1, Week 1. Re-score every Sunday.
"""

def new_quiz_session():
    shuffled = random.sample(ML_QUESTIONS, len(ML_QUESTIONS))
    return {"token_verified": False, "q_idx": 0, "score": 0, "answers": [], "free_used": 0, "questions": shuffled}

def get_question(session):
    qs = session["questions"]
    idx = session["q_idx"]
    return qs[idx] if idx < len(qs) else None

def fmt_score(session):
    return f"Score: {session['score']} / {session['q_idx']}" if session["q_idx"] > 0 else "Score: 0 / 0"

def submit_answer(choice_idx, session):
    if choice_idx is None:
        return session, "Please select an answer.", gr.update(), gr.update(visible=False), fmt_score(session)
    q = get_question(session)
    if q is None:
        return session, "Quiz complete!", gr.update(), gr.update(visible=False), fmt_score(session)
    correct = choice_idx == q["answer"]
    if correct:
        session["score"] += 1
    session["q_idx"] += 1
    if not session["token_verified"]:
        session["free_used"] += 1
    session["ans