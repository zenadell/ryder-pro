import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import InvestmentAsset

type_mapping = {
    'Suzuki Hayabusa': 'bike',
    'Fendt 900 Vario': 'tractor',
    'Setra ComfortClass': 'bus',
    'Volkswagen Crafter': 'van',
    'Freightliner Cascadia': 'truck',
    'Mack Anthem': 'truck',
    'Honda Accord': 'car',
    'Chevrolet Malibu': 'car',
    'BMW R 1250 GS': 'bike',
    'Kawasaki Ninja': 'bike',
    'New Holland T7': 'tractor',
    'Case IH Steiger': 'tractor',
    'Volvo 7900 Hybrid': 'bus',
    'Hyundai Universe': 'bus',
    'Nissan NV Cargo': 'van',
    'Ram ProMaster': 'van',
    'Kenworth T680': 'truck',
    'Peterbilt 579 Semi': 'truck',
    'Toyota Camry Hybrid': 'car',
    'Tesla Model 3 Fleet': 'car',
    'Yamaha MT-09': 'bike',
    'Honda Gold Wing': 'bike',
    'Massey Ferguson 7S': 'tractor',
    'John Deere 8R Tractor': 'tractor',
    'Yutong E12 Electric Bus': 'bus',
    'Scania Touring Coach': 'bus',
    'Ford Transit Custom': 'van',
    'Volvo FH16 Semi': 'truck',
    'Tesla Semi Truck': 'truck',
    'Honda Logistics Bike #4': 'bike',
    'Yamaha Delivery Bike Fleet': 'bike',
    'Mercedes Sprinter Van': 'van',
    'Ford Transit Cargo Van': 'van',
    'Freightliner Cascadia #2': 'truck',
    'Mack Anthem Long-Haul #1': 'truck',
}

image_mapping = {
    'Honda Logistics Bike #4': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/honda_logistics_bike_1783101057304.jpg',
    'Yamaha Delivery Bike Fleet': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/yamaha_delivery_bike_1783101073031.jpg',
    'Ford Transit Cargo Van': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ford_transit_cargo_van_1783101128038.jpg',
    'Freightliner Cascadia #2': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/freightliner_cascadia_1783101144682.jpg',
    'Mack Anthem Long-Haul #1': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/mack_anthem_long_haul_1783101186639.jpg',
}

for name, asset_type in type_mapping.items():
    asset = InvestmentAsset.objects.filter(name=name).first()
    if asset:
        asset.asset_type = asset_type
        if name in image_mapping:
            with open(image_mapping[name], 'rb') as f:
                asset.image.save(os.path.basename(image_mapping[name]), File(f), save=False)
        asset.save()
        print(f"Updated {name}")
    else:
        print(f"NOT FOUND: {name}")

