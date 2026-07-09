import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import InvestmentAsset

def create_asset(name, asset_type, description, value, return_pct, image_path):
    print(f"Creating {name}...")
    asset = InvestmentAsset(
        name=name,
        asset_type=asset_type,
        description=description,
        total_value=value,
        daily_return_percent=return_pct
    )
    if os.path.exists(image_path):
        with open(image_path, 'rb') as f:
            asset.image.save(os.path.basename(image_path), File(f), save=False)
    else:
        print(f"Warning: Image {image_path} not found!")
    asset.save()
    print(f"Created {name} successfully.")
