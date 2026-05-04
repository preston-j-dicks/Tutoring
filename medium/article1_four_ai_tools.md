# I Built 4 Free AI Tools in a Weekend as an Active Duty Officer — Here's What I Learned

*By Dr. Preston*

---

Last month I sat down on a Friday night with a half-eaten pizza, a quiet house, and a simple goal: ship something real. Not a side project I would revisit in six months. Not a polished SaaS I would spend three months pre-building. Four working AI tools deployed and publicly accessible by Sunday night.

I am an active duty Air Force officer with a PhD in Nuclear Engineering. I also run a tutoring business, write a newsletter, and try to build things in the margins. Time is the constraint. That is always the constraint.

Here is what I built, how long it actually took, and what I wish I had known before I started.

---

## The Four Tools

**1. AFOQT Score Predictor**

Every week I work with students preparing for the Air Force Officer Qualifying Test. The first session always starts the same way: I ask them what their weaknesses are, and they shrug. They do not know. They have been studying broadly for weeks and have no sense of where they actually stand.

I built a 20-question diagnostic quiz that uses a weighted scoring model to estimate a candidate's composite score and generate a radar chart of their strengths across the five AFOQT composites: Pilot, Navigator, Academic Aptitude, Verbal, and Quantitative. The output tells them where to focus. The tool is live at dr-p-afoqt-predictor.hf.space.

Time to build: about 9 hours. Hardest part: calibrating the scoring weights to match actual AFOQT composite formulas without access to the official rubric.

**2. Military Resume Translator**

I have watched smart, experienced officers walk out of the military and fumble their first civilian job search because their resume is written in a language civilians cannot parse. AFSC codes, unit designations, military rank abbreviations — none of it lands with a tech recruiter.

The Military Resume Translator takes any military job description, resume bullet, or LinkedIn summary and converts it into civilian-ready professional language. You select your target industry and it adjusts the translation accordingly.

Time to build: about 6 hours. Hardest part: building a prompt chain that preserves the real substance of what someone did in uniform while stripping the jargon. Early versions were either too literal or too generic. Getting the balance right took iteration.

**3. RepurposeAI**

I write a newsletter. I have a YouTube channel. I post on LinkedIn. I am active on Twitter. For a long time, creating content for all of those platforms meant writing the same idea four or five different ways every week. That was the biggest single time sink in my content workflow.

RepurposeAI solves it. Paste any piece of content — a blog post, a script, a PDF, a raw idea — and it generates a full social media content pack: Twitter thread, LinkedIn post, Instagram caption, newsletter snippet, and video script. All at once. What used to take two hours now takes about thirty seconds.

Time to build: about 7 hours. Hardest part: the output formatting. Getting six different content formats to come out cleanly structured — not just as a wall of text — required careful prompt engineering and some Gradio component work.

**4. ClearMinutes AI**

This one came directly from personal pain. Military meetings end, people scatter, and then three days later nobody agrees on what was actually decided. I have been in 8 AM command meetings where the action items were not captured until someone sent a vague email follow-up two days later.

ClearMinutes AI takes any meeting transcript — Zoom auto-transcript, Otter.ai export, anything — and extracts a structured summary, action items with owners, key decisions, a follow-up email draft, and a next meeting agenda. Under 20 seconds.

Time to build: about 5 hours. Hardest part: handling the wild inconsistency of real meeting transcripts. People talk over each other, go off topic, use informal shorthand. The extraction prompt needed to be robust to messiness.

---

## What Actually Worked

**HuggingFace Spaces is the right deployment platform for this kind of project.**

I did not want to build infrastructure. I did not want to manage servers, handle auth, or worry about scaling. HuggingFace Spaces gave me free hosting, a Gradio interface that looks professional out of the box, and immediate public accessibility. Every tool was live within minutes of pushing the code. I will write more about why I use HF Spaces instead of building a full SaaS in a separate post.

**Scope discipline is everything.**

Each of these tools does exactly one thing. There is no account system, no dashboard, no premium tier, no settings menu. The scope discipline is intentional. Every feature I did not build saved two hours of debugging and three hours of second-guessing.

**The hardest part is not the code.**

The LLM prompt engineering took more time than any of the Python or Gradio work. Getting a model to reliably produce well-structured, useful output in a specific format — consistently, across diverse inputs — is genuinely hard. Most of my weekend was spent iterating on prompts, not writing functions.

---

## What Was Harder Than Expected

**Testing with real inputs is not optional.**

I tested each tool with synthetic inputs that I controlled. When I ran them against real-world messy inputs — actual meeting transcripts from my phone, real AFOQT practice tests, my own military resume — the output quality dropped significantly. I spent Sunday afternoon on edge cases.

**Gradio's default UI limits you more than you think.**

Gradio is fast, but it is opinionated. Getting the visual presentation to look the way I wanted — clean, professional, not like a research demo — required working around some default behaviors. Nothing that could not be solved, but it added time.

---

## The Honest Accounting

Total weekend hours: approximately 30, including testing, deployment, writing documentation, and setting up the HuggingFace Space listings.

Tools launched: 4.

Things I would do differently: start with the output format first, then write the prompt backward from there. Define what clean output looks like before you write a single line of the generation logic.

---

## Where This Goes Next

All four tools are free at fissionlab.net. I am watching usage data to see which ones resonate. If any of them get enough traction to justify building a proper paid tier, I will. For now, they are useful, they are live, and they solve real problems I actually have.

That is enough.

---

*Tags: AI Tools, Side Projects, Military, HuggingFace, Gradio*
