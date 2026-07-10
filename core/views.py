from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal, InvalidOperation
from .paystack_utils import paystack_charge_card, paystack_submit_otp
from .emails import (
    send_payment_receipt, send_application_received, send_withdrawal_notice
)
from django.conf import settings
from .models import (
    Vehicle, Category, BlogPost, TeamMember, Review, ContactMessage, GalleryImage, Job, TradeInRequest, RentalRequest, Shipment, SiteContent, PageVisit,
    InstallmentPlan, PaymentTransaction,
    InvestmentAsset, Investment, InvestorWallet, InvestmentTransaction,
    WithdrawalWindow, WithdrawalRequest,
)
from .forms import (
    ContactForm, NewsletterForm, FinancingApplicationForm, JobApplicationForm, TradeInRequestForm, RentalRequestForm, ReviewForm, CardPaymentForm
)

def home_view(request):
    featured_vehicles = Vehicle.objects.filter(is_featured=True, status='available')[:6]
    latest_blogs = BlogPost.objects.filter(is_published=True).order_by('-published_at')[:3]
    reviews = Review.objects.all().order_by('-created_at')[:5]
    
    categories = Category.objects.all()[:4]
    vehicle_count = Vehicle.objects.count()
    
    context = {
        'vehicles': featured_vehicles,
        'latest_blogs': latest_blogs,
        'reviews': reviews,
        'categories': categories,
        'vehicle_count': vehicle_count,
        'page_title': 'Ryder Pro | The Future of Commercial Logistics',
        'page_description': 'Invest in high-yield commercial vehicles, rent top-tier trucks, and experience world-class fleet management with Ryder Pro.',
    }
    return render(request, 'home/index.html', context)

def about_view(request):
    team_members = TeamMember.objects.all()
    gallery_images = GalleryImage.objects.all()
    return render(request, 'about/index.html', {'team_members': team_members, 'gallery_images': gallery_images})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        
        if name and email and message:
            ContactMessage.objects.create(
                name=name, email=email, phone=phone, message=message
            )
            messages.success(request, "Your message has been sent successfully.")
            return redirect('contact')
        else:
            messages.error(request, "Please fill in all required fields.")
            
    return render(request, 'contact/index.html')

def all_cars_view(request):
    vehicles = Vehicle.objects.filter(status='available')
    categories = Category.objects.all()
    
    # Distinct values for dropdowns
    makes = Vehicle.objects.exclude(make='').values_list('make', flat=True).distinct().order_by('make')
    fuel_types = Vehicle.objects.exclude(fuel_type='').values_list('fuel_type', flat=True).distinct().order_by('fuel_type')
    transmissions = Vehicle.objects.exclude(transmission='').values_list('transmission', flat=True).distinct().order_by('transmission')
    
    # Active filters
    category_slug = request.GET.get('category')
    q = request.GET.get('q')
    make = request.GET.get('make')
    fuel_type = request.GET.get('fuel_type')
    transmission = request.GET.get('transmission')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort = request.GET.get('sort')
    
    if category_slug:
        vehicles = vehicles.filter(category__slug=category_slug)
        
    if q:
        vehicles = vehicles.filter(
            Q(name__icontains=q) | 
            Q(make__icontains=q) | 
            Q(model__icontains=q)
        )
        
    if make:
        vehicles = vehicles.filter(make__iexact=make)
        
    if fuel_type:
        vehicles = vehicles.filter(fuel_type__iexact=fuel_type)
        
    if transmission:
        vehicles = vehicles.filter(transmission__iexact=transmission)
        
    if min_price and min_price.isdigit():
        vehicles = vehicles.filter(price_per_day__gte=min_price)
        
    if max_price and max_price.isdigit():
        vehicles = vehicles.filter(price_per_day__lte=max_price)
        
    if sort == 'price_asc':
        vehicles = vehicles.order_by('price_per_day')
    elif sort == 'price_desc':
        vehicles = vehicles.order_by('-price_per_day')
    elif sort == 'newest':
        vehicles = vehicles.order_by('-created_at')
        
    context = {
        'vehicles': vehicles,
        'categories': categories,
        'makes': makes,
        'fuel_types': fuel_types,
        'transmissions': transmissions,
        'current_category': category_slug,
        'q': q,
        'current_make': make,
        'current_fuel': fuel_type,
        'current_trans': transmission,
        'min_price': min_price,
        'max_price': max_price,
        'current_sort': sort,
    }
    return render(request, 'cars/all-cars/index.html', context)

def car_details_view(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    related_vehicles = Vehicle.objects.filter(category=vehicle.category).exclude(id=vehicle.id)[:3]
    vehicle_features = vehicle.features.all()
    vehicle_images = vehicle.images.all()
    vehicle_reviews = vehicle.reviews.all().order_by('-created_at')
    
    # Calculate Average Rating
    average_rating = 0
    if vehicle_reviews.exists():
        total = sum(review.rating for review in vehicle_reviews)
        average_rating = round(total / vehicle_reviews.count(), 1)
    
    # Handle Review Form Submission
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES)
        if form.is_valid():
            review = form.save(commit=False)
            review.vehicle = vehicle
            review.save()
            return redirect('car_details', slug=slug)
    else:
        form = ReviewForm()
        
    # Social Proof Tracking
    from django.utils.timezone import now
    from datetime import timedelta
    
    # Clean up old visits (older than 2 minutes)
    two_mins_ago = now() - timedelta(minutes=2)
    PageVisit.objects.filter(last_seen__lt=two_mins_ago).delete()
    
    # Add current user
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    PageVisit.objects.update_or_create(
        vehicle=vehicle, session_key=session_key,
        defaults={'last_seen': now()}
    )
    
    live_viewers = PageVisit.objects.filter(vehicle=vehicle).count()
    social_proof_mode = 'real'
    context = {
        'vehicle': vehicle,
        'related_vehicles': related_vehicles,
        'vehicle_features': vehicle_features,
        'vehicle_images': vehicle_images,
        'vehicle_reviews': vehicle_reviews,
        'average_rating': average_rating,
        'review_form': form,
        'live_viewers': live_viewers,
        'social_proof_mode': social_proof_mode,
    }
    return render(request, 'cars/car-details/index.html', context)

from django.http import JsonResponse
def ping_visit(request, slug):
    if request.method == 'POST':
        vehicle = get_object_or_404(Vehicle, slug=slug)
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        
        from django.utils.timezone import now
        PageVisit.objects.update_or_create(
            vehicle=vehicle, session_key=session_key,
            defaults={'last_seen': now()}
        )
        live_viewers = PageVisit.objects.filter(vehicle=vehicle).count()
        return JsonResponse({'status': 'success', 'viewers': live_viewers})
    return JsonResponse({'status': 'error'})

def blog_list_view(request):
    blogs = BlogPost.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'blog/index.html', {'posts': blogs})

