import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import InvestorWallet, InvestmentAsset, Investment, InvestmentTransaction

User = get_user_model()

def seed_test_investments():
    emails = ['ryderpro2026@gmail.com', 'emodiligaf@gmail.com']
    asset = InvestmentAsset.objects.filter(is_active=True).first()
    
    if not asset:
        print("No active assets found.")
        return

    for email in emails:
        user = User.objects.filter(email=email).first()
        if not user:
            continue
            
        wallet = InvestorWallet.for_user(user)
        # Add 500k to wallet
        wallet.balance += Decimal('500000.00')
        wallet.save()
        
        # Add a couple of random investments
        inv1 = Investment.objects.create(
            user=user, asset=asset, amount=Decimal('50000.00'),
            contract_months=12,
            daily_return_percent=asset.daily_return_percent,
        )
        inv1.accrued_earnings = Decimal('1450.00')
        inv1.save()
        
        InvestmentTransaction.objects.create(
            user=user, investment=inv1, tx_type='investment',
            amount=Decimal('50000.00'), status='completed', note=f"Invested in {asset.name}"
        )
        print(f"Added funds and mock investment for {email}")

if __name__ == '__main__':
    seed_test_investments()
