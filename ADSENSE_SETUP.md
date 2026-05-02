# Google AdSense Setup — FissionLab

## Step 1: Apply for AdSense
1. Go to https://adsense.google.com/start/
2. Sign in with your Google account
3. Enter: https://fissionlab.net as the site URL
4. Choose "Get started" and complete the application
5. AdSense will review the site (typically 2-4 weeks)

## Step 2: Add the AdSense code to your site
Once approved, go to AdSense → Sites → Get code. You'll receive a snippet like:

```html
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-XXXXXXXXXXXXXXXX" crossorigin="anonymous"></script>
```

Add this to the `<head>` of every page.

## Step 3: Replace ad placeholders
Find all instances of `<div class="adsense-unit"` in the community pages and replace with:

```html
<ins class="adsbygoogle"
     style="display:block"
     data-ad-client="ca-pub-XXXXXXXXXXXXXXXX"
     data-ad-slot="XXXXXXXXXX"
     data-ad-format="auto"
     data-full-width-responsive="true"></ins>
<script>(adsbygoogle = window.adsbygoogle || []).push({});</script>
```

Replace `ca-pub-XXXXXXXXXXXXXXXX` with your publisher ID and `XXXXXXXXXX` with the slot ID from AdSense.

## Current ad placeholders in the site:
- community/practice/index.html (1 unit, between hero and questions)
- community/resources/index.html (check for ad-unit divs)

## Expected revenue at 100 visitors/day:
- CPM (cost per 1000 impressions) for AFOQT/military niche: $4-$8
- At 100 visitors/day = 3,000/month × $6 CPM = ~$18/month initially
- Scales with traffic: at 1,000 visitors/day = ~$180/month
