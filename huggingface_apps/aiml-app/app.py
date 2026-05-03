# HuggingFace Space: Dr-P/aiml-app
# Live URL: https://dr-p-aiml-app.hf.space

import re
import requests
import random
import gradio as gr

PORTAL_VERIFY_URL = "https://web-production-202b9.up.railway.app/api/verify"
TOKEN_PATTERN = re.compile(r"^FLAB-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}$", re.IGNORECASE)
FREE_Q_LIMIT = 10

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

QUESTIONS = [
    # ML Fundamentals
    {"q": "Which of the following best describes the bias-variance tradeoff?",
     "choices": ["A) High bias models overfit; high variance models underfit",
                 "B) High bias models underfit; high variance models overfit",
                 "C) Both bias and variance decrease with more data",
                 "D) Bias and variance always move in the same direction"],
     "answer": 1, "topic": "ML Fundamentals",
     "explanation": "High bias = underfitting (model too simple). High variance = overfitting (model too complex). More data reduces variance but not necessarily bias."},
    {"q": "In k-fold cross-validation with k=5 and 1000 samples, how many samples are in each validation fold?",
     "choices": ["A) 50", "B) 100", "C) 200", "D) 500"],
     "answer": 2, "topic": "ML Fundamentals",
     "explanation": "Each fold contains 1000/5 = 200 samples. 4 folds train, 1 fold validates each round."},
    {"q": "L1 regularization (Lasso) tends to produce what type of model?",
     "choices": ["A) Models with many small weights",
                 "B) Sparse models with many zero weights",
                 "C) Models with equal-magnitude weights",
                 "D) Models that ignore outliers"],
     "answer": 1, "topic": "ML Fundamentals",
     "explanation": "L1 (Lasso) adds |w| penalty, which drives many weights to exactly zero, producing sparse models useful for feature selection."},
    {"q": "A confusion matrix shows TP=80, FP=20, FN=10, TN=90. What is the precision?",
     "choices": ["A) 0.80", "B) 0.89", "C) 0.75", "D) 0.88"],
     "answer": 0, "topic": "ML Fundamentals",
     "explanation": "Precision = TP/(TP+FP) = 80/(80+20) = 80/100 = 0.80."},
    {"q": "Which algorithm is a non-parametric method that makes no assumptions about the underlying data distribution?",
     "choices": ["A) Linear Regression", "B) Logistic Regression", "C) K-Nearest Neighbors", "D) Naive Bayes"],
     "answer": 2, "topic": "ML Fundamentals",
     "explanation": "KNN is non-parametric — it makes predictions based on proximity to training points without assuming a functional form."},
    {"q": "Principal Component Analysis (PCA) finds directions of maximum:",
     "choices": ["A) Mean", "B) Variance", "C) Correlation", "D) Covariance with labels"],
     "answer": 1, "topic": "ML Fundamentals",
     "explanation": "PCA finds orthogonal directions (principal components) that capture maximum variance in the data, enabling dimensionality reduction."},
    # Neural Networks & Deep Learning
    {"q": "Which of the following best describes the vanishing gradient problem?",
     "choices": ["A) Gradients explode to infinity during backpropagation",
                 "B) Gradients become very small, slowing learning in early layers",
                 "C) The model forgets earlier training examples",
                 "D) Weights oscillate without converging"],
     "answer": 1, "topic": "Neural Networks & Deep Learning",
     "explanation": "Vanishing gradients occur when gradients shrink exponentially during backprop through many layers, making early layers learn very slowly."},
    {"q": "What is the output of the softmax function for inputs [2, 1, 0]? (approximate)",
     "choices": ["A) [0.67, 0.24, 0.09]", "B) [0.50, 0.25, 0.25]", "C) [1.0, 0.5, 0.0]", "D) [0.33, 0.33, 0.33]"],
     "answer": 0, "topic": "Neural Networks & Deep Learning",
     "explanation": "Softmax: exp(2)≈7.39, exp(1)≈2.72, exp(0)=1. Sum≈11.11. Outputs≈[0.665, 0.245, 0.090]."},
    {"q": "Batch normalization is typically applied:",
     "choices": ["A) After the activation function only",
                 "B) Before or after the linear transformation, before activation",
                 "C) Only at the output layer",
                 "D) Only during inference"],
     "answer": 1, "topic": "Neural Networks & Deep Learning",
     "explanation": "Batch norm normalizes layer inputs (before activation) to stabilize training. It can be placed before or after the linear transform."},
    {"q": "In a convolutional layer with input 32×32×3, kernel 5×5×3, and 16 filters (no padding), what is the output shape?",
     "choices": ["A) 28×28×16", "B) 32×32×16", "C) 28×28×3", "D) 30×30×16"],
     "answer": 0, "topic": "Neural Networks & Deep Learning",
     "explanation": "Output size = (32-5+1) = 28. With 16 filters and 3-channel kernel: output is 28×28×16."},
    {"q": "The attention mechanism in transformers computes attention scores as:",
     "choices": ["A) softmax(Q·Kᵀ/√d_k)·V",
                 "B) softmax(Q·V/√d_k)·K",
                 "C) Q·Kᵀ·V",
                 "D) sigmoid(Q+K)·V"],
     "answer": 0, "topic": "Neural Networks & Deep Learning",
     "explanation": "Scaled dot-product attention: Attention(Q,K,V) = softmax(QKᵀ/√d_k)V. Scaling by √d_k prevents small gradients."},
    {"q": "Which activation function is most commonly used in hidden layers of modern deep networks?",
     "choices": ["A) Sigmoid", "B) Tanh", "C) ReLU", "D) Softmax"],
     "answer": 2, "topic": "Neural Networks & Deep Learning",
     "explanation": "ReLU (Rectified Linear Unit) f(x)=max(0,x) is preferred: computationally cheap, sparse activations, avoids vanishing gradients."},
    # Python & NumPy
    {"q": "What does numpy.dot(A, B) compute when A is shape (3,4) and B is shape (4,2)?",
     "choices": ["A) Element-wise product, shape (3,4)", "B) Matrix product, shape (3,2)",
                 "C) Outer product, shape (3,4,4,2)", "D) Inner product, scalar"],
     "answer": 1, "topic": "Python & NumPy",
     "explanation": "np.dot performs matrix multiplication for 2D arrays. (3,4)·(4,2) = (3,2) matrix."},
    {"q": "What is the output of numpy.array([1,2,3,4,5])[::2]?",
     "choices": ["A) [1, 3, 5]", "B) [2, 4]", "C) [1, 2]", "D) [3, 4, 5]"],
     "answer": 0, "topic": "Python & NumPy",
     "explanation": "Slice [::2] starts at index 0 and takes every other element: indices 0, 2, 4 → values [1, 3, 5]."},
    {"q": "Which NumPy function computes the element-wise square root?",
     "choices": ["A) np.square(x)", "B) np.sqrt(x)", "C) np.pow(x, 0.5)", "D) np.root(x, 2)"],
     "answer": 1, "topic": "Python & NumPy",
     "explanation": "np.sqrt(x) computes element-wise square root. np.square computes x², np.pow doesn't exist (use np.power)."},
    {"q": "What does the following return: np.zeros((2,3)).shape?",
     "choices": ["A) 6", "B) (2,3)", "C) (3,2)", "D) [2, 3]"],
     "answer": 1, "topic": "Python & NumPy",
     "explanation": "np.zeros((2,3)) creates a 2×3 array of zeros. The .shape attribute returns the tuple (2, 3)."},
    {"q": "In Python, what is the time complexity of checking membership in a set (e.g., x in my_set)?",
     "choices": ["A) O(n)", "B) O(log n)", "C) O(1) average", "D) O(n²)"],
     "answer": 2, "topic": "Python & NumPy",
     "explanation": "Python sets use hash tables, so membership testing is O(1) on average — much faster than lists (O(n))."},
    {"q": "What does np.argmax(arr) return?",
     "choices": ["A) The maximum value", "B) The index of the maximum value",
                 "C) A boolean array of maxima", "D) The sorted array"],
     "answer": 1, "topic": "Python & NumPy",
     "explanation": "np.argmax returns the index of the maximum value in a flattened array (or along a specified axis)."},
    # Probability & Statistics for ML
    {"q": "If X ~ N(μ=5, σ²=4), what is P(X > 7)?",
     "choices": ["A) 0.1587", "B) 0.3413", "C) 0.0228", "D) 0.4772"],
     "answer": 0, "topic": "Probability & Statistics for ML",
     "explanation": "Z = (7-5)/2 = 1. P(X>7) = P(Z>1) ≈ 0.1587 (about 16% probability above one standard deviation)."},
    {"q": "Bayes' theorem states that P(A|B) equals:",
     "choices": ["A) P(B|A)·P(A)/P(B)", "B) P(A)·P(B)", "C) P(A∩B)/P(A)", "D) P(B|A)/P(A)"],
     "answer": 0, "topic": "Probability & Statistics for ML",
     "explanation": "Bayes' theorem: P(A|B) = P(B|A)·P(A)/P(B). This is fundamental to probabilistic ML models."},
    {"q": "A dataset has mean 50 and standard deviation 10. What is the coefficient of variation (CV)?",
     "choices": ["A) 0.2", "B) 5.0", "C) 0.5", "D) 20"],
     "answer": 0, "topic": "Probability & Statistics for ML",
     "explanation": "CV = σ/μ = 10/50 = 0.2 (or 20%). It measures relative variability."},
    {"q": "The Central Limit Theorem states that for large n, the sampling distribution of the mean is approximately:",
     "choices": ["A) Uniform", "B) Poisson", "C) Normal", "D) Exponential"],
     "answer": 2, "topic": "Probability & Statistics for ML",
     "explanation": "CLT: Regardless of the population distribution, the sample mean distribution approaches Normal as n → ∞. Critical for statistical inference."},
    {"q": "Maximum Likelihood Estimation (MLE) finds parameters that:",
     "choices": ["A) Minimize the prior probability",
                 "B) Maximize the probability of observing the data",
                 "C) Minimize the posterior probability",
                 "D) Maximize the entropy of predictions"],
     "answer": 1, "topic": "Probability & Statistics for ML",
     "explanation": "MLE finds θ̂ = argmax P(data|θ). It maximizes the likelihood of observing the given data."},
    {"q": "Which metric is most appropriate for evaluating a classifier on a heavily imbalanced dataset (99% class A, 1% class B)?",
     "choices": ["A) Accuracy", "B) F1 Score", "C) MSE", "D) R-squared"],
     "answer": 1, "topic": "Probability & Statistics for ML",
     "explanation": "F1 score (harmonic mean of precision and recall) handles class imbalance better than accuracy, which can be misleadingly high by predicting majority class."},
    # NLP & Computer Vision
    {"q": "In NLP, TF-IDF stands for Term Frequency — Inverse Document Frequency. High TF-IDF indicates a word that is:",
     "choices": ["A) Common in the corpus and the document",
                 "B) Frequent in the document but rare in the corpus",
                 "C) Rare in the document but common in the corpus",
                 "D) Equally common everywhere"],
     "answer": 1, "topic": "NLP & Computer Vision",
     "explanation": "TF-IDF is high when a word appears frequently in a document (high TF) but is rare across the corpus (high IDF). This identifies discriminative terms."},
    {"q": "Word2Vec's Skip-gram model is trained to:",
     "choices": ["A) Predict the center word from surrounding context words",
                 "B) Predict surrounding context words from a center word",
                 "C) Classify sentence sentiment",
                 "D) Generate new sentences"],
     "answer": 1, "topic": "NLP & Computer Vision",
     "explanation": "Skip-gram predicts context words given the center word. CBOW does the reverse: predicts center word from context."},
    {"q": "In a ResNet (Residual Network), skip connections help by:",
     "choices": ["A) Reducing the number of parameters",
                 "B) Allowing gradients to flow directly to earlier layers",
                 "C) Increasing the receptive field",
                 "D) Normalizing activations"],
     "answer": 1, "topic": "NLP & Computer Vision",
     "explanation": "Skip connections add the input to a block's output (x + F(x)), allowing gradients to bypass layers during backprop, solving the vanishing gradient problem in deep networks."},
    {"q": "In object detection, Intersection over Union (IoU) measures:",
     "choices": ["A) The ratio of predicted bounding box to ground truth box areas",
                 "B) The overlap area divided by the union area of two bounding boxes",
                 "C) The distance between box centers",
                 "D) The aspect ratio similarity of two boxes"],
     "answer": 1, "topic": "NLP & Computer Vision",
     "explanation": "IoU = (Area of intersection) / (Area of union). An IoU > 0.5 is typically used as the threshold for a true positive detection."},
    {"q": "The BERT model uses which training objective?",
     "choices": ["A) Next sentence prediction only",
                 "B) Masked language modeling only",
                 "C) Masked language modeling and next sentence prediction",
                 "D) Causal language modeling"],
     "answer": 2, "topic": "NLP & Computer Vision",
     "explanation": "BERT is pre-trained with two objectives: Masked Language Modeling (MLM) — predict masked tokens — and Next Sentence Prediction (NSP)."},
    {"q": "Image augmentation during training helps primarily by:",
     "choices": ["A) Reducing model size",
                 "B) Increasing training speed",
                 "C) Improving generalization by reducing overfitting",
                 "D) Improving gradient flow"],
     "answer": 2, "topic": "NLP & Computer Vision",
     "explanation": "Augmentation (flipping, cropping, color jitter) artificially expands the training set, exposing the model to more variations and reducing overfitting."},
]

