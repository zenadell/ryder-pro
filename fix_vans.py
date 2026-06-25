import os
import django
from django.core.files import File

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle

vehicles_data = [
    (79, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/mercedes_benz_sprinter_1782326026950.png', 'mercedes-benz-sprinter-cargo-van.png'),
    (110, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ford_transit_350_1782326179637.png', 'ford-transit-350.png'),
    (111, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/ram_promaster_2500_1782326038105.png', 'ram-promaster-2500.png'),
    (112, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/chevrolet_express_2500_1782326047913.png', 'chevrolet-express-2500.png'),
    (113, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/gmc_savana_2500_1782326058127.png', 'gmc-savana-2500.png'),
    (114, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/nissan_nv2500_hd_1782326068813.png', 'nissan-nv2500-hd.png'),
    (115, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/volkswagen_crafter_1782326082523.png', 'volkswagen-crafter.png'),
    (116, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/renault_master_1782326092481.png', 'renault-master.png'),
    (117, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/fiat_ducato_1782326101800.png', 'fiat-ducato.png'),
    (118, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/peugeot_boxer_1782326111673.png', 'peugeot-boxer.png'),
    (119, '/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/citroen_jumper_1782326122554.png', 'citroen-jumper.png'),
]

for vid, path, filename in vehicles_data:
    try:
        v = Vehicle.objects.get(id=vid)
        with open(path, 'rb') as f:
            v.main_image.save(filename, File(f), save=True)
            print(f"Updated {v.name}")
    except Exception as e:
        print(f"Failed to update {vid}: {e}")
