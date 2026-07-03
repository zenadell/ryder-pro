import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from django.core.files import File
from core.models import InvestmentAsset

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'media', 'invest', 'assets')

# Map each vehicle name to its category image file
VEHICLE_IMAGE_MAP = {
    "Tesla Semi Truck": "truck.jpg",
    "Volvo FH16 Semi": "truck.jpg",
    "Peterbilt 579 Semi": "truck.jpg",
    "Kenworth T680": "truck.jpg",
    "Mack Anthem": "truck.jpg",
    "Freightliner Cascadia": "truck.jpg",
    "Ford Transit Custom": "van.jpg",
    "Mercedes Sprinter Van": "van.jpg",
    "Ram ProMaster": "van.jpg",
    "Nissan NV Cargo": "van.jpg",
    "Volkswagen Crafter": "van.jpg",
    "Scania Touring Coach": "bus.jpg",
    "Yutong E12 Electric Bus": "bus.jpg",
    "Hyundai Universe": "bus.jpg",
    "Volvo 7900 Hybrid": "bus.jpg",
    "Setra ComfortClass": "bus.jpg",
    "John Deere 8R Tractor": "tractor.jpg",
    "Massey Ferguson 7S": "tractor.jpg",
    "Case IH Steiger": "tractor.jpg",
    "New Holland T7": "tractor.jpg",
    "Fendt 900 Vario": "tractor.jpg",
    "Honda Gold Wing": "motorcycle.jpg",
    "Yamaha MT-09": "motorcycle.jpg",
    "Kawasaki Ninja": "motorcycle.jpg",
    "BMW R 1250 GS": "motorcycle.jpg",
    "Suzuki Hayabusa": "motorcycle.jpg",
    "Tesla Model 3 Fleet": "car.jpg",
    "Toyota Camry Hybrid": "car.jpg",
    "Chevrolet Malibu": "car.jpg",
    "Honda Accord": "car.jpg",
}

def upload_images():
    count = 0
    for asset in InvestmentAsset.objects.all():
        img_file = VEHICLE_IMAGE_MAP.get(asset.name)
        if not img_file:
            print(f"SKIP (no mapping): {asset.name}")
            continue

        img_path = os.path.join(IMAGE_DIR, img_file)
        if not os.path.exists(img_path):
            print(f"SKIP (file missing): {asset.name} -> {img_path}")
            continue

        # Use Django's File wrapper to trigger proper storage backend upload
        with open(img_path, 'rb') as f:
            django_file = File(f, name=f"invest/assets/{asset.name.lower().replace(' ', '_')}.jpg")
            asset.image.save(django_file.name, django_file, save=True)
        
        count += 1
        print(f"UPLOADED: {asset.name} -> {asset.image.url}")

    print(f"\nDone! Uploaded images for {count} assets.")

if __name__ == '__main__':
    upload_images()
