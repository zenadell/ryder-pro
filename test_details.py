import os
import django
from django.test import Client

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle, BlogPost, Category
from django.contrib.auth.models import User

# Create mock data
user, _ = User.objects.get_or_create(username='testuser')
cat, _ = Category.objects.get_or_create(name='Test Category')
vehicle, _ = Vehicle.objects.get_or_create(name='Test Car', category=cat, price_per_day=50)

post, _ = BlogPost.objects.get_or_create(title='Test Post', author=user, content='Test')

client = Client()

response = client.get(f'/vehicles/{vehicle.slug}/')
print(f"Vehicle Detail: {response.status_code}")

response = client.get(f'/blog/{post.slug}/')
print(f"Blog Detail: {response.status_code}")

