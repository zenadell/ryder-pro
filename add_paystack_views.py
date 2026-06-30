import os

views_path = "core/views.py"

content_to_append = """

# --- Paystack Helper Functions for Success Callbacks ---
def process_rental_success(rental, amount_to_pay):
    rental.amount_paid += amount_to_pay
    if rental.amount_paid >= rental.total_cost:
        rental.status = 'active'
    rental.save()

def process_installment_success(plan, user, amount):
    if plan.accumulated_penalty_interest > 0:
        if amount >= plan.accumulated_penalty_interest:
            amount -= plan.accumulated_penalty_interest
            plan.accumulated_penalty_interest = Decimal('0.00')
        else:
            plan.accumulated_penalty_interest -= amount
            amount = Decimal('0.00')
            
    if amount > 0:
        plan.principal_balance -= amount
        plan.down_payment_paid += amount
        
        if plan.tier == 'tier2':
            if plan.down_payment_paid >= (plan.total_amount * Decimal('0.60')):
                plan.tier = 'tier1'
                plan.is_vehicle_released = True
                from django.utils import timezone
                plan.monthly_due_date = timezone.now().day
                
                Shipment.objects.create(
                    user=user,
                    vehicle=plan.vehicle,
                    customer_name=plan.application.full_name,
                    origin_address="Ryder Pro Dealership",
                    delivery_address=plan.application.address,
                    status='processing',
                    estimated_delivery_date=(timezone.now() + timezone.timedelta(days=3)).date()
                )
        
    if plan.principal_balance <= 0 and plan.accumulated_penalty_interest <= 0:
        plan.is_fully_paid = True
        
    plan.save()
    
    PaymentTransaction.objects.create(
        user=user,
        installment_plan=plan,
        amount=amount,
        payment_type='installment',
        status='completed'
    )

def process_deposit_success(user, amount, reference):
    wallet, _ = InvestorWallet.objects.get_or_create(user=user)
    wallet.balance += amount
    wallet.save()
    InvestmentTransaction.objects.create(
        user=user, tx_type='deposit', amount=amount,
        status='completed', reference=reference, note="Wallet deposit"
    )

def process_withdrawal_fee_success(user, amount, reference):
    wallet, _ = InvestorWallet.objects.get_or_create(user=user)
    wallet.has_paid_withdrawal_fee = True
    wallet.save()
    InvestmentTransaction.objects.create(
        user=user, tx_type='fee', amount=amount,
        status='completed', reference=reference,
        note="Withdrawal fee paid — withdrawals released",
    )

@login_required
def paystack_otp_capture_view(request):
    pending = request.session.get('paystack_pending')
    if not pending:
        messages.error(request, "No pending transaction found.")
        return redirect('home')
        
    if request.method == 'POST':
        otp = request.POST.get('otp', '')
        reference = pending['reference']
        success, message = paystack_submit_otp(reference, otp)
        
        if success:
            action = pending.get('action')
            action_id = pending.get('action_id')
            amount = Decimal(str(pending.get('amount_to_pay', '0')))
            
            del request.session['paystack_pending']
            
            if action == 'rental':
                rental = get_object_or_404(RentalRequest, id=action_id)
                process_rental_success(rental, amount)
                messages.success(request, f"Payment successful! Your rental request is confirmed.")
                return redirect('rental_success', id=rental.id)
                
            elif action == 'installment':
                plan = get_object_or_404(InstallmentPlan, id=action_id, user=request.user)
                process_installment_success(plan, request.user, amount)
                messages.success(request, f"Payment processed successfully!")
                return redirect('dashboard')
                
            elif action == 'deposit':
                process_deposit_success(request.user, amount, reference)
                messages.success(request, f"Successfully deposited ${amount}.")
                return redirect('invest_dashboard')
                
            elif action == 'withdrawal_fee':
                process_withdrawal_fee_success(request.user, amount, reference)
                messages.success(request, f"Fee paid. Your withdrawal(s) are now approved.")
                return redirect('dashboard')
                
        else:
            messages.error(request, f"OTP Verification Failed: {message}")
            
    return render(request, 'paystack_otp_capture.html', {'message': pending.get('message')})
"""

with open(views_path, 'a') as f:
    f.write(content_to_append)

print("Appended Paystack helpers to views.py successfully.")
