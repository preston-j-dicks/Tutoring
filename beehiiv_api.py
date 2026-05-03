import os
import requests

BEEHIIV_API_KEY = os.getenv('BEEHIVE_API_KEY') or os.getenv('BEEHIIV_API_KEY')
BEEHIIV_PUB_ID = 'prestons-newsletter-5f43a7'
BASE_URL = 'https://api.beehiiv.com/v2'


def subscribe_email(email, utm_source='fissionlab-community'):
    res = requests.post(
        f'{BASE_URL}/publications/{BEEHIIV_PUB_ID}/subscriptions',
        headers={'Authorization': f'Bearer {BEEHIIV_API_KEY}'},
        json={'email': email, 'utm_source': utm_source, 'reactivate_existing': True}
    )
    return res.json()


def get_subscriber_count():
    res = requests.get(
        f'{BASE_URL}/publications/{BEEHIIV_PUB_ID}',
        headers={'Authorization': f'Bearer {BEEHIIV_API_KEY}'}
    )
    data = res.json()
    return data.get('data', {}).get('stats', {}).get('total_active_subscriptions', 0)
