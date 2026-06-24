import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Category, Vehicle
from django.core.files import File
from django.utils.text import slugify

def create_vehicle(cat_name, make, model, year, price, image_path):
    # Get or create category
    cat, _ = Category.objects.get_or_create(name=cat_name, slug=slugify(cat_name))
    
    # Check if vehicle exists
    if not Vehicle.objects.filter(name=f"{make} {model}").exists():
        v = Vehicle(
            name=f"{make} {model}",
            category=cat,
            make=make,
            model=model,
            year=year,
            price_per_day=price,
            status='available',
            description=f"A highly capable {cat_name.lower()} ready for your heavy-duty tasks.",
            seats=2 if cat_name in ['Trucks', 'Tractors'] else 5,
            luggage='4+ bags',
            transmission='Automatic',
            fuel_type='Diesel',
            mileage=5000,
        )
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                v.main_image.save(f"{make.lower()}_{model.lower()}.png", File(f), save=False)
        v.save()
        print(f"Created {v.name}")
    else:
        print(f"{make} {model} already exists.")

def run():
    truck_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/truck_image_1782059802627.png'
    tractor_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/tractor_image_1782060093288.png'
    hilux_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/hilux_image_1782060272136.png'
    van_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/van_image_1782061193035.png'
    
    create_vehicle('Trucks', 'Hino', 'Box Truck', 2023, 120.00, truck_img)
    create_vehicle('Tractors', 'John Deere', 'Agricultural Tractor', 2022, 150.00, tractor_img)
    create_vehicle('Pickup Trucks', 'Toyota', 'Hilux Double Cab', 2024, 85.00, hilux_img)
    create_vehicle('Vans', 'Mercedes-Benz', 'Sprinter Cargo Van', 2023, 95.00, van_img)
    
    print("Done adding new categories and vehicles!")

if __name__ == '__main__':
    run()
