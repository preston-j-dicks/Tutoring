"""
Amazon ASIN verification script for FissionLab affiliate links.
Tries HEAD requests on candidate ASINs and writes verified links to JSON.
"""
import requests
import json
import time

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

CANDIDATE_BOOKS = [
    {
        "title": "Peterson's Master Military Flight Aptitude Tests",
        "asins": ["0768944716", "0768941733"],
        "keywords": ["afoqt", "military", "officer", "flight", "aptitude", "peterson"],
    },
    {
        "title": "Trivium AFOQT Study Guide 2024-2025",
        "asins": ["1637983417", "1637981066"],
        "keywords": ["afoqt", "military", "officer", "trivium"],
    },
    {
        "title": "Barron's Military Flight Aptitude Tests",
        "asins": ["1506264573", "1438011768"],
        "keywords": ["afoqt", "military", "officer", "flight", "barron"],
    },
    {
        "title": "Mometrix AFOQT Secrets Study Guide",
        "asins": ["1516701909"],
        "keywords": ["afoqt", "military", "officer"],
    },
    {
        "title": "Officer Candidate Tests For Dummies",
        "asins": ["1119550823", "0470598239"],
        "keywords": ["afoqt", "military", "officer", "candidate"],
    },
]

TAG = "fissionlab-20"
SEARCH_BASE = "https://www.amazon.com/s?k={query}&i=books&tag=" + TAG


def make_dp_url(asin):
    return f"https://www.amazon.com/dp/{asin}?tag={TAG}"


def title_keywords_ok(final_url, keywords):
    """Check if any keyword appears in the final URL path."""
    url_lower = final_url.lower()
    return any(kw in url_lower for kw in keywords)


def check_asin(asin, keywords, session):
    url = make_dp_url(asin)
    try:
        resp = session.get(url, headers=HEADERS, timeout=10, allow_redirects=True)
        final_url = resp.url
        status = resp.status_code
        if status == 200:
            # Check if final URL suggests wrong content (e.g. CPA exam)
            bad_terms = ["cpa", "accounting", "tax-cut", "turbo"]
            if any(b in final_url.lower() for b in bad_terms):
                print(f"  ASIN {asin}: 200 but final URL looks wrong -> {final_url[:80]}")
                return False, final_url, status
            print(f"  ASIN {asin}: OK (200) -> {final_url[:80]}")
            return True, final_url, status
        else:
            print(f"  ASIN {asin}: {status} -> {final_url[:80]}")
            return False, final_url, status
    except Exception as e:
        print(f"  ASIN {asin}: ERROR {e}")
        return False, url, 0


def build_search_url(title):
    query = title.replace(" ", "+").replace("'", "")
    return f"https://www.amazon.com/s?k={query}&i=books&tag={TAG}"


results = []
session = requests.Session()

for book in CANDIDATE_BOOKS:
    print(f"\n--- {book['title']} ---")
    chosen_asin = None
    chosen_url = None
    verified = False

    for asin in book["asins"]:
        ok, final_url, status = check_asin(asin, book["keywords"], session)
        time.sleep(0.5)  # polite delay
        if ok:
            chosen_asin = asin
            chosen_url = make_dp_url(asin)
            verified = True
            break

    if not verified:
        # Fall back to search URL
        chosen_url = build_search_url(book["title"])
        print(f"  Falling back to search URL: {chosen_url[:80]}")

    result = {
        "title": book["title"],
        "asin": chosen_asin,
        "url": chosen_url,
        "verified": verified,
    }
    results.append(result)
    print(f"  => URL: {chosen_url}")
    print(f"     Verified: {verified}")

output = {"books": results}
output_path = "C:/Users/prest/projects/Tutoring/verified_amazon_links.json"
with open(output_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nWrote results to {output_path}")
print("\nSummary:")
for r in results:
    status = "VERIFIED" if r["verified"] else "SEARCH URL"
    print(f"  [{status}] {r['title']}")
    print(f"           {r['url']}")
