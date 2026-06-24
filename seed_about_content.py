import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import SiteContent

ABOUT_KEYS = {
    'about_hero_title': 'Who we are',
    'about_hero_desc': 'Founded with a passion for making city travel easy and accessible, we have grown to become a trusted car rental service in the area. Our mission is to provide seamless and affordable transportation options for every occasion, from daily commutes to special events. With a fleet of diverse, well-maintained vehicles and a commitment to customer satisfaction, we strive to make every rental experience smooth and stress-free.',
    'about_stat_1_value': '3+',
    'about_stat_1_label': 'Years of Experience',
    'about_stat_2_value': '48+',
    'about_stat_2_label': 'Rental Cars',
    'about_stat_3_value': '5k+',
    'about_stat_3_label': 'Satisfied Customers',
    'about_stat_4_value': '15+',
    'about_stat_4_label': 'Cities Served',
    'about_mission_title': 'Our mission',
    'about_mission_desc': 'Our mission is to provide exceptional car rental services that make urban travel easy, affordable, and enjoyable. We aim to create a seamless experience by offering a diverse fleet of vehicles, flexible rental options, and outstanding customer support. We are committed to being your trusted partner in city travel, ensuring every journey is smooth, convenient, and tailored to your needs.',
    'about_values_title': 'Our values',
    'about_value_1_title': 'Customer Focus:',
    'about_value_1_desc': 'We put our customers at the heart of everything we do. Your satisfaction is our top priority.',
    'about_value_2_title': 'Integrity:',
    'about_value_2_desc': 'Honesty and transparency are the cornerstones of our business. No hidden fees.',
    'about_value_3_title': 'Reliability:',
    'about_value_3_desc': 'Our customers rely on us for safe and dependable transportation.',
}

for key, value in ABOUT_KEYS.items():
    obj, created = SiteContent.objects.get_or_create(key=key)
    if created or not obj.value:
        obj.value = value
        obj.save()
        print(f"Seeded: {key}")
    else:
        print(f"Already exists: {key}")

print("Done seeding About page content!")
