import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import InvestmentAsset

assets_data = [
    {
        'name': 'Kawasaki Ninja',
        'asset_type': 'bike',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/kawasaki_ninja_1783098603693.jpg'
    },
    {
        'name': 'New Holland T7',
        'asset_type': 'truck',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/new_holland_t7_1783098615064.jpg'
    },
    {
        'name': 'Case IH Steiger',
        'asset_type': 'truck',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/case_ih_steiger_1783098639243.jpg'
    },
    {
        'name': 'Volvo 7900 Hybrid',
        'asset_type': 'truck',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/volvo_7900_hybrid_1783098653611.jpg'
    },
    {
        'name': 'Hyundai Universe',
        'asset_type': 'truck',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/hyundai_universe_1783098688015.jpg'
    },
    {
        'name': 'Nissan NV Cargo',
        'asset_type': 'van',
        'image_path': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/nissan_nv_cargo_1783098699460.jpg'
    }
]

for data in assets_data:
    try:
        asset = InvestmentAsset.objects.filter(name__icontains=data['name']).first()
        if asset:
            asset.asset_type = data['asset_type']
            with open(data['image_path'], 'rb') as f:
                asset.image.save(os.path.basename(data['image_path']), File(f), save=True)
            print(f"Updated {asset.name} successfully.")
        else:
            print(f"Asset NOT found: {data['name']}")
    except Exception as e:
        print(f"Error for {data['name']}: {e}")

