import os
import shutil
import json
import requests
import time
from django.core.files import File
from django.utils.text import slugify

# We need to run this script within the Django context
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle, Category, VehicleFeature
from core.utils import generate_vehicle_data
from duckduckgo_search import DDGS

generated_cars = {
    "2025 Porsche 911 GT3 RS": "porsche_911_gt3_rs_1781904361034.png",
    "2024 Land Rover Defender 110": "land_rover_defender_1781904458960.png",
    "2022 Tesla Model X Plaid": "tesla_model_x_1781904496105.png",
    "2025 Chevrolet Corvette Z06": "chevrolet_corvette_z06_1781904525035.png",
    "2021 BMW M5 Competition": "bmw_m5_1781904577578.png",
    "2023 Audi RS6 Avant": "audi_rs6_1781904598905.png",
    "2024 Mercedes-Benz G63 AMG": "mercedes_g63_1781904643683.png",
    "2023 Lamborghini Urus": "lamborghini_urus_1781904685839.png",
    "2025 Ferrari Purosangue": "ferrari_purosangue_1781904712401.png",
    "2022 Rolls-Royce Cullinan": "rolls_royce_cullinan_1781904738361.png",
    "2024 Bentley Continental GT": "bentley_continental_1781904763237.png",
    "2025 Aston Martin DB12": "aston_martin_db12_1781904776682.png",
    "2023 McLaren 765LT": "mclaren_765lt_1781904787362.png",
    "2024 Porsche Taycan Turbo S": "porsche_taycan_1781904797511.png",
    "2025 Lucid Air Sapphire": "lucid_air_1781904807731.png",
    "2024 Rivian R1S": "rivian_r1s_1781904816505.png",
    "2024 Dodge Challenger SRT Hellcat": "dodge_challenger_hellcat_1781904848502.png"
}

unsplash_cars = [
    "2024 Toyota Sienna", # Family
    "2023 Honda Odyssey", # Family
    "2025 Chrysler Pacifica", # Family
    "2024 Ford F-150 Raptor", # Heavy Duty
    "2025 Chevrolet Silverado 2500HD", # Heavy Duty
    "2024 Ram 3500 Heavy Duty", # Heavy Duty
    "2024 Toyota Camry", # Sedan
    "2025 Honda Accord", # Sedan
    "2023 Hyundai Sonata", # Sedan
    "2025 Lexus LC 500", # Sports
    "2024 Toyota Supra GR", # Sports
    "2025 Mercedes-AMG GT 63", # Sports
    "2024 Range Rover SVAutobiography" # SUV
]

BRAIN_DIR = "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/"

def get_unsplash_image(car_name):
    query = f"site:unsplash.com {car_name}"
    try:
        with DDGS() as ddgs:
            results = list(ddgs.images(query, max_results=1))
            if results:
                image_url = results[0]['image']
                res = requests.get(image_url)
                if res.status_code == 200:
                    filename = f"{slugify(car_name)}.jpg"
                    filepath = os.path.join("media/vehicles/", filename)
                    with open(filepath, 'wb') as f:
                        f.write(res.content)
                    return filepath
    except Exception as e:
        print(f"Failed to fetch {car_name}: {e}")
    return None

print("Starting to process cars...")

for car_name, filename in generated_cars.items():
    print(f"Processing generated: {car_name}")
    year_str, name = car_name.split(' ', 1)
    year = int(year_str)
    
    if Vehicle.objects.filter(name=name, year=year).exists():
        print(f"Skipping {car_name}, already exists")
        continue

    data = generate_vehicle_data(f"{year} {name}")
    cat_name = data.get('category', 'Luxury')
    category_obj, _ = Category.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})
    v = Vehicle(
        name=name,
        slug=slugify(f"{year} {name}"),
        year=year,
        price_per_day=data.get('price', 1000),
        mileage=data.get('mileage', 0),
        fuel_type=data.get('fuel_type', 'Petrol'),
        transmission=data.get('transmission', 'Automatic'),
        description=data.get('description', ''),
        category=category_obj
    )
    v.save()

    feature_names = data.get('features', [])
    for fname in feature_names:
        feature_obj, _ = VehicleFeature.objects.get_or_create(name=fname)
        v.features.add(feature_obj)

    src_path = os.path.join(BRAIN_DIR, filename)
    if os.path.exists(src_path):
        dst_filename = f"{slugify(car_name)}.png"
        dst_path = os.path.join("media/vehicles", dst_filename)
        shutil.copy2(src_path, dst_path)
        v.main_image = f"vehicles/{dst_filename}"
        v.save()
    # Removed sleep here because Gemini API is bypassed

for car_name in unsplash_cars:
    print(f"Processing unsplash: {car_name}")
    year_str, name = car_name.split(' ', 1)
    year = int(year_str)
    
    if Vehicle.objects.filter(name=name, year=year).exists():
        print(f"Skipping {car_name}, already exists")
        continue

    data = generate_vehicle_data(f"{year} {name}")
    cat_name = data.get('category', 'Luxury')
    category_obj, _ = Category.objects.get_or_create(name=cat_name, defaults={'slug': slugify(cat_name)})
    v = Vehicle(
        name=name,
        slug=slugify(f"{year} {name}"),
        year=year,
        price_per_day=data.get('price', 1000),
        mileage=data.get('mileage', 0),
        fuel_type=data.get('fuel_type', 'Petrol'),
        transmission=data.get('transmission', 'Automatic'),
        description=data.get('description', ''),
        category=category_obj
    )
    v.save()

    feature_names = data.get('features', [])
    for fname in feature_names:
        feature_obj, _ = VehicleFeature.objects.get_or_create(name=fname)
        v.features.add(feature_obj)

    img_path = get_unsplash_image(name)
    if img_path:
        v.main_image = img_path.replace("media/", "")
        v.save()
    
    time.sleep(8) # rate limit protection

print("Done processing 30 cars!")
