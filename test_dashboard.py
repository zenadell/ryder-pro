import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ryder_pro.settings")
django.setup()

import traceback
from django.test import Client
from django.contrib.auth.models import User

c = Client()
user = User.objects.first()
if user:
    c.force_login(user)
try:
    response = c.get('/dashboard/')
    if response.status_code == 500:
        print(response.content.decode()[:1000]) # Print first 1000 chars of 500 page
except Exception as e:
    traceback.print_exc()
