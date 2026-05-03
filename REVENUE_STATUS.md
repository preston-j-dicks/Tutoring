# FissionLab Revenue Status — 2026-05-03

## ACTIVE (earning now)

- **Amazon Associates (fissionlab-20)**: Links fixed — all AFOQT book links use `www.amazon.com/dp/ASIN?tag=fissionlab-20`. Mometrix (was pointing to CPA exam) and Officer Candidate Dummies (broken) replaced with verified search URLs. All 22 HTML files use normalized `www.amazon.com` prefix.
- **Beehiiv affiliate (preston-dicks)**: `https://www.beehiiv.com/?via=preston-dicks` wired in disclosure pages. Dynamic newsletter widget added to resources page and app page, with API fallback.
- **ElevenLabs affiliate**: `https://try.elevenlabs.io/e7b0uf20fr3c` — added to community/resources page AI Tools section. Already present in 5 other files.
- **Direct tutoring**: $70–125/hr, contact via `Dr_PrestonD@proton.me`, Calendly: `https://calendly.com/preston-j-dicks/introductory-meeting`
- **AFOQT App (community/app/)**: New dedicated page at `/community/app/` with Free/Monthly/Annual pricing tiers. Stripe payment links wired to existing live Stripe link. Run `stripe_products.py` to create official subscription products and save new links to .env.
- **Gumroad products**: Run `gumroad_api.py` to fetch existing products and create new ones. Targets: AFOQT Physical Science Cheat Sheet ($12), Math Formula Quick Reference ($9), 100 Hard AFOQT Practice Questions ($7), 30-Day Study Plan Template ($14).

## PENDING APPROVAL

- **Google AdSense (ca-pub-3289071681648577)**: Auto ads script on all 22 HTML files. Review timeline: 1–14 days after activation.
- **Impact.com**: Coursera, Brilliant, Bluehost (72hr from application)
- **PartnerStack**: Kit, Thinkific (pending review)

## DECLINED / REMOVED

- **Notion affiliate (PartnerStack)**: DECLINED — Notion links kept as direct `https://notion.so` (no affiliate parameters added)
- **Calendly affiliate**: No program exists — all Calendly links use direct URL `https://calendly.com/preston-j-dicks/introductory-meeting`

## NEEDS MANUAL ACTION

| Item | Action |
|------|--------|
| GA4 `G-K285VK64MP` | Verify data flowing in analytics.google.com — all 22 HTML files tagged |
| Stripe products | Run `python stripe_products.py` → save output URLs to `.env` as `STRIPE_APP_MONTHLY_LINK` and `STRIPE_APP_ANNUAL_LINK` |
| Gumroad products | `GUMROAD_ACCESS_TOKEN` missing from `.env` — add it, then run `python gumroad_api.py` |
| Beehiiv API key | Present in `.env` as `BEEHIVE_API_KEY` (note spelling). Both Portal and `beehiiv_api.py` read both `BEEHIVE_API_KEY` and `BEEHIIV_API_KEY`. |
| Skool affiliate | Not applied — go to skool.com/affiliate-program (40% lifetime commission) |
| Amazon ASIN verification | Confirm Mometrix and Officer Candidate search URLs return correct AFOQT titles |

## ESTIMATED MONTHLY PASSIVE INCOME

| Stream | Estimate |
|--------|----------|
| AdSense (post-approval, 100 visitors/day) | $60–240/mo |
| Amazon Associates (3–10 sales/month) | $3–15/mo |
| Beehiiv affiliate (5 upgrades/month) | $15–50/mo |
| ElevenLabs (10 signups/month) | varies |
| App subscriptions (10 students) | $99.90/mo |
| Gumroad products (5 sales/month) | $35–60/mo |
| **Total passive estimate** | **$213–464/mo** |

Direct tutoring (~6 students, $70–125/hr): ~$2,500/mo additional
