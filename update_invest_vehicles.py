import os
import django
from django.core.files import File
import shutil

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle, Category

vehicle_data = [
    {
        'name': 'Kawasaki Ninja',
        'category_name': 'Motorcycle',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/kawasaki_ninja_1783098603693.jpg'
    },
    {
        'name': 'New Holland T7',
        'category_name': 'Tractor',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/new_holland_t7_1783098615064.jpg'
    },
    {
        'name': 'Case IH Steiger',
        'category_name': 'Tractor',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/case_ih_steiger_1783098639243.jpg'
    },
    {
        'name': 'Volvo 7900 Hybrid',
        'category_name': 'Bus',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/volvo_7900_hybrid_1783098653611.jpg'
    },
    {
        'name': 'Hyundai Universe',
        'category_name': 'Bus',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/hyundai_universe_1783098688015.jpg'
    },
    {
        'name': 'Nissan NV Cargo',
        'category_name': 'Van',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/nissan_nv_cargo_1783098699460.jpg'
    }
]

for data in vehicle_data:
    try:
        vehicle = Vehicle.objects.filter(name__iexact=data['name']).first()
        if vehicle:
            # Fix Category
            cat, created = Category.objects.get_or_create(name=data['category_name'])
            vehicle.category = cat
            
            # Fix Image (it uses 'images' related manager, or 'image_1' field? Wait, in models it might be 'image_1', let's check)
            # Actually, I should check the fields of Vehicle first.
            print(f"Vehicle found: {vehicle.name}")
        else:
            print(f"Vehicle NOT found: {data['name']}")
    except Exception as e:
        print(f"Error for {data['name']}: {e}")

