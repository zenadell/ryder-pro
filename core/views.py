from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Q
from decimal import Decimal
import stripe
from django.conf import settings
from .models import (
    Vehicle, Category, BlogPost, TeamMember, Review, ContactMessage, GalleryImage, Job, TradeInRequest, RentalRequest, Shipment, SiteContent, PageVisit,
    InstallmentPlan, PaymentTransaction
)
from .forms import (
    ContactForm, NewsletterForm, FinancingApplicationForm, JobApplicationForm, TradeInRequestForm, RentalRequestForm, ReviewForm, DummyPaymentForm
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
    import random
    from django.utils.timezone import now
    from datetime import timedelta
    
    try:
        social_proof_mode = SiteContent.objects.get(key='social_proof_mode').value
    except SiteContent.DoesNotExist:
        social_proof_mode = 'simulated'
        
    if social_proof_mode == 'real':
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
        # Fallback to simulated if real viewers is 1 (just the user) so it looks better
        if live_viewers <= 1:
            live_viewers = random.randint(3, 8)
    else:
        live_viewers = random.randint(12, 24)
    
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
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('financing_success', slug=vehicle.slug)
    else:
        form = FinancingApplicationForm()
        
    context = {
        'vehicle': vehicle,
        'form': form
    }
    return render(request, 'financing/apply.html', context)

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

def trade_in_view(request):
    if request.method == 'POST':
        form = TradeInRequestForm(request.POST, request.FILES)
        if form.is_valid():
            trade_in = form.save(commit=False)
            if request.user.is_authenticated:
                trade_in.user = request.user
            trade_in.save()
            messages.success(request, 'Your trade-in request has been submitted successfully!')
            return redirect('trade_in_success')
    else:
        form = TradeInRequestForm()
        
    return render(request, 'trade-in/index.html', {'form': form})

def trade_in_success_view(request):
    return render(request, 'trade-in/success.html')

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

def rental_checkout_view(request, id):
    rental = get_object_or_404(RentalRequest, id=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    
    if request.method == 'POST':
        form = DummyPaymentForm(request.POST)
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
            
            try:
                payment_method = stripe.PaymentMethod.create(
                    type="card",
                    card={
                        "number": card_number,
                        "exp_month": int(exp_month),
                        "exp_year": int(exp_year),
                        "cvc": cvv,
                    },
                )
                
                intent = stripe.PaymentIntent.create(
                    amount=int(amount_to_pay * 100),
                    currency="usd",
                    payment_method=payment_method.id,
                    confirm=True,
                    automatic_payment_methods={
                        'enabled': True,
                        'allow_redirects': 'never'
                    }
                )
                
                rental.amount_paid += amount_to_pay
                if rental.amount_paid >= rental.total_cost:
                    rental.status = 'active'
                rental.save()
                messages.success(request, f'Payment of ${amount_to_pay} successful! Your rental request is confirmed.')
                return redirect('rental_success', id=rental.id)
                
            except stripe.error.CardError as e:
                messages.error(request, f"{e.user_message}")
            except Exception as e:
                messages.error(request, f"Payment error: {str(e)}")
    else:
        form = DummyPaymentForm(initial={'amount_to_pay': rental.amount_remaining})
        
    return render(request, 'rentals/checkout.html', {'form': form, 'rental': rental})

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
            
            # --- MOCK API INTEGRATION (Shippo / AfterShip) ---
            # In Phase 3, this will use shipment.tracking_provider and make a real HTTP request
            if shipment.tracking_provider:
                # Mocking a response from a logistics API
                api_updates = [
                    {'time': timezone.now() - timezone.timedelta(days=1), 'location': shipment.origin_address, 'message': 'Package received by carrier'},
                    {'time': timezone.now() - timezone.timedelta(hours=5), 'location': shipment.current_location or 'Hub', 'message': 'In transit to destination'},
                ]
            # -------------------------------------------------
            
        except Shipment.DoesNotExist:
            error = "We couldn't find a shipment with that Tracking ID. Please verify and try again."
            
    context = {
        'shipment': shipment, 
        'error': error, 
        'tracking_id': tracking_id,
        'api_updates': api_updates,
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
    
    context = {
        'financing_apps': financing_apps,
        'job_apps': job_apps,
        'trade_ins': trade_ins,
        'rentals': rentals,
        'shipments': shipments,
        'installment_plans': installment_plans,
        'payments': payments,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def make_payment_view(request, plan_id):
    plan = get_object_or_404(InstallmentPlan, id=plan_id, user=request.user)
    
    if request.method == 'POST':
        # Mock payment processor
        amount = Decimal(request.POST.get('amount', '0.00'))
        
        if amount > 0:
            if plan.accumulated_penalty_interest > 0:
                # Pay off penalty first
                if amount >= plan.accumulated_penalty_interest:
                    amount -= plan.accumulated_penalty_interest
                    plan.accumulated_penalty_interest = Decimal('0.00')
                else:
                    plan.accumulated_penalty_interest -= amount
                    amount = Decimal('0.00')
                    
            if amount > 0:
                plan.principal_balance -= amount
                plan.down_payment_paid += amount
                
                # Check for tier 1 upgrade if it's currently tier 2
                if plan.tier == 'tier2':
                    if plan.down_payment_paid >= (plan.total_amount * Decimal('0.60')):
                        plan.tier = 'tier1'
                        plan.is_vehicle_released = True
                        plan.monthly_due_date = timezone.now().day
                        
                        # Trigger Shipment Creation automatically
                        Shipment.objects.create(
                            user=request.user,
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
                user=request.user,
                installment_plan=plan,
                amount=Decimal(request.POST.get('amount', '0.00')),
                payment_type='installment',
                status='completed'
            )
            
            messages.success(request, f"Payment of ${request.POST.get('amount')} processed successfully!")
            return redirect('dashboard')
            
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
