import os
import django
import random
import urllib.request
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Category, Vehicle

def run():
    cat_cars, _ = Category.objects.get_or_create(
        name='Cars'
    )

    cars_to_add = [
        {'name': 'Toyota Camry', 'price': 50},
        {'name': 'Honda Accord', 'price': 55},
        {'name': 'Hyundai Sonata', 'price': 45},
        {'name': 'Nissan Altima', 'price': 48},
        {'name': 'Kia K5', 'price': 47},
        {'name': 'Chevrolet Malibu', 'price': 46},
        {'name': 'Subaru Legacy', 'price': 52},
        {'name': 'Mazda 6', 'price': 54},
        {'name': 'Volkswagen Passat', 'price': 53},
        {'name': 'Ford Fusion', 'price': 49},
    ]

    for data in cars_to_add:
        v, created = Vehicle.objects.get_or_create(
            name=data['name'],
            defaults={
                'category': cat_cars,
                'price_per_day': data['price'],
                'make': data['name'].split()[0],
                'model': ' '.join(data['name'].split()[1:]),
                'year': 2024,
                'mileage': 1500,
                'condition': 'Excellent',
                'status': 'available',
                'seats': 5,
                'transmission': 'Automatic',
                'luggage': '2 bags',
                'description': f"A reliable and comfortable {data['name']} for all your daily needs.",
                'is_featured': True
            }
        )
        if created or not v.main_image:
            url = f"https://loremflickr.com/800/600/car,sedan?lock={random.randint(1, 1000)}"
            try:
                result = urllib.request.urlretrieve(url)
                with open(result[0], 'rb') as f:
                    v.main_image.save(f"{v.name.replace(' ', '_')}.jpg", File(f), save=True)
                print(f"Added {v.name} and downloaded image.")
            except Exception as e:
                print(f"Failed to download image for {v.name}: {e}")
        else:
            print(f"{v.name} already exists.")

    print("Added 10 cars successfully.")

if __name__ == '__main__':
    run()
