import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Category, Vehicle
from django.core.files import File
from django.utils.text import slugify

def create_vehicle(cat_name, make, model, year, price, image_path):
    cat, _ = Category.objects.get_or_create(name=cat_name, slug=slugify(cat_name))
    
    vehicle_name = f"{make} {model}"
    if not Vehicle.objects.filter(name=vehicle_name).exists():
        v = Vehicle(
            name=vehicle_name,
            category=cat,
            make=make,
            model=model,
            year=year,
            price_per_day=price,
            status='available',
            description=f"A highly capable {cat_name.lower()} ready for your demanding tasks. Equipped with the latest features to ensure reliability and performance.",
            seats=2 if cat_name in ['Trucks', 'Tractors'] else 5,
            luggage='4+ bags' if cat_name in ['Pickup Trucks', 'Vans'] else 'N/A',
            transmission=random.choice(['Automatic', 'Manual']),
            fuel_type='Diesel',
            mileage=random.randint(1000, 50000),
        )
        if os.path.exists(image_path):
            with open(image_path, 'rb') as f:
                v.main_image.save(f"{make.lower()}_{model.lower().replace(' ', '_')}.png", File(f), save=False)
        v.save()
        return True
    return False

def run():
    truck_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/truck_image_1782059802627.png'
    tractor_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/tractor_image_1782060093288.png'
    hilux_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/hilux_image_1782060272136.png'
    van_img = '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/van_image_1782061193035.png'

    trucks_data = [
        ('Isuzu', 'NPR HD'), ('Freightliner', 'M2 106'), ('Peterbilt', 'Model 337'),
        ('Kenworth', 'T270'), ('International', 'MV Series'), ('Mack', 'MD6'),
        ('Volvo', 'VNR 300'), ('Hino', 'L6'), ('Ford', 'F-650'), ('Chevrolet', 'Silverado 6500HD')
    ]

    tractors_data = [
        ('Case IH', 'Magnum 340'), ('New Holland', 'T8.380'), ('Massey Ferguson', '8730 S'),
        ('Fendt', '900 Vario'), ('Claas', 'Axion 870'), ('Kubota', 'M7-171'),
        ('Deutz-Fahr', '9340 TTV'), ('Valtra', 'T254'), ('JCB', 'Fastrac 8330'), ('Challenger', 'MT700')
    ]

    pickups_data = [
        ('Ford', 'Ranger Wildtrak'), ('Ford', 'F-150 Lightning'), ('Chevrolet', 'Colorado ZR2'),
        ('GMC', 'Canyon AT4'), ('Ram', '1500 TRX'), ('Nissan', 'Navara PRO-4X'),
        ('Isuzu', 'D-Max V-Cross'), ('Mitsubishi', 'Triton Triton'), ('Volkswagen', 'Amarok V6'), ('Jeep', 'Gladiator Rubicon')
    ]

    vans_data = [
        ('Ford', 'Transit 350'), ('Ram', 'ProMaster 2500'), ('Chevrolet', 'Express 2500'),
        ('GMC', 'Savana 2500'), ('Nissan', 'NV2500 HD'), ('Volkswagen', 'Crafter'),
        ('Renault', 'Master'), ('Fiat', 'Ducato'), ('Peugeot', 'Boxer'), ('Citroen', 'Jumper')
    ]

    count = 0
    print("Generating Trucks...")
    for make, model in trucks_data:
        if create_vehicle('Trucks', make, model, random.randint(2018, 2024), random.randint(100, 250), truck_img): count += 1

    print("Generating Tractors...")
    for make, model in tractors_data:
        if create_vehicle('Tractors', make, model, random.randint(2018, 2024), random.randint(150, 400), tractor_img): count += 1

    print("Generating Pickups...")
    for make, model in pickups_data:
        if create_vehicle('Pickup Trucks', make, model, random.randint(2018, 2024), random.randint(70, 150), hilux_img): count += 1

    print("Generating Vans...")
    for make, model in vans_data:
        if create_vehicle('Vans', make, model, random.randint(2018, 2024), random.randint(80, 140), van_img): count += 1

    print(f"Successfully added {count} new vehicles!")

if __name__ == '__main__':
    run()