def blog_detail_view(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug)
    recent_posts = BlogPost.objects.filter(is_published=True).exclude(id=blog.id).order_by('-published_at')[:3]
    
    context = {
        'post': blog,
        'recent_posts': recent_posts,
    }
    return render(request, 'blog/blog-page/index.html', context)

def api_dispatch(request, tracking_id):
    if request.method == 'POST':
        try:
            shipment = Shipment.objects.get(tracking_id__iexact=tracking_id)
            shipment.status = 'in_transit'
            shipment.tracking_started_at = timezone.now()
            shipment.save()
            return JsonResponse({'success': True, 'tracking_started_at': shipment.tracking_started_at.isoformat()})
        except Shipment.DoesNotExist:
            pass
    return JsonResponse({'success': False}, status=400)

def api_arrived(request, tracking_id):
    if request.method == 'POST':
        try:
            shipment = Shipment.objects.get(tracking_id__iexact=tracking_id)
            shipment.status = 'delivered'
            shipment.save()
            return JsonResponse({'success': True})
        except Shipment.DoesNotExist:
            pass
    return JsonResponse({'success': False}, status=400)

def faq_view(request):
    return render(request, 'faq/index.html')

def privacy_view(request):
    return render(request, 'privacy/index.html')

def terms_view(request):
    return render(request, 'terms/index.html')

def custom_404_view(request, exception=None):
    return render(request, 'utilities/404/index.html', status=404)

def link_in_bio_view(request):
    return render(request, 'utilities/link-in-bio/index.html')

def instructions_view(request):
    return render(request, 'utilities/instructions/index.html')

def licenses_view(request):
    return render(request, 'utilities/licenses/index.html')

def subscribe_newsletter(request):
    from .forms import NewsletterForm
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to our newsletter!')
        else:
            if 'email' in form.errors:
                messages.error(request, 'This email is already subscribed or invalid.')
            else:
                messages.error(request, 'An error occurred while subscribing.')
    
    # Redirect back to where the user came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')

