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

assign_images('2025-porsche-911-gt3-rs', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/porsche_gt3_front_int_1782241896531.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/porsche_gt3_side_1782241908638.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/porsche_gt3_back_int_1782241919768.png"
])

assign_images('2022-rolls-royce-cullinan', [
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/rolls_cullinan_front_int_1782241929532.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/rolls_cullinan_side_1782241941816.png",
    "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/rolls_cullinan_back_int_1782241952278.png"
])
