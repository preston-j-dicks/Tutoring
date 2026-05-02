# FissionLab Revenue Checklist

## Revenue Streams Status

### ACTIVE
| Stream | Monthly Estimate | Notes |
|--------|-----------------|-------|
| 1:1 Tutoring (Wyzant) | $350-700 | $70/hr, 5-10 hr/mo |
| 1:1 Tutoring (Direct via Stripe) | $0-350 | Growing |
| Amazon Affiliate (fissionlab-20) | $10-50 | 5 books linked |
| Beehiiv Newsletter (via=preston-dicks) | $5-25 | Referral commissions |

### PENDING SETUP
| Stream | Action Required | Est. Monthly |
|--------|----------------|-------------|
| Google AdSense | Apply at adsense.google.com → get publisher ID → update ADSENSE_SETUP.md | $15-180 |
| Beehiiv Embed Form | Get embed code from beehiiv.com → Settings → Embed → replace BEEHIIV_EMBED_PLACEHOLDER | Builds list |
| AFOQT App ($9.99/mo) | Build app or use existing AFOQT_APP/ project → add Stripe payment | $100-500 |
| Gumroad Study Guides | Upload PDFs from D:\ → set price → add links to community pages | $50-200 |
| Discord Community Growth | Hit 100 members → sponsorship opportunities | Variable |

### GUMROAD UPLOAD QUEUE (D:\ drive PDFs)
These files are ready to upload to prestonj.gumroad.com:

| File | Suggested Price | Gumroad Title |
|------|----------------|---------------|
| D:\AFOQT Quantitative Master Guide.pdf | $12 | AFOQT Quantitative Master Guide |
| D:\AFOQT_Quant_Advanced_Hefty_Problems.pdf | $7 | 100 Hard AFOQT Math Problems |
| D:\AFOQT_Guide_ASCII_Wrapped_DrD.pdf | $9 | AFOQT Complete Study Guide |

Steps to upload:
1. Go to app.gumroad.com → Products → New Product
2. Upload PDF → set price → add description → publish
3. Add Gumroad link to community/resources/ page

### REVENUE PROJECTION (100 visitors/day)
| Month | Sources | Estimated Monthly |
|-------|---------|------------------|
| Month 1 | Tutoring + Affiliates | $400-800 |
| Month 3 | + AdSense + Gumroad | $600-1,200 |
| Month 6 | + App + Newsletter growth | $1,000-2,500 |
| Month 12 | All streams optimized | $2,500-5,000+ |

### BEEHIIV SETUP
To get embed form code:
1. Log in at beehiiv.com
2. Go to your publication → Settings → Email → Embed
3. Copy the iframe embed code (format: `<iframe src="https://embeds.beehiiv.com/[ID]" ...>`)
4. Search all community pages for `beehiiv.com/?via=preston-dicks` links and replace with the embed
5. Your referral link stays active: https://www.beehiiv.com/?via=preston-dicks

### STRIPE KEYS
Existing Stripe payment links (from main site):
- Single session $75: https://buy.stripe.com/aFabIU7lcgIa1xU4Bc1Fe00
- 4-session $270: https://buy.stripe.com/8x2eV65d477Aa4qebM1Fe01
- 8-session $500: https://buy.stripe.com/bJe5kw0WOfE64K6gjU1Fe02

To create new links for AFOQT App:
1. Log in at dashboard.stripe.com
2. Products → Payment Links → Create new
3. Set $9.99/month recurring and $79.99/year
4. Copy links and add to community/index.html app section