@login_required
def financing_apply_view(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    
    if request.method == 'POST':
        form = FinancingApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.vehicle = vehicle
            if request.user.is_authenticated:
                application.user = request.user
            application.save()
            
            if request.user.is_authenticated:
                send_application_received(request.user, "Vehicle Financing", f"Vehicle: {vehicle.brand} {vehicle.title}")
                
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('financing_success', slug=vehicle.slug)
    else:
        form = FinancingApplicationForm()
        
    context = {
        'vehicle': vehicle,
        'form': form
    }
    return render(request, 'financing/apply.html', context)

@login_required
def financing_success_view(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    return render(request, 'financing/success.html', {'vehicle': vehicle})

def jobs_list_view(request):
    jobs = Job.objects.filter(status='open').order_by('-created_at')
    context = {
        'jobs': jobs
    }
    return render(request, 'jobs/index.html', context)

def job_detail_view(request, id):
    job = get_object_or_404(Job, id=id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            if request.user.is_authenticated:
                application.user = request.user
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('job_success', id=job.id)
    else:
        form = JobApplicationForm()
        
    context = {
        'job': job,
        'form': form
    }
    return render(request, 'jobs/detail.html', context)

def job_success_view(request, id):
    job = get_object_or_404(Job, id=id)
    return render(request, 'jobs/success.html', {'job': job})

@login_required
def trade_in_view(request):
    if request.method == 'POST':
        form = TradeInRequestForm(request.POST, request.FILES)
        if form.is_valid():
            trade_in = form.save(commit=False)
            if request.user.is_authenticated:
                trade_in.user = request.user
            trade_in.save()
            
            if request.user.is_authenticated:
                send_application_received(request.user, "Vehicle Trade-In", f"Proposed Vehicle: {trade_in.brand} {trade_in.model} ({trade_in.year})")
                
            messages.success(request, 'Your trade-in request has been submitted successfully!')
            return redirect('trade_in_success')
    else:
        form = TradeInRequestForm()
        
    return render(request, 'trade-in/index.html', {'form': form})

@login_required
def trade_in_success_view(request):
    return render(request, 'trade-in/success.html')

@login_required
def rental_apply_view(request, slug):
    vehicle = get_object_or_404(Vehicle, slug=slug)
    if request.method == 'POST':
        form = RentalRequestForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.vehicle = vehicle
            if request.user.is_authenticated:
                rental.user = request.user
                
            # Calculate total cost
            days = (rental.end_date - rental.start_date).days
            if days < 1:
                days = 1
            rental.total_cost = days * vehicle.price_per_day
            rental.save()
            
            if request.user.is_authenticated:
                send_application_received(request.user, "Vehicle Rental", f"Vehicle: {vehicle.brand} {vehicle.title} | Duration: {days} days")
            
            return redirect('rental_checkout', id=rental.id)
    else:
        # Pre-fill user data if logged in
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
                'email': request.user.email,
            }
        form = RentalRequestForm(initial=initial_data)
        
    return render(request, 'rentals/apply.html', {'form': form, 'vehicle': vehicle})

@login_required
def rental_checkout_view(request, id):
    rental = get_object_or_404(RentalRequest, id=id)
    if request.method == 'POST':
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            amount_to_pay = form.cleaned_data['amount_to_pay']
            card_number = request.POST.get('card_number', '').replace(' ', '')
            expiry = request.POST.get('expiry', '')
            cvv = request.POST.get('cvv', '')
            
            exp_month, exp_year = '12', '2030'
            if '/' in expiry:
                exp_month, exp_year = expiry.split('/')
                if len(exp_year) == 2:
                    exp_year = '20' + exp_year
            
            card_dict = {
                'number': card_number,
                'cvv': cvv,
                'exp_month': exp_month,
                'exp_year': exp_year
            }
            
            email = request.user.email
            status, payload = paystack_charge_card(email, amount_to_pay, card_dict)
            
            if status == "success":
                rental.amount_paid += amount_to_pay
                if rental.amount_paid >= rental.total_cost:
                    rental.status = 'active'
                rental.save()
                messages.success(request, f'Payment of ${amount_to_pay} successful! Your rental request is confirmed.')
                return redirect('rental_success', id=rental.id)
            elif status in ['send_otp', 'send_pin', 'send_phone', 'send_birthday']:
                request.session['paystack_pending'] = {
                    'reference': payload.get('reference'),
                    'message': payload.get('message'),
                    'action': 'rental',
                    'action_id': rental.id,
                    'amount_to_pay': float(amount_to_pay)
                }
                return redirect('paystack_otp_capture')
            else:
                messages.error(request, payload.get('message', 'Payment failed.'))
    else:
        form = CardPaymentForm(initial={'amount_to_pay': rental.amount_remaining})
        
    return render(request, 'rentals/checkout.html', {'form': form, 'rental': rental})

@login_required
def rental_success_view(request, id):
    rental = get_object_or_404(RentalRequest, id=id)
    return render(request, 'rentals/success.html', {'rental': rental})

def shipment_tracking_view(request):
    tracking_id = request.GET.get('tracking_id')
    shipment = None
    error = None
    api_updates = []
    
    if tracking_id:
        try:
            shipment = Shipment.objects.get(tracking_id__iexact=tracking_id)
            # Generate real external tracking URL based on provider
            tracking_url = ''
            if shipment.tracking_provider:
                provider = shipment.tracking_provider.lower()
                if 'fedex' in provider:
                    tracking_url = f"https://www.fedex.com/fedextrack/?trknbr={tracking_id}"
                elif 'ups' in provider:
                    tracking_url = f"https://www.ups.com/track?tracknum={tracking_id}"
                elif 'usps' in provider:
                    tracking_url = f"https://tools.usps.com/go/TrackConfirmAction?tLabels={tracking_id}"
                elif 'dhl' in provider:
                    tracking_url = f"https://www.dhl.com/en/express/tracking.html?AWB={tracking_id}"
                else:
                    tracking_url = f"https://www.google.com/search?q={shipment.tracking_provider}+tracking+{tracking_id}"
            
            # Use real tracking URL instead of fake API updates
            api_updates = []
        except Shipment.DoesNotExist:
            error = "We couldn't find a shipment with that Tracking ID. Please verify and try again."
            
    context = {
        'shipment': shipment, 
        'error': error, 
        'tracking_id': tracking_id,
        'tracking_url': tracking_url if 'tracking_url' in locals() else '',
        'tracking_started_at_iso': shipment.tracking_started_at.isoformat() if shipment and shipment.tracking_started_at else ''
    }
    return render(request, 'tracking/index.html', context)

@login_required
def customer_dashboard_view(request):
    financing_apps = request.user.financing_applications.all().order_by('-submitted_at')
    job_apps = request.user.job_applications.all().order_by('-submitted_at')
    trade_ins = request.user.trade_in_requests.all().order_by('-submitted_at')
    rentals = request.user.rental_requests.all().order_by('-submitted_at')
    shipments = request.user.shipments.all().order_by('-created_at')
    
    # Phase 2 Models
    installment_plans = request.user.installment_plans.all().order_by('-created_at')
    payments = request.user.payments.all().order_by('-created_at')
    
    user_display_name = request.user.first_name if request.user.first_name else request.user.username.split('@')[0]

    # Ryder Invest — accrue daily earnings on load, then summarise the portfolio
    _accrue_user_investments(request.user)
    wallet = InvestorWallet.for_user(request.user)
    investments = request.user.investments.select_related('asset').all()
    active_investments = investments.filter(status='active')
    invest_transactions = request.user.investment_transactions.all()[:30]
    withdrawal_requests = request.user.withdrawal_requests.all()[:10]
    current_window = WithdrawalWindow.current()

    total_invested = active_investments.aggregate(s=Sum('amount'))['s'] or Decimal('0.00')
    total_accrued = active_investments.aggregate(s=Sum('accrued_earnings'))['s'] or Decimal('0.00')
    # The fee that would apply if the user withdrew now (the fee is PAID and accumulates)
    _fee_window = current_window or WithdrawalWindow.objects.filter(is_active=True).order_by('-opens_at').first()
    fee_display = _fee_window.fee_display if _fee_window else '5%'

    # Generate Chart Data (Last 14 days portfolio growth)
    import json
    from datetime import timedelta
    chart_labels = []
    chart_data = []
    today = timezone.now().date()
    
    # Calculate exact historical growth based on active investments
    for i in range(14, -1, -1):
        d = today - timedelta(days=i)
        chart_labels.append(d.strftime('%b %d'))
        
        day_total = Decimal('0.00')
        for inv in active_investments:
            if inv.start_date and inv.start_date.date() <= d:
                days_active = (d - inv.start_date.date()).days
                # Cap at contract end date if applicable
                if inv.end_date and d > inv.end_date.date():
                    days_active = (inv.end_date.date() - inv.start_date.date()).days
                    
                earnings = inv.daily_earning * days_active
                day_total += inv.amount + earnings
                
        chart_data.append(round(float(day_total), 2))
    
    if float(total_invested + total_accrued) == 0:
        # Empty state chart - data is already [0,0...] from the loop above, but just to be sure
        chart_data = [0] * 15

    context = {
        'financing_apps': financing_apps,
        'job_apps': job_apps,
        'trade_ins': trade_ins,
        'rentals': rentals,
        'shipments': shipments,
        'installment_plans': installment_plans,
        'payments': payments,
        'user_display_name': user_display_name,
        # Invest
        'wallet': wallet,
        'investments': investments,
        'active_investments': active_investments,
        'invest_transactions': invest_transactions,
        'withdrawal_requests': withdrawal_requests,
        'current_window': current_window,
        'total_invested': total_invested,
        'total_accrued': total_accrued,
        'invest_asset_count': active_investments.values('asset').distinct().count(),
        'withdrawal_fee_display': fee_display,
        'accumulated_fee': wallet.accumulated_fee,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def make_payment_view(request, plan_id):
    plan = get_object_or_404(InstallmentPlan, id=plan_id, user=request.user)
    
    if request.method == 'POST':
        amount_to_pay = request.POST.get('amount', '0.00')
        card_number = request.POST.get('card_number', '').replace(' ', '')
        expiry = request.POST.get('expiry', '')
        cvv = request.POST.get('cvv', '')
        
        exp_month, exp_year = '12', '2030'
        if '/' in expiry:
            exp_month, exp_year = expiry.split('/')
            if len(exp_year) == 2:
                exp_year = '20' + exp_year
                
        card_dict = {
            'number': card_number,
            'cvv': cvv,
            'exp_month': exp_month,
            'exp_year': exp_year
        }
        
        email = request.user.email
        status, payload = paystack_charge_card(email, amount_to_pay, card_dict)
        
        if status == "success":
            process_installment_success(plan, request.user, Decimal(amount_to_pay))
            messages.success(request, f"Payment of ${amount_to_pay} processed successfully!")
            return redirect('payment_success')
        elif status in ['send_otp', 'send_pin', 'send_phone', 'send_birthday']:
            request.session['paystack_pending'] = {
                'reference': payload.get('reference'),
                'message': payload.get('message'),
                'action': 'installment',
                'action_id': plan.id,
                'amount_to_pay': float(amount_to_pay)
            }
            return redirect('paystack_otp_capture')
        else:
            messages.error(request, payload.get('message', 'Payment failed.'))
            
    return render(request, 'dashboard/make_payment.html', {'plan': plan})

from django.http import HttpResponse
from .utils import generate_bill_of_sale_pdf

@login_required
def schedule_delivery(request, plan_id):
    plan = get_object_or_404(InstallmentPlan, id=plan_id, user=request.user)
    if not plan.is_fully_paid:
        messages.error(request, "Vehicle must be fully paid before scheduling delivery.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        date_str = request.POST.get('delivery_date')
        address = request.POST.get('delivery_address')
        phone = request.POST.get('delivery_phone')
        if date_str and address:
            from django.utils.dateparse import parse_datetime
            parsed_date = parse_datetime(date_str)
            plan.delivery_date = parsed_date
            plan.delivery_address = address
            plan.delivery_phone = phone
            plan.delivery_status = 'scheduled'
            plan.save()
            
            # Create Shipment for the Active Shipments table
            from .models import Shipment
            Shipment.objects.create(
                user=plan.user,
                vehicle=plan.vehicle,
                customer_name=plan.user.get_full_name() or plan.user.username,
                delivery_address=address,
                estimated_delivery_date=parsed_date.date() if parsed_date else None,
                status='processing'
            )
            
            messages.success(request, f"Delivery for {plan.vehicle.name} successfully scheduled!")
        return redirect('dashboard')
        
    return render(request, 'dashboard/schedule_delivery.html', {'plan': plan})

from django.http import JsonResponse
import json
import hashlib
from datetime import timedelta
from django.utils import timezone

@login_required
def calculate_delivery(request):
    import random
    if request.method == 'POST':
        data = json.loads(request.body)
        zip_code = data.get('zip_code', '00000')
        street = data.get('street', '').lower()
        city = data.get('city', '').lower()
        state = data.get('state', '').lower()
        
        full_address_str = f"{street} {city} {state} {zip_code}"
        
        is_international = False
        
        # Check for non-US keywords or missing US state patterns
        us_states = ['al','ak','az','ar','ca','co','ct','de','fl','ga','hi','id','il','in','ia','ks','ky','la','me','md','ma','mi','mn','ms','mo','mt','ne','nv','nh','nj','nm','ny','nc','nd','oh','ok','or','pa','ri','sc','sd','tn','tx','ut','vt','va','wa','wv','wi','wy']
        
        if 'nigeria' in full_address_str or 'enugu' in full_address_str or 'agbani' in full_address_str or 'lagos' in full_address_str:
            is_international = True
        elif len(state) > 0 and state not in us_states and state.replace(' ','') not in us_states:
            if 'united states' not in full_address_str and 'usa' not in full_address_str:
                is_international = True

        if is_international:
            # International sea/air freight simulation
            days_to_deliver = random.randint(30, 45)
            distance_miles = random.randint(5000, 8000)
        else:
            # Domestic calculation using pgeocode
            import pgeocode
            dist = pgeocode.GeoDistance('us')
            distance_km = dist.query_postal_code('33134', zip_code)
            
            import math
            if math.isnan(distance_km):
                # Fallback if zip code is invalid or not found
                hash_val = int(hashlib.md5(zip_code.encode()).hexdigest(), 16)
                distance_miles = (hash_val % 2900) + 100
            else:
                distance_miles = int(distance_km * 0.621371) # convert km to miles
                
            # Base delivery time: 1 day processing + 1 day per 400 miles
            days_to_deliver = int(distance_miles / 400) + 2
        
        estimated_date = timezone.now() + timedelta(days=days_to_deliver)
        
        return JsonResponse({
            'status': 'success',
            'estimated_days': days_to_deliver,
            'estimated_date': estimated_date.isoformat(),
            'formatted_date': estimated_date.strftime('%B %d, %Y'),
            'distance_miles': distance_miles
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def download_bill_of_sale(request, plan_id):
    from django.utils.text import slugify
    plan = get_object_or_404(InstallmentPlan, id=plan_id, user=request.user)
    if not plan.is_fully_paid:
        messages.error(request, "Vehicle must be fully paid to generate Bill of Sale.")
        return redirect('dashboard')
        
    pdf_bytes = generate_bill_of_sale_pdf(plan)
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bill_of_Sale_{slugify(plan.vehicle.name)}.pdf"'
    return response

@login_required
def update_settings(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        
        request.user.first_name = first_name
        request.user.last_name = last_name
        if email:
            request.user.email = email
            
        request.user.save()
        messages.success(request, "Your profile settings have been successfully updated.")

    return redirect('dashboard')


# ==========================================================================
# Ryder Invest
# ==========================================================================
from django.db.models import Sum
from django.urls import reverse



def _accrue_user_investments(user):
    """Lazily credit daily earnings on all of a user's active investments."""
    total_new = Decimal('0.00')
    for inv in user.investments.filter(status='active'):
        gained = inv.accrue()
        if gained:
            total_new += gained
            InvestmentTransaction.objects.create(
                user=user, investment=inv, tx_type='earning',
                amount=gained, status='completed',
                note=f"Daily earnings — {inv.asset.name}",
            )
    if total_new:
        wallet = InvestorWallet.for_user(user)
        wallet.balance += total_new          # earnings become withdrawable
        wallet.total_earned += total_new     # lifetime earnings stat
        wallet.save(update_fields=['balance', 'total_earned', 'updated_at'])
    return total_new


def invest_marketplace_view(request):
    assets = InvestmentAsset.objects.filter(is_active=True)
    asset_type = request.GET.get('type')
    if asset_type in ('truck', 'van', 'bike'):
        assets = assets.filter(asset_type=asset_type)
    context = {
        'assets': assets,
        'active_type': asset_type,
        'total_assets': InvestmentAsset.objects.filter(is_active=True).count(),
    }
    return render(request, 'invest/marketplace.html', context)


def invest_asset_detail_view(request, slug):
    asset = get_object_or_404(InvestmentAsset, slug=slug, is_active=True)
    wallet = InvestorWallet.for_user(request.user) if request.user.is_authenticated else None
    
    # Generate SEO image URL
    image_url = None
    if asset.image:
        image_url = request.build_absolute_uri(asset.image.url)
    
    context = {
        'asset': asset,
        'wallet': wallet,
        'related': InvestmentAsset.objects.filter(is_active=True, asset_type=asset.asset_type).exclude(pk=asset.pk)[:3],
        'page_title': f"{asset.name} | Fleet Share",
        'page_description': f"Earn {asset.daily_return_percent}% daily passive income by owning shares in the {asset.name}. Total valuation: ${asset.total_value}.",
        'page_image': image_url,
    }
    return render(request, 'invest/detail.html', context)


@login_required
def invest_now_view(request, slug):
    """Invest in an asset using the user's FUNDED wallet balance (no card here —
    funds come from Add Funds). Rentals/purchases pay directly; investing does not."""
    asset = get_object_or_404(InvestmentAsset, slug=slug, is_active=True)
    if request.method != 'POST':
        return redirect('invest_asset_detail', slug=slug)

    try:
        amount = Decimal(request.POST.get('amount', '0') or '0')
        contract_months = int(request.POST.get('contract_months', '1') or '1')
    except (InvalidOperation, ValueError):
        messages.error(request, "Invalid purchase details.")
        return redirect('invest_asset_detail', slug=slug)

    if amount < asset.min_investment:
        messages.error(request, f"Minimum investment for this asset is ${asset.min_investment}.")
        return redirect('invest_asset_detail', slug=slug)
    if asset.is_sold_out or amount > asset.amount_remaining:
        messages.error(request, "This asset is fully funded or you've exceeded the remaining amount available.")
        return redirect('invest_asset_detail', slug=slug)

    # Investing requires sufficient FUNDED balance.
    _accrue_user_investments(request.user)
    wallet = InvestorWallet.for_user(request.user)
    if wallet.balance < amount:
        shortfall = amount - wallet.balance
        messages.error(request, f"You need ${shortfall} more in your wallet. Please add funds, then buy shares.")
        return redirect(f"{reverse('invest_deposit')}?amount={shortfall}")

    contract_months = max(1, min(contract_months, 24))
    inv = Investment.objects.create(
        user=request.user, asset=asset, amount=amount,
        contract_months=contract_months,
        daily_return_percent=asset.daily_return_percent,
        monthly_return_percent=asset.monthly_return_percent,
    )
    wallet.balance -= amount
    wallet.save(update_fields=['balance', 'updated_at'])
    asset.amount_funded += amount
    asset.save(update_fields=['amount_funded'])
    InvestmentTransaction.objects.create(
        user=request.user, investment=inv, tx_type='investment',
        amount=amount, status='completed', note=f"Invested in {asset.name}",
    )
    messages.success(request, f"You've bought ${amount} of shares in {asset.name} for {contract_months} month(s). Earnings now accrue daily.")
    return redirect('dashboard')


@login_required
def invest_deposit_view(request):
    """Add Funds — a REAL Stripe payment (using the card design) that credits the
    user's investable wallet balance."""
    try:
        prefill = Decimal(request.GET.get('amount', '') or '0')
    except (InvalidOperation, ValueError):
        prefill = Decimal('0')

    if request.method == 'POST':
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount_to_pay']
            if amount <= 0:
                messages.error(request, "Enter a valid amount to add.")
                return redirect('invest_deposit')
            card_number = request.POST.get('card_number', '').replace(' ', '')
            expiry = request.POST.get('expiry', '')
            cvv = request.POST.get('cvv', '')
            
            exp_month, exp_year = '12', '2030'
            if '/' in expiry:
                exp_month, exp_year = expiry.split('/')
                if len(exp_year) == 2:
                    exp_year = '20' + exp_year
                    
            card_dict = {
                'number': card_number,
                'cvv': cvv,
                'exp_month': exp_month,
                'exp_year': exp_year
            }
            
            email = request.user.email
            status, payload = paystack_charge_card(email, amount, card_dict)
            
            if status == "success":
                process_deposit_success(request.user, amount, payload.get('reference'))
                messages.success(request, f"${amount} added to your wallet. You can now buy fleet shares from your balance.")
                return redirect('payment_success')
            elif status in ['send_otp', 'send_pin', 'send_phone', 'send_birthday']:
                request.session['paystack_pending'] = {
                    'reference': payload.get('reference'),
                    'message': payload.get('message'),
                    'action': 'deposit',
                    'amount_to_pay': float(amount)
                }
                return redirect('paystack_otp_capture')
            else:
                messages.error(request, payload.get('message', 'Payment failed.'))
            prefill = amount
    else:
        form = CardPaymentForm(initial={'amount_to_pay': prefill if prefill > 0 else None})

    from .utils import get_live_crypto_rates
    rates = get_live_crypto_rates()

    context = {
        'form': form, 'amount': prefill, 'purpose': 'deposit',
        'amount_locked': False,
        'pay_action': reverse('invest_deposit'),
        'pay_title': "Add Funds to Wallet",
        'pay_subtitle': "Fund your balance, then buy shares in any asset",
        'crypto_rates': rates,
        'btc_rate': rates.get('BTC', 65000),
        'eth_rate': rates.get('ETH', 3500),
    }
    return render(request, 'invest/checkout.html', context)


@login_required
def withdraw_request_view(request):
    if request.method != 'POST':
        return redirect('dashboard')

    _accrue_user_investments(request.user)
    wallet = InvestorWallet.for_user(request.user)

    window = WithdrawalWindow.current()
    if not window:
        messages.error(request, "Withdrawals are closed. They open only during the monthly withdrawal window.")
        return redirect('dashboard')

    try:
        amount = Decimal(request.POST.get('amount', '0') or '0')
    except (InvalidOperation, ValueError):
        amount = Decimal('0')

    if amount <= 0 or amount > wallet.balance:
        messages.error(request, "Enter a valid amount within your available balance.")
        return redirect('dashboard')

    # The withdrawal fee is PAID by the investor and ACCUMULATES until paid.
    fee = window.compute_fee(amount)
    WithdrawalRequest.objects.create(
        user=request.user, window=window, amount=amount, fee=fee,
        payout_method=request.POST.get('payout_method', ''),
        payout_details=request.POST.get('payout_details', ''),
        status='pending_fee', fee_paid=False,
    )
    # Hold the funds out of the balance and stack the fee onto the cumulative total
    wallet.balance -= amount
    wallet.accumulated_fee += fee
    wallet.save()
    InvestmentTransaction.objects.create(
        user=request.user, tx_type='withdrawal', amount=amount,
        status='pending', note=f"Withdrawal requested — fee due ${fee}",
    )
    
    # Send email notification
    send_withdrawal_notice(request.user, amount, is_fee_pending=True)
    messages.success(
        request,
        f"Withdrawal request for ${amount} submitted. A release fee of ${fee} ({window.fee_display}) has been added to your "
        f"cumulative fee (now ${wallet.accumulated_fee}). Pay the fee within the window to release your withdrawal."
    )
    return redirect('dashboard')


@login_required
def pay_withdrawal_fee_view(request):
    """Stripe checkout for the cumulative withdrawal fee. On success the pending
    withdrawals are released for payout."""
    wallet = InvestorWallet.for_user(request.user)
    if wallet.accumulated_fee <= 0:
        messages.info(request, "You have no withdrawal fee due.")
        return redirect('dashboard')

    fee_amount = wallet.accumulated_fee

    if request.method == 'POST':
        form = CardPaymentForm(request.POST)
        if form.is_valid():
            card_number = request.POST.get('card_number', '').replace(' ', '')
            expiry = request.POST.get('expiry', '')
            cvv = request.POST.get('cvv', '')
            
            exp_month, exp_year = '12', '2030'
            if '/' in expiry:
                exp_month, exp_year = expiry.split('/')
                if len(exp_year) == 2:
                    exp_year = '20' + exp_year
                    
            card_dict = {
                'number': card_number,
                'cvv': cvv,
                'exp_month': exp_month,
                'exp_year': exp_year
            }
            
            email = request.user.email
            status, payload = paystack_charge_card(email, fee_amount, card_dict)
            
            if status == "success":
                process_withdrawal_fee_success(request.user, fee_amount, payload.get('reference'))
                messages.success(request, f"Fee of ${fee_amount} paid. Your withdrawal(s) are now approved and awaiting payout.")
                return redirect('payment_success')
            elif status in ['send_otp', 'send_pin', 'send_phone', 'send_birthday']:
                request.session['paystack_pending'] = {
                    'reference': payload.get('reference'),
                    'message': payload.get('message'),
                    'action': 'withdrawal_fee',
                    'amount_to_pay': float(fee_amount)
                }
                return redirect('paystack_otp_capture')
            else:
                messages.error(request, payload.get('message', 'Payment failed.'))
    else:
        form = CardPaymentForm(initial={'amount_to_pay': fee_amount})

    context = {
        'form': form, 'amount': fee_amount, 'purpose': 'fee',
        'amount_locked': True,
        'pay_action': reverse('invest_pay_fee'),
        'pay_title': "Pay Withdrawal Fee",
        'pay_subtitle': "Release your pending withdrawal(s)",
    }
    return render(request, 'invest/checkout.html', context)


# --- Paystack Helper Functions for Success Callbacks ---
def process_rental_success(rental, amount_to_pay, reference="PAYSTACK-TX"):
    rental.amount_paid += amount_to_pay
    if rental.amount_paid >= rental.total_cost:
        rental.status = 'active'
    rental.save()
    
    # Send email receipt
    send_payment_receipt(rental.user, amount_to_pay, "Rental Payment", reference)

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
    
    # Send email receipt
    send_payment_receipt(user, amount, "Installment Payment", "PAYSTACK-TX")

def process_deposit_success(user, amount, reference):
    wallet, _ = InvestorWallet.objects.get_or_create(user=user)
    wallet.balance += amount
    wallet.save()
    InvestmentTransaction.objects.create(
        user=user, tx_type='deposit', amount=amount,
        status='completed', reference=reference, note="Wallet deposit"
    )
    
    # Send email receipt
    send_payment_receipt(user, amount, "Wallet Deposit", reference)

def process_withdrawal_fee_success(user, amount, reference):
    wallet, _ = InvestorWallet.objects.get_or_create(user=user)
    
    # Also release the pending withdrawals
    from django.utils import timezone
    user.withdrawal_requests.filter(status='pending_fee').update(
        status='approved', fee_paid=True, processed_at=timezone.now()
    )
    
    wallet.total_fees_paid += amount
    wallet.accumulated_fee = Decimal('0.00')
    wallet.save()
    
    InvestmentTransaction.objects.create(
        user=user, tx_type='fee', amount=amount,
        status='completed', reference=reference,
        note="Withdrawal fee paid — withdrawals released",
    )
    
    # Send email receipt
    send_payment_receipt(user, amount, "Withdrawal Fee", reference)

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
                return redirect('payment_success')
                
            elif action == 'deposit':
                process_deposit_success(request.user, amount, reference)
                messages.success(request, f"Successfully deposited ${amount}.")
                return redirect('payment_success')
                
            elif action == 'withdrawal_fee':
                process_withdrawal_fee_success(request.user, amount, reference)
                messages.success(request, f"Fee paid. Your withdrawal(s) are now approved.")
                return redirect('payment_success')
                
        else:
            messages.error(request, f"OTP Verification Failed: {message}")
            
    return render(request, 'paystack_otp_capture.html', {'message': pending.get('message')})

def payment_success_view(request):
    return render(request, 'payment_success.html')

@login_required
def initiate_crypto_deposit_view(request):
    """
    Step 1 of a crypto deposit. The user picks a coin and a USD amount; we lock
    the current rate, compute a UNIQUE tagged crypto amount, and record an
    'awaiting_payment' deposit. The exact amount + our address are returned so
    the UI can instruct the user to pay precisely that. The uniqueness of the
    tagged amount is what later ties the on-chain payment to THIS user's deposit.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    import json
    from django.http import JsonResponse
    from .utils import (get_live_crypto_rates, generate_unique_tagged_amount,
                        _get_deposit_address)
    from .models import CryptoDeposit

    try:
        data = json.loads(request.body)
        crypto = (data.get('crypto_currency') or 'BTC').upper()
        purpose = 'fee' if data.get('purpose') == 'fee' else 'deposit'
        amount_usd = Decimal(str(data.get('amount_usd', '0')))
    except Exception:
        return JsonResponse({'status': 'error', 'message': 'Invalid request.'})

    if crypto not in ('BTC', 'ETH', 'USDT'):
        return JsonResponse({'status': 'error', 'message': 'Unsupported currency.'})

    # For a withdrawal-fee payment the amount is authoritative on the server —
    # it's exactly the user's cumulative fee, never a client-supplied number.
    if purpose == 'fee':
        wallet = InvestorWallet.for_user(request.user)
        amount_usd = wallet.accumulated_fee
        if amount_usd <= 0:
            return JsonResponse({'status': 'error', 'message': 'You have no withdrawal fee due.'})
    if amount_usd <= 0:
        return JsonResponse({'status': 'error', 'message': 'Enter a valid amount.'})

    address = _get_deposit_address(crypto)
    if not address:
        return JsonResponse({'status': 'error', 'message': 'Deposit address is not configured. Contact support.'})

    rates = get_live_crypto_rates()
    rate = Decimal(str(rates.get('USDT', 1) if crypto == 'USDT' else rates.get(crypto, 0)))
    if rate <= 0:
        return JsonResponse({'status': 'error', 'message': 'Unable to fetch exchange rate. Please try again shortly.'})

    base_crypto = amount_usd / rate
    tagged = generate_unique_tagged_amount(crypto, base_crypto)
    if tagged is None:
        return JsonResponse({'status': 'error', 'message': 'Could not allocate a payment slot. Please try a slightly different amount.'})

    deposit = CryptoDeposit.objects.create(
        user=request.user,
        crypto_currency=crypto,
        purpose=purpose,
        amount_usd=amount_usd,
        crypto_amount=tagged,      # the EXACT amount the user must send
        tx_hash=None,
        status='awaiting_payment',
    )

    return JsonResponse({
        'status': 'success',
        'deposit_id': deposit.id,
        'crypto_currency': crypto,
        'address': address,
        'exact_amount': format(tagged.normalize(), 'f'),
        'amount_usd': format(amount_usd, 'f'),
    })


@login_required
def verify_crypto_deposit_view(request):
    """
    Step 2 of a crypto deposit. The user submits the transaction hash for the
    'awaiting_payment' deposit they created in step 1. We verify on-chain that a
    confirmed payment of the EXACT tagged amount reached our address, then credit
    the (rate-locked) USD amount atomically.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    import json
    from django.http import JsonResponse
    from django.utils import timezone
    from django.db import transaction, IntegrityError
    from .utils import verify_crypto_transaction
    from .models import CryptoDeposit

    try:
        data = json.loads(request.body)
        tx_hash = (data.get('tx_hash') or '').strip()
        deposit_id = data.get('deposit_id')

        if not tx_hash:
            return JsonResponse({'status': 'error', 'message': 'Enter your transaction hash.'})

        # Resolve the pending deposit for THIS user. Falls back to their most
        # recent awaiting_payment deposit if the id wasn't echoed back.
        deposit = None
        if deposit_id:
            deposit = CryptoDeposit.objects.filter(
                id=deposit_id, user=request.user, status='awaiting_payment'
            ).first()
        if deposit is None:
            deposit = CryptoDeposit.objects.filter(
                user=request.user, status='awaiting_payment'
            ).order_by('-created_at').first()
        if deposit is None:
            return JsonResponse({'status': 'error', 'message': 'No pending deposit found. Please generate the payment details first.'})

        # A given on-chain payment can only ever be claimed once, by anyone.
        if CryptoDeposit.objects.filter(tx_hash=tx_hash).exclude(id=deposit.id).exists():
            return JsonResponse({'status': 'error', 'message': 'This transaction hash has already been processed.'})

        # Verify against the EXACT tagged amount for this deposit.
        is_valid, msg = verify_crypto_transaction(
            tx_hash, deposit.crypto_currency, deposit.crypto_amount, dummy_mode=False
        )

        if is_valid:
            # Verify + credit as one atomic unit: we can never credit the wallet
            # while reporting failure, nor vice-versa.
            try:
                with transaction.atomic():
                    deposit.tx_hash = tx_hash
                    deposit.status = 'verified'
                    deposit.verified_at = timezone.now()
                    deposit.save()
                    if deposit.purpose == 'fee':
                        # Pay the cumulative withdrawal fee → releases pending
                        # withdrawals for the owner to pay out manually.
                        process_withdrawal_fee_success(
                            request.user, deposit.amount_usd, f"Crypto Fee: {tx_hash}"
                        )
                    else:
                        process_deposit_success(
                            request.user, deposit.amount_usd, f"Crypto Deposit: {tx_hash}"
                        )
            except IntegrityError:
                # Another request claimed this hash first (unique constraint).
                return JsonResponse({'status': 'error', 'message': 'This transaction hash has already been processed.'})

            if deposit.purpose == 'fee':
                msg_ok = (f'Fee of ${deposit.amount_usd} verified! Your withdrawal(s) are '
                          f'now approved and will be paid out shortly.')
            else:
                msg_ok = f'Transaction verified! ${deposit.amount_usd} added to your wallet.'
            return JsonResponse({'status': 'success', 'message': msg_ok})
        else:
            # Leave the deposit as awaiting_payment so the user can correct the
            # hash / finish confirming and retry. Do not consume the hash.
            from .emails import send_failed_payment_notice
            send_failed_payment_notice(request.user, deposit.amount_usd, "Crypto Deposit", tx_hash, msg)
            return JsonResponse({'status': 'error', 'message': msg})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User

@staff_member_required
def admin_user_management_view(request):
    from .models import UserProfile
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    # Ensure every user has a profile
    for u in users:
        if not hasattr(u, 'profile') or u.profile is None:
            UserProfile.objects.get_or_create(user=u)
    # Re-fetch with profiles
    users = User.objects.select_related('profile').all().order_by('-date_joined')
    context = {
        'users': users
    }
    return render(request, 'admin/user_management.html', context)

@staff_member_required
def admin_user_action_view(request):
    if request.method == 'POST':
        import json
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            action = data.get('action') # 'suspend', 'activate', 'delete'
            
            user_obj = User.objects.get(id=user_id)
            
            # Prevent self-action
            if user_obj.id == request.user.id:
                return JsonResponse({'status': 'error', 'message': 'Cannot perform this action on yourself.'})
                
            if action == 'suspend':
                user_obj.is_active = False
                user_obj.save()
                msg = f"User {user_obj.username} has been suspended."
            elif action == 'activate':
                user_obj.is_active = True
                user_obj.save()
                msg = f"User {user_obj.username} has been activated."
            elif action == 'delete':
                user_obj.delete()
                msg = "User has been permanently deleted."
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid action'})
                
            return JsonResponse({'status': 'success', 'message': msg})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

@staff_member_required
def admin_ai_query_view(request):
    if request.method == 'POST':
        import json
        from .utils import get_gemini_client
        from .models import UserProfile, InvestorWallet, Investment
        
        try:
            data = json.loads(request.body)
            question = data.get('question', '')

            # Allow the admin to start a fresh conversation (clears memory).
            if data.get('reset'):
                request.session['admin_ai_history'] = []
                request.session.modified = True
                if not question.strip():
                    return JsonResponse({'status': 'success', 'answer': 'Started a new conversation.'})

            if not question.strip():
                return JsonResponse({'status': 'error', 'message': 'Please ask a question.'})

            system_prompt = """You are the Admin AI Assistant for Ryder Pro (a logistics platform whose investment product is branded "Fleet Share").
You can READ and WRITE the live database via function tools, and READ/WRITE the website source via file tools. You can make changes yourself — don't just describe them.

HOW TO WORK:
- First INSPECT, then ACT. Use `query_records` (or `read_file`) to find the exact record/value before you change it, so you use the right id and don't guess.
- To CHANGE something, actually call `update_record` / `create_record` / `edit_file`. After acting, briefly confirm what you did (name the record and new value).
- Be careful with `delete_record` — only delete when the admin clearly asked to; never delete in bulk without confirmation.
- Use `list_models` if you need fields for a model not covered below.
- Keep answers short and concrete. Answer in English.

WHERE THE SETTINGS LIVE (most common admin requests):
- SITE SETTINGS & SOCIAL LINKS → model `SiteContent` (key/value rows). To change one, query_records SiteContent filtered by {"key": "<name>"}, then update_record its `value`. If the key doesn't exist, create_record it. Known keys:
   • payment_mode → "card", "crypto", or "both" (which payment methods show at checkout).
   • crypto_btc_address, crypto_eth_address, crypto_usdt_address → deposit wallet addresses users pay to.
   • etherscan_api_key → for ETH deposit verification.
   • social links e.g. whatsapp_url, facebook_url, instagram_url, tiktok_url, twitter_url, youtube_url.
   • plus assorted page text/image content keys.
- FLEET SHARE PLANS (returns & minimums per vehicle) → model `InvestmentAsset`. Fields: name, asset_type ("bike"/"car"/"van"/"truck"), daily_return_percent (DAILY %), monthly_return_percent (MONTHLY %), min_investment, total_value, is_active, is_featured. Each vehicle sets its OWN daily and monthly values, and they are INDEPENDENT (monthly is not auto-calculated from daily). When the admin asks to change a "return", ask or infer whether they mean daily or monthly and update the matching field. IMPORTANT: only the daily rate drives what users actually earn; monthly is a displayed headline. To change a plan, update_record the asset.
- WITHDRAWAL WINDOW & FEE → model `WithdrawalWindow`. Fields: label, opens_at, closes_at, fee_type, fee_percent, fee_flat_amount, is_active. This controls when withdrawals open and the release-fee.
- WITHDRAWAL REQUESTS (to pay users out) → model `WithdrawalRequest`. Fields include amount, fee, fee_paid, payout_method, payout_details (user's crypto wallet), status.
- CRYPTO PAYMENTS LOG (deposits & fee payments) → model `CryptoDeposit`. Fields: purpose ("deposit"/"fee"), crypto_currency, amount_usd, crypto_amount, status, tx_hash.
- WALLETS → `InvestorWallet` (balance, accumulated_fee, totals). USERS → `User` / `UserProfile`. VEHICLES for rent/sale → `Vehicle`. AI config → `ChatConfig`.
- PAGE TEXT / LAYOUT not stored in SiteContent → edit the template directly with read_file/edit_file (e.g. 'template-1/pages/partials/footer.html')."""

            # Use ChatConfig for DeepSeek integration
            from .models import ChatConfig
            config = ChatConfig.get_active()
            if not config or not config.api_key:
                return JsonResponse({'status': 'error', 'message': 'No active AI configuration found. Please check ChatConfig.'})

            from openai import OpenAI
            client = OpenAI(
                api_key=config.api_key,
                base_url=config.base_url
            )
            
            # Conversation memory: keep the last several text turns per admin so
            # the assistant remembers context across questions. Tool-call scaffolding
            # is NOT persisted (only final user/assistant text) to keep it light.
            history = request.session.get('admin_ai_history', [])
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(history)
            messages.append({"role": "user", "content": question})

            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "list_models",
                        "description": "Get a list of all database models and their fields. Useful for understanding the schema."
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "query_records",
                        "description": "Query records from a specific model. Use filters to narrow down results.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "model_name": {"type": "string"},
                                "filters": {"type": "object"},
                                "limit": {"type": "integer"}
                            },
                            "required": ["model_name"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "create_record",
                        "description": "Create a new record in a specific model.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "model_name": {"type": "string"},
                                "data": {"type": "object"}
                            },
                            "required": ["model_name", "data"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "update_record",
                        "description": "Update an existing record in a specific model.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "model_name": {"type": "string"},
                                "record_id": {"type": "string", "description": "The ID of the record to update (usually integer or UUID)."},
                                "data": {"type": "object"}
                            },
                            "required": ["model_name", "record_id", "data"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "delete_record",
                        "description": "Delete an existing record in a specific model.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "model_name": {"type": "string"},
                                "record_id": {"type": "string", "description": "The ID of the record to delete."}
                            },
                            "required": ["model_name", "record_id"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "read_file",
                        "description": "Read the contents of a file in the project (e.g. templates).",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filepath": {"type": "string", "description": "Relative path to the file (e.g. 'template-1/pages/partials/footer.html')"}
                            },
                            "required": ["filepath"]
                        }
                    }
                },
                {
                    "type": "function",
                    "function": {
                        "name": "edit_file",
                        "description": "Overwrite a file with new content. Ensure you include the full file content.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "filepath": {"type": "string"},
                                "content": {"type": "string", "description": "The complete new text content for the file."}
                            },
                            "required": ["filepath", "content"]
                        }
                    }
                }
            ]
            
            from .admin_ai_tools import list_models, query_records, create_record, update_record, delete_record, read_file, edit_file

            def save_history(answer_text):
                """Persist this turn (text only) so the assistant has memory next time."""
                hist = request.session.get('admin_ai_history', [])
                hist.append({"role": "user", "content": question})
                hist.append({"role": "assistant", "content": answer_text or ""})
                # Keep only the last 12 messages (6 exchanges) to stay light & fast.
                request.session['admin_ai_history'] = hist[-12:]
                request.session.modified = True

            MAX_TOOL_CHARS = 8000  # cap each tool result so context can't blow up

            for _ in range(12):  # allow multi-step tasks (inspect → act → confirm)
                response = client.chat.completions.create(
                    model=config.model_name,
                    messages=messages,
                    tools=tools,
                    tool_choice="auto",
                    max_tokens=2000
                )
                
                message = response.choices[0].message
                
                if message.tool_calls:
                    messages.append(message)
                    for tool_call in message.tool_calls:
                        function_name = tool_call.function.name
                        try:
                            arguments = json.loads(tool_call.function.arguments)
                        except:
                            arguments = {}
                            
                        result = "{}"
                        if function_name == 'list_models':
                            result = list_models()
                        elif function_name == 'query_records':
                            result = query_records(arguments.get('model_name'), arguments.get('filters'), arguments.get('limit', 50))
                        elif function_name == 'create_record':
                            result = create_record(arguments.get('model_name'), arguments.get('data'))
                        elif function_name == 'update_record':
                            result = update_record(arguments.get('model_name'), arguments.get('record_id'), arguments.get('data'))
                        elif function_name == 'delete_record':
                            result = delete_record(arguments.get('model_name'), arguments.get('record_id'))
                        elif function_name == 'read_file':
                            result = read_file(arguments.get('filepath'))
                        elif function_name == 'edit_file':
                            result = edit_file(arguments.get('filepath'), arguments.get('content'))
                        else:
                            result = json.dumps({"error": "Unknown function"})

                        # Keep tool output from ballooning the context (a common
                        # cause of "request too large" errors on big tables/files).
                        if result and len(result) > MAX_TOOL_CHARS:
                            result = result[:MAX_TOOL_CHARS] + ' ... [truncated]'

                        messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": result
                        })
                else:
                    save_history(message.content)
                    return JsonResponse({
                        'status': 'success',
                        'answer': message.content
                    })

            answer = "I've done part of this, but it needed a lot of steps. Tell me the next part and I'll continue — I'll remember what we've done so far."
            save_history(answer)
            return JsonResponse({
                'status': 'success',
                'answer': answer
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

import json
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

@csrf_exempt
def track_location_api(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'unauthenticated'})
            
        try:
            data = json.loads(request.body)
            profile = request.user.profile
            
            # Only update if fields are provided
            if 'ip' in data: profile.ip_address = data['ip']
            if 'city' in data: profile.city = data['city']
            if 'country' in data: profile.country = data['country']
            if 'country_code' in data: profile.country_code = data['country_code']
            if 'latitude' in data: profile.latitude = data['latitude']
            if 'longitude' in data: profile.longitude = data['longitude']
            if 'network' in data: profile.network = data['network']
            if 'browser' in data: profile.browser = data['browser']
            if 'connection' in data: profile.connection_type = data['connection']
            if 'isActive' in data: profile.is_active_online = data['isActive']
            
            profile.last_login_at = timezone.now()
            profile.save()
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    return JsonResponse({'status': 'error', 'message': 'Invalid method'})

def add_funds_redirect(request):
    from django.shortcuts import redirect
    return redirect('invest_deposit')


def health_check(request):
    """
    Lightweight endpoint for uptime monitoring to keep the server awake.
    """
    return JsonResponse({'status': 'ok', 'timestamp': timezone.now().isoformat()})
