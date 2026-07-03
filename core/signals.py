from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import FinancingApplication, InstallmentPlan

@receiver(post_save, sender=FinancingApplication)
def create_installment_plan(sender, instance, created, **kwargs):
    if instance.status == 'approved' and not hasattr(instance, 'installment_plan'):
        if instance.vehicle and instance.vehicle.full_price:
            # Automatically create an InstallmentPlan for the approved application
            InstallmentPlan.objects.create(
                application=instance,
                user=instance.user,
                vehicle=instance.vehicle,
                total_amount=instance.vehicle.full_price,
                principal_balance=instance.vehicle.full_price,
                tier='tier2' # Defaults to Tier 2 until 60% is paid
            )

from django.contrib.auth.signals import user_logged_in
import requests
from django.utils import timezone
from .models import UserProfile

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def update_user_geolocation(sender, request, user, **kwargs):
    profile, _ = UserProfile.objects.get_or_create(user=user)
    
    ip = get_client_ip(request)
    profile.ip_address = ip
    profile.last_login_at = timezone.now()
    
    try:
        # If localhost or LAN, fetch the server's real public IP for geolocation
        lookup_ip = ip
        is_local = ip in ('127.0.0.1', 'localhost', '::1', None) or (ip and (ip.startswith('192.168.') or ip.startswith('10.') or ip.startswith('172.')))
        
        if is_local:
            resp = requests.get('http://ip-api.com/json/', timeout=3)
        else:
            resp = requests.get(f'http://ip-api.com/json/{lookup_ip}', timeout=3)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get('status') == 'success':
                profile.city = data.get('city')
                profile.country = data.get('country')
                profile.country_code = data.get('countryCode', '').lower()
                profile.latitude = data.get('lat')
                profile.longitude = data.get('lon')
                if is_local:
                    profile.ip_address = data.get('query', ip)
    except:
        pass
        
    profile.save()
    profile.save()