CSS = """
body, .gradio-container { background: #0a1628 !important; color: #f0ebe0 !important; font-family: 'Georgia', serif; }
h1, h2, h3 { color: #c9a84c !important; }
.gr-button-primary { background: #c9a84c !important; color: #0a1628 !important; font-weight: bold; border: none; }
.gr-button { border: 1px solid #c9a84c !important; color: #c9a84c !important; background: transparent !important; }
.gr-textbox, .gr-radio, .gr-box { background: #0d1f3c !important; color: #f0ebe0 !important; border-color: #c9a84c !important; }
label { color: #f0ebe0 !important; }
.authority { color: #c9a84c; font-size: 0.85em; text-align: center; margin-top: 4px; }
"""

def new_session():
    shuffled = random.sample(QUESTIONS, len(QUESTIONS))
    return {"token_verified": False, "q_idx": 0, "score": 0, "answers": [], "free_used": 0, "questions": shuffled}

def get_question(session):
    qs = session["questions"]
    idx = session["q_idx"]
    if idx >= len(qs):
        return None
    return qs[idx]

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
    session["answers"].append(correct)
    result_icon = "Correct!" if correct else f"Incorrect. Correct answer: {q['choices'][q['answer']]}"
    feedback = f"**{result_icon}**\n\n{q['explanation']}"
    return session, feedback, gr.update(), gr.update(visible=True), fmt_score(session)

