import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

client = Client()

routes = [
    '/',
    '/about/',
    '/contact/',
    '/faq/',
    '/privacy/',
    '/terms/',
    '/vehicles/',
    '/blog/',
]

for route in routes:
    response = client.get(route)
    if response.status_code == 200:
        print(f"SUCCESS: {route} returned 200 OK")
    else:
        print(f"FAILED: {route} returned {response.status_code}")
        print(response.content[:500])

