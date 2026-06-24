import os, django, requests
from django.core.files.base import ContentFile

os.environ['DJANGO_SETTINGS_MODULE'] = 'ryder_pro.settings'
django.setup()
from core.models import Vehicle, VehicleImage

headers = {'User-Agent': 'RyderProBot/1.0 (https://ryderpro.com)'}

def save_images(slug, urls):
    try:
        v = Vehicle.objects.get(slug=slug)
    except Vehicle.DoesNotExist:
        print(f"Vehicle {slug} not found.")
        return
        
    v.images.all().delete()
    print(f"Updating {v.make} {v.model}...")
    
    for i, url in enumerate(urls):
        img_data = requests.get(url, headers=headers).content
        filename = f"gallery_{slug}_{i}.jpg"
        vi = VehicleImage(vehicle=v, order=i)
        vi.image.save(filename, ContentFile(img_data), save=True)
        print(f"Saved {url} as {filename}")

save_images('2025-porsche-911-gt3-rs', [
    "https://upload.wikimedia.org/wikipedia/commons/a/a2/2003_LHD_GT3_RS_white_and_blue_%287921190936%29.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/1/1a/2010_Porsche_911_GT3_CS_3.8_Front.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/d/d6/2010_Porsche_911_GT3_RS_-_Flickr_-_The_Car_Spy_%2829%29.jpg"
])

save_images('2022-rolls-royce-cullinan', [
    "https://upload.wikimedia.org/wikipedia/commons/8/87/2022_Rolls_Royce_Cullinan_Black_Badge.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/c/cc/2024_Rolls-Royce_Cullinan_V12_-_6749cc_6.75_%28571PS%29_Petrol_-_Salamanca_Blue_-_01-2025%2C_Rear.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/2/2b/2024_Rolls-Royce_Cullinan_V12_-_6749cc_6.75_%28571PS%29_Petrol_-_Salamanca_Blue_-_01-2025%2C_Side.jpg"
])