def next_question(session):
    if not session["token_verified"] and session["free_used"] >= FREE_Q_LIMIT:
        paywall_msg = (
            "**You have reached the free limit of 10 questions.**\n\n"
            "Unlock unlimited practice with a FissionLab Premium subscription:\n\n"
            "- **Monthly**: [Upgrade Now](https://buy.stripe.com/5kQfZadJAbnQ5OagjU1Fe09)\n"
            "- **Annual**: [Best Value](https://buy.stripe.com/7sY14g20SeA2ccy9Vw1Fe0a)\n\n"
            "Already have a token? Enter it in the **Unlock Premium** tab."
        )
        return session, paywall_msg, gr.update(choices=[], value=None, interactive=False), gr.update(visible=False), fmt_score(session)
    q = get_question(session)
    if q is None:
        total = session["q_idx"]
        score = session["score"]
        return session, f"**Quiz complete! Final score: {score}/{total}**\n\nRefresh the page to start a new quiz.", gr.update(choices=[], value=None, interactive=False), gr.update(visible=False), fmt_score(session)
    return session, "", gr.update(choices=q["choices"], value=None, interactive=True, label=f"Q{session['q_idx']+1}: {q['q']}"), gr.update(visible=False), fmt_score(session)

def verify_token_action(token, session):
    if verify_token(token):
        session["token_verified"] = True
        return session, "**Premium unlocked! Enjoy unlimited practice.**"
    return session, "**Invalid token.** Check your token format (FLAB-XXXX-XXXX-XXXX) or purchase a subscription."

