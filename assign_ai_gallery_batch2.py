import os, django
from django.core.files.base import ContentFile

os.environ['DJANGO_SETTINGS_MODULE'] = 'ryder_pro.settings'
django.setup()
from core.models import Vehicle, VehicleImage

def assign_images(slug, image_paths):
    try:
        v = Vehicle.objects.get(slug=slug)
    except Vehicle.DoesNotExist:
        print(f"Vehicle {slug} not found.")
        return
        
    v.images.all().delete()
    print(f"Updating {v.make} {v.model} with AI generated images...")
    
    for i, path in enumerate(image_paths):
        with open(path, 'rb') as f:
            img_data = f.read()
        filename = f"ai_gallery_{slug}_{i}.png"
        vi = VehicleImage(vehicle=v, order=i)
        vi.image.save(filename, ContentFile(img_data), save=True)
        print(f"Saved {path} as {filename}")

assign_images('2024-land-rover-defender-110', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/defender_front_int_1782242051735.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/defender_side_1782242064306.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/defender_back_int_1782242075864.png"
])

assign_images('2022-tesla-model-x-plaid', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/tesla_x_front_int_1782242085365.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/tesla_x_side_1782242094927.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/tesla_x_back_int_1782242106387.png"
])

assign_images('2025-chevrolet-corvette-z06', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/corvette_front_int_1782242118891.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/corvette_side_1782242130194.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/corvette_back_int_1782242141539.png"
])
