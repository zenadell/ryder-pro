import os
import django
import urllib.request
import tempfile
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle

def run():
    print("Updating Pickups with realistic AI generated images...")
    realistic_pickup_images = {
        'Toyota Hilux Double Cab': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/toyota_hilux_1782119943077.png',
        'Ford Ranger Wildtrak': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ford_ranger_1782119956401.png',
        'Ford F-150 Lightning': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ford_f150_1782119974001.png',
        'Chevrolet Colorado ZR2': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/chevy_colorado_1782119996107.png',
        'GMC Canyon AT4': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/gmc_canyon_1782120016373.png',
        'Ram 1500 TRX': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ram_1500_1782120091069.png',
        'Nissan Navara PRO-4X': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/nissan_navara_1782120245786.png',
        'Mitsubishi Triton Triton': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/mitsubishi_triton_1782120513678.png',
    }

    for name, path in realistic_pickup_images.items():
        try:
            v = Vehicle.objects.get(name=name)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    v.main_image.save(f"{name.replace(' ', '_')}.png", File(f), save=True)
                print(f"Updated realistic image for {name}")
            else:
                print(f"File not found: {path}")
        except Vehicle.DoesNotExist:
            # Maybe the name is just 'Mitsubishi Triton' instead of 'Mitsubishi Triton Triton'
            if name == 'Mitsubishi Triton Triton':
                try:
                    v = Vehicle.objects.get(name='Mitsubishi Triton')
                    if os.path.exists(path):
                        with open(path, 'rb') as f:
                            v.main_image.save(f"Mitsubishi_Triton.png", File(f), save=True)
                        print(f"Updated realistic image for Mitsubishi Triton")
                except Vehicle.DoesNotExist:
                    print(f"Vehicle {name} not found.")
            else:
                print(f"Vehicle {name} not found.")

    print("Done updating realistic pickups!")

if __name__ == '__main__':
    run()
