from pathlib import Path
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT
except ImportError:
    import subprocess, sys
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'reportlab'], check=True)
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, PageBreak
    from reportlab.lib.enums import TA_CENTER, TA_LEFT

OUTPUT = Path(r'C:\Users\prest\projects\Tutoring\assets\free-ai-prompts-sampler.pdf')
OUTPUT.parent.mkdir(exist_ok=True)

NAVY = HexColor('#0d1b2a')
GOLD = HexColor('#c9a84c')
CREAM = HexColor('#f5f0e8')
GRAY = HexColor('#5a6475')
LIGHT = HexColor('#f0ebe0')

doc = SimpleDocTemplate(str(OUTPUT), pagesize=letter,
    rightMargin=0.75*inch, leftMargin=0.75*inch,
    topMargin=0.75*inch, bottomMargin=0.75*inch)

styles = getSampleStyleSheet()
center = ParagraphStyle('C', parent=styles['Normal'], alignment=TA_CENTER)
title_s = ParagraphStyle('T', parent=styles['Title'], fontSize=26, textColor=CREAM, alignment=TA_CENTER, leading=32)
subtitle_s = ParagraphStyle('S', parent=styles['Normal'], fontSize=13, textColor=GOLD, alignment=TA_CENTER, leading=18)
h2_s = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=14, textColor=NAVY, spaceBefore=16, spaceAfter=6)
body_s = ParagraphStyle('B', parent=styles['Normal'], fontSize=10.5, leading=15, spaceAfter=6)
prompt_s = ParagraphStyle('P', parent=styles['Normal'], fontSize=9.5, fontName='Courier', leading=13,
    leftIndent=10, backColor=LIGHT, spaceBefore=4, spaceAfter=4)
note_s = ParagraphStyle('N', parent=styles['Normal'], fontSize=9, textColor=GRAY, fontName='Helvetica-Oblique',
    leftIndent=10, spaceAfter=8)
small_s = ParagraphStyle('Sm', parent=styles['Normal'], fontSize=8.5, textColor=GRAY, alignment=TA_CENTER)

PROMPTS = [
    ('AFOQT / Military Test Prep', 'Study Planning',
     'I\'m taking the AFOQT in [WEEKS] weeks. My strongest subtests are [STRONG] and my weakest are [WEAK]. Build me a day-by-day study schedule that prioritizes my weak areas without neglecting the strong ones. Include specific resource recommendations for each subtest.',
     'Use when: Starting your AFOQT prep and need a structured game plan.',
     'Example output: A 6-week schedule with daily focus areas, practice test timing, and specific subtests to drill each day.'),

    ('Physics & Science Tutoring', 'Concept Breakdown',
     'I\'m studying [PHYSICS TOPIC] and I understand [RELATED SIMPLER CONCEPT] well. Use that as a bridge to explain [PHYSICS TOPIC] step by step. Show me the mathematical relationship, a real-world analogy, and one worked example problem.',
     'Use when: A physics concept isn\'t clicking from the textbook explanation.',
     'Example output: A scaffold explanation connecting Newton\'s laws to a new concept, with analogies from daily life and a full worked problem.'),

    ('Business Writing', 'Email & Communication',
     'I need to write a professional email to [RECIPIENT TYPE] about [SITUATION]. My goal is [OUTCOME]. My relationship with them is [RELATIONSHIP]. Draft 3 versions: one formal, one conversational, one direct/brief. Then recommend which one to send and why.',
     'Use when: You need to write a high-stakes professional email and want options.',
     'Example output: Three complete email drafts with different tones, plus a recommendation with reasoning.'),

    ('Meeting Productivity', 'Action Item Extraction',
     'Here are my notes from a [MEETING TYPE] meeting: [PASTE NOTES]. Extract: (1) Every action item with the owner\'s name and a deadline, (2) The 3 most important decisions made, (3) Any unresolved questions that need follow-up, (4) A one-paragraph summary I can copy into Slack.',
     'Use when: You have messy meeting notes and need them structured fast.',
     'Example output: Structured action items table, decisions list, open questions, and a ready-to-paste Slack summary.'),

    ('Content Creation', 'Repurposing Engine',
     'I wrote this [BLOG POST / ARTICLE / TRANSCRIPT]: [PASTE CONTENT]. Repurpose it into: (1) 3 tweets under 280 characters each, (2) A LinkedIn post with a strong hook and 3-5 hashtags, (3) A newsletter intro paragraph, (4) One 60-second video script with a hook, 3 points, and a CTA.',
     'Use when: You have long-form content and need social media versions quickly.',
     'Example output: All 4 formats ready to copy-paste, tuned for each platform\'s style.'),
]

story = []

# Cover
cover = [[Paragraph('5 Free AI Prompts<br/>That Actually Work', title_s)]]
ct = Table(cover, colWidths=[6.5*inch])
ct.setStyle(TableStyle([
    ('BACKGROUND', (0,0),(-1,-1), NAVY),
    ('TOPPADDING', (0,0),(-1,-1), 50),
    ('BOTTOMPADDING', (0,0),(-1,-1), 30),
    ('LEFTPADDING', (0,0),(-1,-1), 30),
    ('RIGHTPADDING', (0,0),(-1,-1), 30),
]))
story.append(ct)
story.append(Spacer(1, 0.25*inch))
story.append(Paragraph('Ready-to-use prompts for AFOQT prep, physics, business writing,', subtitle_s))
story.append(Paragraph('meeting notes, and content creation.', subtitle_s))
story.append(Spacer(1, 0.15*inch))
story.append(Paragraph('by Dr. Preston  |  fissionlab.net', small_s))
story.append(Spacer(1, 0.15*inch))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD))
story.append(Spacer(1, 0.12*inch))
story.append(Paragraph(
    'These 5 prompts are taken from the full 100 ChatGPT Prompts for Students guide. '
    'Copy any prompt, replace the [BRACKETS] with your specifics, and paste into ChatGPT or Claude.',
    body_s))

for i, (cat, title, prompt, note, example) in enumerate(PROMPTS, 1):
    story.append(Spacer(1, 0.2*inch))
    story.append(HRFlowable(width='100%', thickness=0.5, color=GOLD))
    story.append(Paragraph(f'Prompt {i} of 5  —  {cat}', ParagraphStyle('num', parent=body_s, textColor=GOLD, fontName='Helvetica-Bold', spaceBefore=10)))
    story.append(Paragraph(title, h2_s))
    story.append(Paragraph(prompt, prompt_s))
    story.append(Paragraph(note, note_s))
    story.append(Paragraph(f'<i>{example}</i>', note_s))

story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width='100%', thickness=1, color=GOLD))
story.append(Spacer(1, 0.12*inch))
story.append(Paragraph('Want 95 more prompts like these?', ParagraphStyle('cta', parent=body_s, fontSize=12, fontName='Helvetica-Bold', alignment=TA_CENTER, textColor=NAVY)))
story.append(Paragraph('100 ChatGPT Prompts for Students covers 12 categories: essays, research, math, science, exam prep, career, and more.', ParagraphStyle('cta2', parent=body_s, alignment=TA_CENTER)))
story.append(Spacer(1, 0.08*inch))
story.append(Paragraph('Get the full guide at fissionlab.net', ParagraphStyle('cta3', parent=body_s, alignment=TA_CENTER, textColor=GOLD, fontName='Helvetica-Bold')))

doc.build(story)
print(f'Saved: {OUTPUT}')
print(f'Size: {OUTPUT.stat().st_size/1024:.1f} KB')
