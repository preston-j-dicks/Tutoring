# FissionLab — CLAUDE.md
Static site on GitHub Pages. Domain: fissionlab.net. Repo: preston-j-dicks/Tutoring.

## Brand rules (non-negotiable)
Public name: "Dr. Preston" only. NEVER write: Dicks, Captain, active duty, .mil, current rank, uniform — anywhere user-facing. PhD credential is fine.
Historical military bio facts (military-brat childhood, commissioning at 19, "youngest commissioned officer since the Air Force's founding", USAF officer/years of service) are allowed since they don't reveal current active-duty status or position — this is the approved bio content in `index.html` (About section) and `community/about/index.html`. Do not add current rank, unit, or duty-status details.
Voice: technical, direct, honest, occasional dry humor. Not hype. Not corporate.

## Tech stack
- Static HTML/CSS/JS — no build step. GitHub Pages auto-deploys on push to main.
- Student portal: separate Railway Flask+PostgreSQL project — NOT in this repo, never link publicly.
- HuggingFace Spaces: Dr-P account, separate deployments.
- AdSense: ads.txt in root, auto-ads live. Search Console verified, sitemap.xml at root.
- FissionLab Discord: discord.gg/e9bXRtjW

## Don't
- Military references anywhere user-facing.
- Link to portal.fissionlab.net from any public page.
- Commit .env files or secrets.
- Images over 400KB without lazy-loading.
- Inline scripts over 150 lines without splitting.