with gr.Blocks(css=CSS, title="FissionLab AI/ML Practice — Dr. Preston PhD") as demo:
    session_state = gr.State(new_session())

    gr.Markdown("# FissionLab AI/ML Practice App — Dr. Preston PhD")
    gr.Markdown(
        "<div class='authority'>Dr. Preston — PhD Nuclear Engineering AFIT · B.A. Physics UC Berkeley · USAF Captain · LLNL/LBNL</div>"
    )

    with gr.Tabs():
        with gr.Tab("Practice Quiz"):
            score_display = gr.Markdown("Score: 0 / 0")
            q_radio = gr.Radio(choices=[], label="Loading first question...", interactive=True)
            with gr.Row():
                submit_btn = gr.Button("Submit Answer", variant="primary")
                next_btn = gr.Button("Next Question", visible=False)
            feedback_box = gr.Markdown("")

        with gr.Tab("Unlock Premium"):
            gr.Markdown("## Unlock Unlimited Practice")
            gr.Markdown(
                "The free tier includes **10 questions**. Upgrade for unlimited access to all topics, "
                "detailed explanations, and score tracking.\n\n"
                "### Subscribe\n"
                "- **Monthly Plan**: [Upgrade Now](https://buy.stripe.com/5kQfZadJAbnQ5OagjU1Fe09)\n"
                "- **Annual Plan (Best Value)**: [Upgrade Now](https://buy.stripe.com/7sY14g20SeA2ccy9Vw1Fe0a)\n\n"
                "### Already have a token?\n"
            )
            token_input = gr.Textbox(label="Enter your token (FLAB-XXXX-XXXX-XXXX)", placeholder="FLAB-XXXX-XXXX-XXXX")
            verify_btn = gr.Button("Verify Token", variant="primary")
            verify_status = gr.Markdown("")

    demo.load(next_question, inputs=[session_state],
              outputs=[session_state, feedback_box, q_radio, next_btn, score_display])

    submit_btn.click(submit_answer, inputs=[q_radio, session_state],
                     outputs=[session_state, feedback_box, q_radio, next_btn, score_display])
    next_btn.click(next_question, inputs=[session_state],
                   outputs=[session_state, feedback_box, q_radio, next_btn, score_display])
    verify_btn.click(verify_token_action, inputs=[token_input, session_state],
                     outputs=[session_state, verify_status])

if __name__ == "__main__":
    demo.launch()
