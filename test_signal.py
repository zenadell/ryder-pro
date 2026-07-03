import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import UserProfile
from django.contrib.auth.models import User
import requests

user = User.objects.first()
profile, _ = UserProfile.objects.get_or_create(user=user)
ip = '127.0.0.1'

is_local = True

try:
    resp = requests.get('http://ip-api.com/json/', timeout=3)
    if resp.status_code == 200:
        data = resp.json()
        print("Data:", data)
        if data.get('status') == 'success':
            profile.city = data.get('city')
            profile.country = data.get('country')
            profile.country_code = data.get('countryCode', '').lower()
            profile.latitude = data.get('lat')
            profile.longitude = data.get('lon')
            if is_local:
                profile.ip_address = data.get('query', ip)
            print("Successfully set properties on profile!")
            profile.save()
            print("Profile saved.")
except Exception as e:
    print("EXCEPTION:", e)
