import os
import shutil
import glob

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from core.models import Vehicle

BRAIN_DIR = "/Users/mac/.gemini/antigravity/brain/d9117b30-c094-4165-badc-e1d6a19b20bf/"

mapping = {
    "Honda Odyssey": "honda_odyssey",
    "Chrysler Pacifica": "chrysler_pacifica",
    "Ford F-150 Raptor": "ford_f150_raptor",
    "Chevrolet Silverado 2500HD": "chevrolet_silverado",
    "Ram 3500 Heavy Duty": "ram_3500",
    "Toyota Camry": "toyota_camry",
    "Honda Accord": "honda_accord",
    "Hyundai Sonata": "hyundai_sonata",
    "Lexus LC 500": "lexus_lc_500",
    "Toyota Supra GR": "toyota_supra_gr",
    "Mercedes-AMG GT 63": "mercedes_amg_gt_63",
    "Range Rover SVAutobiography": "range_rover_sv"
}

for v in Vehicle.objects.filter(main_image=''):
    prefix = mapping.get(v.name)
    if not prefix:
        print(f"No mapping for {v.name}")
        continue
    
    # find the file
    search_pattern = os.path.join(BRAIN_DIR, f"{prefix}_*.png")
    matches = glob.glob(search_pattern)
    if matches:
        src_file = matches[0]
        dst_filename = f"{prefix}.png"
        dst_path = os.path.join("media/vehicles", dst_filename)
        shutil.copy2(src_file, dst_path)
        v.main_image = f"vehicles/{dst_filename}"
        v.save()
        print(f"Attached image for {v.name}")
    else:
        print(f"Could not find image for {prefix}")

print("Done attaching images.")
