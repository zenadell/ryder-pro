from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import InstallmentPlan
from decimal import Decimal

class Command(BaseCommand):
    help = 'Process monthly penalty interest for Tier 1 installment plans'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting penalty processing...'))
        
        today = timezone.now().date()
        
        # Only process Tier 1 plans that are not fully paid
        plans = InstallmentPlan.objects.filter(tier='tier1', is_fully_paid=False)
        
        processed_count = 0
        for plan in plans:
            if plan.monthly_due_date and today.day == plan.monthly_due_date:
                # Add 5% penalty to principal balance if missed (simplification for MVP)
                # In reality we'd check if they made a payment this month.
                penalty = plan.principal_balance * Decimal('0.05')
                plan.accumulated_penalty_interest += penalty
                plan.save()
                processed_count += 1
                self.stdout.write(f'Added ${penalty:.2f} penalty to {plan}')

        self.stdout.write(self.style.SUCCESS(f'Successfully processed {processed_count} plans.'))
