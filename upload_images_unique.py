import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from django.core.files import File
from core.models import InvestmentAsset

IMAGE_DIR = os.path.join(os.path.dirname(__file__), 'media', 'invest', 'assets')

# Map specific vehicles to their new unique images
VEHICLE_IMAGE_MAP = {
    "Mack Anthem": "mack_anthem.jpg",
    "Chevrolet Malibu": "chevrolet_malibu.jpg",
    "BMW R 1250 GS": "bmw_r_1250.jpg",
    "Yutong E12 Electric Bus": "yutong_bus.jpg",
}

def upload_images():
    count = 0
    for asset in InvestmentAsset.objects.filter(name__in=VEHICLE_IMAGE_MAP.keys()):
        img_file = VEHICLE_IMAGE_MAP.get(asset.name)
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

    print(f"\nDone! Uploaded {count} unique images.")

if __name__ == '__main__':
    upload_images()
