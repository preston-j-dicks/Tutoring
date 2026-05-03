"""
Gumroad API utility — fetch existing products and create new ones.
Run to get product URLs saved to gumroad_products.json.
"""
import os
import json
import requests

GUMROAD_TOKEN = os.getenv('GUMROAD_ACCESS_TOKEN')
BASE = 'https://api.gumroad.com/v2'


def get_products():
    res = requests.get(f'{BASE}/products', headers={'Authorization': f'Bearer {GUMROAD_TOKEN}'})
    return res.json().get('products', [])


def create_product(name, price_cents, description, url=None):
    data = {
        'name': name,
        'price': price_cents,
        'description': description,
        'published': True
    }
    if url:
        data['custom_permalink'] = url
    res = requests.post(
        f'{BASE}/products',
        headers={'Authorization': f'Bearer {GUMROAD_TOKEN}'},
        json=data
    )
    return res.json()


def get_sales_count(product_id):
    res = requests.get(
        f'{BASE}/products/{product_id}',
        headers={'Authorization': f'Bearer {GUMROAD_TOKEN}'}
    )
    return res.json().get('product', {}).get('sales_count', 0)


NEW_PRODUCTS = [
    {
        'name': 'AFOQT Physical Science Cheat Sheet',
        'price_cents': 1200,
        'description': 'Essential physical science formulas and concepts for the AFOQT Physical Science subtest.',
        'url': 'afoqt-science-cheatsheet'
    },
    {
        'name': 'AFOQT Math Formula Quick Reference',
        'price_cents': 900,
        'description': 'All key algebra, geometry, and arithmetic formulas for the AFOQT Math Knowledge subtest.',
        'url': 'afoqt-math-cheatsheet'
    },
    {
        'name': '100 Hard AFOQT Practice Questions',
        'price_cents': 700,
        'description': '100 challenging AFOQT-style practice questions with detailed explanations across all subtests.',
        'url': 'afoqt-100-hard-questions'
    },
    {
        'name': 'AFOQT 30-Day Study Plan Template',
        'price_cents': 1400,
        'description': 'A structured 30-day intensive AFOQT study schedule, fully customizable PDF template.',
        'url': 'afoqt-30day-plan'
    },
]


if __name__ == '__main__':
    existing = get_products()
    existing_names = {p['name'] for p in existing}
    print(f"Found {len(existing)} existing products:")
    results = []
    for p in existing:
        print(f"  - {p['name']} | ${p.get('price', 0)/100:.2f} | {p.get('short_url', '')}")
        results.append({'name': p['name'], 'price': p.get('price', 0), 'url': p.get('short_url', '')})

    print("\nCreating new products...")
    for prod in NEW_PRODUCTS:
        if prod['name'] not in existing_names:
            result = create_product(prod['name'], prod['price_cents'], prod['description'], prod.get('url'))
            product = result.get('product', {})
            print(f"  Created: {product.get('name')} | {product.get('short_url', '')}")
            results.append({'name': product.get('name'), 'price': prod['price_cents'], 'url': product.get('short_url', '')})
        else:
            print(f"  Skipped (exists): {prod['name']}")

    with open('gumroad_products.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("\nSaved to gumroad_products.json")
