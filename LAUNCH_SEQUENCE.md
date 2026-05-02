# AFOQT Community — Launch Sequence
**Total time: ~45 minutes from zero to live**

---

## Phase 1: Discord Setup (20 min)
→ Follow `DISCORD_SETUP.md` step by step.

At the end of Phase 1 you'll have:
- A fully structured Discord server
- MEE6 welcome bot configured
- A permanent Discord invite link (e.g. `discord.gg/XXXXXXX`)

---

## Phase 2: Wire the Invite Link into the Website (5 min)

1. Open a terminal in the `Tutoring` project directory
2. Find and replace `[DISCORD_INVITE_LINK]` with your actual link in all five community pages:

**Using Claude Code (recommended):**
```
claude "Replace every instance of [DISCORD_INVITE_LINK] with https://discord.gg/YOURLINKHERE in all files under community/"
```

**Manually (grep + sed):**
```
grep -rl "\[DISCORD_INVITE_LINK\]" community/
# Then edit each file and replace the placeholder
```

3. Verify the pages look right by opening them in a browser locally.

---

## Phase 3: Go Live (5 min)

```bash
git add community/
git commit -m "Launch: wire Discord invite link into all community pages"
git push origin main
```

GitHub Pages will deploy within 1–3 minutes. Verify at:
- `https://fissionlab.net/community/`
- `https://fissionlab.net/community/resources/`
- `https://fissionlab.net/community/practice/`

---

## Phase 4: Submit Sitemap to Google Search Console (2 min)

1. Go to Google Search Console → your fissionlab.net property
2. Left sidebar → **Sitemaps**
3. Enter: `community/sitemap.xml`
4. Click **Submit**

This tells Google to index your new community pages.

---

## Phase 5: Message the 10+ Students (5 min)

Send the message below individually or as a group via Wyzant/email/text.

---

### Student Announcement Message
*(In Dr. Preston's voice — warm, direct, no bullets)*

---

Hey — I wanted to reach out personally because you're one of the people who asked me about this.

The AFOQT community is live.

I built a free Discord server and resource hub at fissionlab.net/community/ — full subtest breakdowns, 60 original practice questions, cheat sheets, study schedules, and an organized Discord where you can post questions, share scores, find study partners, and join my weekly office hours. No fees, no upsells on the core material. Just a place where people preparing for the same test can work together with real expert guidance behind them.

I'm running weekly live Q&A sessions where you can bring anything — a concept you're struggling with, a question about the Pilot composite, anything about your test strategy. And if you want focused 1:1 work, you know where to find me.

Join here: [YOUR DISCORD INVITE LINK]

Let me know when you're in — I'll look for you there.

— Preston

---

## Phase 6: First Office Hours Announcement (3 min)

Post this in `#announcements` on your Discord after students start joining:

```
📅 FIRST OFFICE HOURS — [INSERT DATE AND TIME]

Our first live Q&A session is scheduled for [DATE] at [TIME] [TIMEZONE].

Bring your questions — AFOQT math strategies, Pilot composite breakdown, how to read instruments, study schedule review, anything.

The Zoom link will be posted in this channel 15 minutes before we start.

If you can't make it live, post your questions in #office-hours beforehand and I'll answer them in the session and post a summary after.

— Dr. Preston
```

---

## Success Verification Checklist

Before declaring launch complete, confirm all 12 criteria:

- [ ] `/community/index.html` — renders correctly at fissionlab.net/community/
- [ ] `/community/resources/` — Amazon affiliate links (fissionlab-20) present, Beehiiv CTA present
- [ ] `/community/practice/` — 60 questions visible, answer key accordion works, AdSense placeholders present
- [ ] `/community/about/` — Dr. Preston bio, Calendly CTA, Course JSON-LD in source
- [ ] `/community/forum/` — Discord redirect page with channel map
- [ ] AdSense `<div class="adsense-unit" data-ad-slot="placeholder">` present on practice + resources pages
- [ ] Affiliate disclosure (`"This site contains affiliate links..."`) on every community page footer
- [ ] JSON-LD FAQ schema on resources page (view source → search for `FAQPage`)
- [ ] JSON-LD Course schema on about page (view source → search for `Course`)
- [ ] `community/sitemap.xml` submitted to Google Search Console
- [ ] `DISCORD_SETUP.md` complete with server structure + MEE6 instructions
- [ ] `LAUNCH_SEQUENCE.md` with student announcement message — ✅ (this file)

---

## After Launch — First 30 Days

| Day | Action |
|-----|--------|
| Launch day | Message all 10+ students personally |
| Day 2–3 | Post first daily question in #daily-question |
| Day 7 | First office hours session |
| Day 10 | Submit sitemap to Google Search Console if not done |
| Day 14 | Check Google Analytics / Search Console for first organic traffic |
| Day 30 | Apply for Google AdSense using fissionlab.net (needs 30+ days of content) |

---

*Built by Claude Code for FissionLab.net — May 2026*
