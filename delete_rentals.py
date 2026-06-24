import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()
from core.models import User, InstallmentPlan, RentalRequest
user = User.objects.get(username='admin')
for plan in InstallmentPlan.objects.filter(user=user):
    RentalRequest.objects.filter(user=user, vehicle=plan.vehicle).delete()
