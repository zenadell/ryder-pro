import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'ryder_pro.settings'
django.setup()
from core.models import Vehicle
for v in Vehicle.objects.all():
    print(v.year, v.make, v.model, "-", v.slug)
