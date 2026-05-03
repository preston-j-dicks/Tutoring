"""
Run once to create Stripe products and payment links.
Save the output URLs to .env as STRIPE_APP_MONTHLY_LINK and STRIPE_APP_ANNUAL_LINK.
"""
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')


def create_products():
    monthly = stripe.Product.create(name="AFOQT Adaptive App - Monthly")
    monthly_price = stripe.Price.create(
        product=monthly.id,
        unit_amount=999,
        currency='usd',
        recurring={'interval': 'month'}
    )
    annual = stripe.Product.create(name="AFOQT Adaptive App - Annual")
    annual_price = stripe.Price.create(
        product=annual.id,
        unit_amount=7999,
        currency='usd',
        recurring={'interval': 'year'}
    )
    session_product = stripe.Product.create(name="1:1 Tutoring Session with Dr. Preston")
    session_price = stripe.Price.create(
        product=session_product.id,
        unit_amount=7000,
        currency='usd'
    )
    return {
        'monthly_price_id': monthly_price.id,
        'annual_price_id': annual_price.id,
        'session_price_id': session_price.id
    }


def create_payment_links(price_ids):
    monthly_link = stripe.PaymentLink.create(
        line_items=[{'price': price_ids['monthly_price_id'], 'quantity': 1}]
    )
    annual_link = stripe.PaymentLink.create(
        line_items=[{'price': price_ids['annual_price_id'], 'quantity': 1}]
    )
    return monthly_link.url, annual_link.url


if __name__ == '__main__':
    price_ids = create_products()
    monthly_url, annual_url = create_payment_links(price_ids)
    print(f"STRIPE_APP_MONTHLY_LINK={monthly_url}")
    print(f"STRIPE_APP_ANNUAL_LINK={annual_url}")
    print("Add these to your .env file.")
