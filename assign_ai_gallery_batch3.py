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

assign_images('2021-bmw-m5-competition', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/bmw_m5_front_int_1782287642032.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/bmw_m5_side_1782287654626.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/bmw_m5_back_int_1782287665502.png"
])

assign_images('2023-audi-rs6-avant', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/audi_rs6_front_int_1782287676229.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/audi_rs6_side_1782287686800.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/audi_rs6_back_int_1782287701792.png"
])

assign_images('2024-mercedes-benz-g63-amg', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/benz_g63_front_int_1782287713623.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/benz_g63_side_1782287722988.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/benz_g63_back_int_1782287733128.png"
])

assign_images('2023-lamborghini-urus', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/lambo_urus_front_int_1782287748866.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/lambo_urus_side_1782287757786.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/lambo_urus_back_int_1782287769310.png"
])

assign_images('2025-ferrari-purosangue', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ferrari_puro_front_int_1782287780128.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ferrari_puro_side_1782287792737.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ferrari_puro_back_int_1782287803612.png"
])
