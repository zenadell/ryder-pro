import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ryder_pro.settings")
django.setup()

import traceback
from django.test import Client

c = Client()
try:
    response = c.get('/accounts/oauth/google/')
    print(response.status_code)
    if response.status_code == 500:
        print(response.content.decode())
except Exception as e:
    traceback.print_exc()
