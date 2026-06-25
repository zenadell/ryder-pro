import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from django.contrib.auth.models import User

superusers = User.objects.filter(is_superuser=True)
for u in superusers:
    print(f"Superuser: {u.username}, email: {u.email}")
