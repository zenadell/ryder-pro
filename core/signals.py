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
