import os
import django
import urllib.request
import tempfile
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle

def run():
    print("Updating Tractors with realistic AI generated images...")
    realistic_tractor_images = {
        'Case IH Magnum 340': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/case_ih_magnum_1782117090545.png',
        'New Holland T8.380': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/new_holland_t8_1782117103179.png',
        'Massey Ferguson 8730 S': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/massey_ferguson_8730_1782117113997.png',
        'Fendt 900 Vario': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/fendt_900_1782117126201.png',
        'Claas Axion 870': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/claas_axion_870_1782117136312.png',
        'Kubota M7-171': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/kubota_m7_1782117149710.png',
        'Deutz-Fahr 9340 TTV': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/deutz_fahr_9340_1782117162233.png',
        'Valtra T254': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/valtra_t254_1782117173426.png',
        'JCB Fastrac 8330': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/jcb_fastrac_1782117184109.png',
        'Challenger MT700': '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/challenger_mt700_1782117196425.png',
    }

    for name, path in realistic_tractor_images.items():
        try:
            v = Vehicle.objects.get(name=name)
            if os.path.exists(path):
                with open(path, 'rb') as f:
                    v.main_image.save(f"{name.replace(' ', '_')}.png", File(f), save=True)
                print(f"Updated realistic image for {name}")
        except Vehicle.DoesNotExist:
            print(f"Vehicle {name} not found.")

    print("Done updating realistic tractors!")

    print("Done fixing images!")

if __name__ == '__main__':
    run()
