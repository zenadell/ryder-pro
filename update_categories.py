import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ryder_pro.settings")
django.setup()

from core.models import Category
from django.core.files import File

# wait, where is Category model? it could be in core.models or vehicles.models.
# I'll try core.models first, if not I'll try vehicles.models.
try:
    from core.models import Category
except ImportError:
    try:
        from vehicles.models import Category
    except ImportError:
        pass

image_map = {
    'SUV': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/suv_category_1782214259579.png',
    'Sedan': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/sedan_category_1782214270983.png',
    'Luxury': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/luxury_category_1782214281905.png',
    'Electric': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/electric_category_1782214291157.png'
}

for name, path in image_map.items():
    try:
        cat = Category.objects.get(name=name)
        with open(path, 'rb') as f:
            cat.image.save(os.path.basename(path), File(f), save=True)
        print(f"Updated {name}")
    except Category.DoesNotExist:
        print(f"Category {name} not found")

