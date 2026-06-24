import os, django

os.environ['DJANGO_SETTINGS_MODULE'] = 'ryder_pro.settings'
django.setup()
from core.models import Vehicle

vehicles = Vehicle.objects.all().order_by('id')
done_slugs = [
    '2025-porsche-911-gt3-rs',
    '2022-rolls-royce-cullinan',
    '2024-land-rover-defender-110',
    '2022-tesla-model-x-plaid',
    '2025-chevrolet-corvette-z06',
    '2021-bmw-m5-competition',
    '2023-audi-rs6-avant',
    '2024-mercedes-benz-g63-amg',
    '2023-lamborghini-urus',
    '2025-ferrari-purosangue'
]

next_batch = [v for v in vehicles if v.slug not in done_slugs][:5]
for v in next_batch:
    print(f"{v.slug}: {v.make} {v.model} ({v.year})")
