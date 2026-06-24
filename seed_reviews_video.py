import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import SiteContent, Review

# Seed video content key
video_content, created = SiteContent.objects.get_or_create(
    key='home_step_video',
    defaults={'value': 'Upload your home step video here. Supported formats: .mp4, .webm'}
)
if created:
    print("Created 'home_step_video' SiteContent key.")
else:
    print("'home_step_video' already exists.")

# Seed reviews
reviews_data = [
    {
        'title': 'Incredible Experience',
        'content': 'The process was incredibly smooth. I rented a compact car for a weekend getaway and it was in perfect condition. Highly recommend!',
        'rating': 5,
        'reviewer_name': 'Sarah Jenkins'
    },
    {
        'title': 'Easy and Affordable',
        'content': 'I loved how easy it was to book a car online. The rates were very competitive and the pickup was exactly as described.',
        'rating': 4,
        'reviewer_name': 'Michael Chen'
    },
    {
        'title': 'Great Customer Service',
        'content': 'I had to change my reservation last minute and the support team was super helpful. The SUV we got was spacious and clean.',
        'rating': 5,
        'reviewer_name': 'Elena Rodriguez'
    }
]

if Review.objects.count() < 3:
    for review_data in reviews_data:
        Review.objects.get_or_create(**review_data)
    print("Seeded 3 sample reviews.")
else:
    print("Reviews already exist. Skipping review seed.")

print("Seeding complete.")
