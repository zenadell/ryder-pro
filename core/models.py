from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from decimal import Decimal
import os
from django.core.files.storage import FileSystemStorage

if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    from cloudinary_storage.storage import RawMediaCloudinaryStorage
    from ryder_pro.storage import CustomVideoMediaCloudinaryStorage
    RAW_STORAGE = RawMediaCloudinaryStorage()
    VIDEO_STORAGE = CustomVideoMediaCloudinaryStorage()
else:
    RAW_STORAGE = FileSystemStorage()
    VIDEO_STORAGE = FileSystemStorage()

# Global & Static Content
class SiteContent(models.Model):
    key = models.SlugField(unique=True, help_text="e.g. 'home_hero_title'")
    value = models.TextField(help_text="The text or HTML content", blank=True, null=True)
    image = models.ImageField(upload_to='site_images/', blank=True, null=True, help_text="Use this for image content")
    video = models.FileField(upload_to='site_videos/', storage=VIDEO_STORAGE, blank=True, null=True, help_text="Use this for video content (mp4/webm)")
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key

class GeminiAPIKey(models.Model):
    key = models.CharField(max_length=255, unique=True, help_text="Gemini API Key")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.key[:10]}... (Active: {self.is_active})"
    
    class Meta:
        verbose_name = "Gemini API Key"
        verbose_name_plural = "Gemini API Keys"

class BulkImport(models.Model):
    class Meta:
        managed = False
        verbose_name_plural = "AI Bulk Importer"

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.email}"

class TeamMember(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    excerpt = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    published_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

# Vehicle Marketplace
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class VehicleFeature(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
    ]

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='vehicles')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.PositiveIntegerField()
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2)
    full_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, help_text="Required for financing")
    mileage = models.PositiveIntegerField(help_text="Mileage in miles or km")
    condition = models.CharField(max_length=100)
    vin = models.CharField(max_length=17, blank=True, null=True, unique=True, help_text="Vehicle Identification Number")
    financing_eligible = models.BooleanField(default=False)
    minimum_down_payment_percent = models.DecimalField(max_digits=5, decimal_places=2, default=10.00, help_text="Minimum down payment percentage (e.g. 10.00 for 10%)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    
    # Specs
    seats = models.PositiveIntegerField(default=4)
    transmission = models.CharField(max_length=50, default='Automatic')
    luggage = models.CharField(max_length=50, default='2 bags')
    fuel_type = models.CharField(max_length=50, default='Petrol')
    engine_type = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. V6, Electric, Hybrid")
    exterior_color = models.CharField(max_length=50, blank=True, null=True)
    interior_color = models.CharField(max_length=50, blank=True, null=True)
    drivetrain = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. AWD, RWD, FWD, 4x4")
    
    description = models.TextField()
    main_image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    
    features = models.ManyToManyField(VehicleFeature, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_featured = models.BooleanField(default=False, help_text="Show in homepage slider")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.make} {self.model} {self.year}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('car_details', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='vehicles/gallery/')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.vehicle.name}"

class Review(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.PositiveIntegerField(default=5)
    reviewer_name = models.CharField(max_length=255)
    reviewer_image = models.ImageField(upload_to='reviews/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer_name}"

class PageVisit(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='page_visits')
    session_key = models.CharField(max_length=255)
    last_seen = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('vehicle', 'session_key')

class GalleryImage(models.Model):
    image = models.ImageField(upload_to='gallery/')
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.caption or f"Gallery Image {self.id}"

# Applications & Jobs
class Job(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='job_applications')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    resume = models.FileField(upload_to='resumes/', storage=RAW_STORAGE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"App from {self.full_name} for {self.job.title}"

class FinancingApplication(models.Model):
    STATUS_CHOICES = [
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='financing_applications')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True, related_name='financing_applications')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    country = models.CharField(max_length=100)
    address = models.TextField()
    
    government_id_file = models.FileField(upload_to='financing/ids/', storage=RAW_STORAGE)
    drivers_license_file = models.FileField(upload_to='financing/licenses/', storage=RAW_STORAGE)
    proof_of_income_file = models.FileField(upload_to='financing/income/', storage=RAW_STORAGE)
    
    employment_details = models.TextField()
    business_details = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='submitted')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Financing App from {self.full_name}"

class InstallmentPlan(models.Model):
    TIER_CHOICES = [
        ('tier1', 'Tier 1 (Drive Now - >= 60% Down)'),
        ('tier2', 'Tier 2 (Layaway - < 60% Down)'),
    ]
    application = models.OneToOneField(FinancingApplication, on_delete=models.CASCADE, related_name='installment_plan')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='installment_plans')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='installment_plans')
    
    tier = models.CharField(max_length=10, choices=TIER_CHOICES, default='tier2')
    
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    down_payment_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    principal_balance = models.DecimalField(max_digits=12, decimal_places=2) # amount remaining
    
    # Penalty tracking for Tier 1
    accumulated_penalty_interest = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    monthly_due_date = models.IntegerField(help_text="Day of the month payment is due", null=True, blank=True)
    
    is_vehicle_released = models.BooleanField(default=False)
    is_fully_paid = models.BooleanField(default=False)
    
    # Delivery & Handover Tracking
    delivery_date = models.DateTimeField(null=True, blank=True)
    delivery_address = models.TextField(null=True, blank=True)
    delivery_phone = models.CharField(max_length=50, null=True, blank=True)
    delivery_status = models.CharField(
        max_length=50, 
        choices=[
            ('pending', 'Pending Scheduling'),
            ('scheduled', 'Scheduled for Delivery'),
            ('out_for_delivery', 'Out for Delivery'),
            ('delivered', 'Delivered & Handed Over')
        ],
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_balance_due(self):
        return self.principal_balance + self.accumulated_penalty_interest

    def __str__(self):
        return f"Plan for {self.user.username} - {self.vehicle.name}"

class PaymentTransaction(models.Model):
    PAYMENT_TYPES = [
        ('down_payment', 'Down Payment'),
        ('installment', 'Installment Payment'),
        ('penalty', 'Penalty Payment'),
        ('rental', 'Rental Payment'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    installment_plan = models.ForeignKey(InstallmentPlan, on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    rental_request = models.ForeignKey('RentalRequest', on_delete=models.CASCADE, null=True, blank=True, related_name='payments')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # To be populated by Stripe/Crypto in Phase 3
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Stripe, Crypto Wallet, Bank Transfer")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} - {self.payment_type} by {self.user.username}"

class TradeInRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Valuation'),
        ('offer_made', 'Offer Made'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    CONDITION_CHOICES = [
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('poor', 'Poor'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='trade_in_requests')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField()
    vin = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, default='good')
    interested_in = models.CharField(max_length=255, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    pickup_address = models.TextField(blank=True, null=True, help_text="Where the vehicle will be picked up")
    photos = models.FileField(upload_to='trade_in_photos/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    offer_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model} from {self.full_name}"

class RentalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending_payment', 'Pending Payment'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='rental_requests')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='rental_requests')
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    delivery_address = models.TextField(blank=True, null=True, help_text="Where the vehicle will be delivered")
    
    start_date = models.DateField()
    end_date = models.DateField()
    
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_payment')
    submitted_at = models.DateTimeField(auto_now_add=True)

    @property
    def amount_remaining(self):
        return self.total_cost - self.amount_paid

    @property
    def duration_days(self):
        return (self.end_date - self.start_date).days

    def __str__(self):
        return f"Rental: {self.vehicle.name} by {self.full_name}"

import random
import string

def generate_tracking_id():
    chars = string.ascii_uppercase + string.digits
    return 'RYDER-' + ''.join(random.choices(chars, k=6))

class Shipment(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('carrier_assigned', 'Carrier Assigned'),
        ('in_transit', 'In Transit'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
    ]
    
    tracking_id = models.CharField(max_length=20, unique=True, default=generate_tracking_id, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='shipments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, related_name='shipments')
    
    customer_name = models.CharField(max_length=255)
    origin_address = models.CharField(max_length=255, default="2333 Ponce de Leon Blvd., Suite 700, Coral Gables, FL 33134, USA")
    delivery_address = models.TextField()
    
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='processing')
    tracking_provider = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. UPS, FedEx, Shippo, AfterShip")
    tracking_started_at = models.DateTimeField(null=True, blank=True)
    estimated_delivery_date = models.DateField(null=True, blank=True)
    current_location = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Dallas, TX")
    notes = models.TextField(blank=True, null=True, help_text="Public notes for the customer tracking this shipment.")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Shipment {self.tracking_id} - {self.customer_name}"


# ==========================================================================
# Ryder Invest — fractional vehicle investment platform
# ==========================================================================
from dateutil.relativedelta import relativedelta


class InvestmentAsset(models.Model):
    """A single logistics vehicle that users can buy a stake in."""
    ASSET_TYPES = [
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('bike', 'Bike'),
        ('car', 'Car'),
        ('tractor', 'Tractor'),
        ('bus', 'Bus'),
    ]
    name = models.CharField(max_length=255, help_text="e.g. 'Mack Anthem Long-Haul #1'")
    slug = models.SlugField(unique=True, blank=True)
    asset_type = models.CharField(max_length=10, choices=ASSET_TYPES, default='truck')
    image = models.ImageField(upload_to='invest/assets/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    total_value = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total value of the vehicle, e.g. 120000.00")
    amount_funded = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total amount invested by users so far")
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, default=2000, help_text="Minimum amount a user can invest (starts at $2,000)")
    daily_return_percent = models.DecimalField(max_digits=6, decimal_places=3, default=0.021, help_text="Daily earnings as a percent of the invested amount, e.g. 0.021 for ~8% APY")

    is_active = models.BooleanField(default=True, help_text="Show on the invest marketplace and accept new investments")
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f"{self.name}")
            slug = base
            i = 2
            while InvestmentAsset.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def funded_percent(self):
        if not self.total_value:
            return 0
        return min(100, round((self.amount_funded / self.total_value) * 100, 1))

    @property
    def amount_remaining(self):
        return max(Decimal('0.00'), self.total_value - self.amount_funded)

    @property
    def is_sold_out(self):
        return self.amount_funded >= self.total_value

    @property
    def monthly_return_percent(self):
        return round(self.daily_return_percent * 30, 2)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('invest_asset_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return f"{self.name} ({self.get_asset_type_display()})"


class Investment(models.Model):
    """A user's stake in a single InvestmentAsset."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('matured', 'Matured'),
        ('withdrawn', 'Withdrawn'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investments')
    asset = models.ForeignKey(InvestmentAsset, on_delete=models.PROTECT, related_name='investments')

    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Principal invested")
    contract_months = models.PositiveIntegerField(default=1, help_text="Contract length chosen by the investor, in months")
    daily_return_percent = models.DecimalField(max_digits=6, decimal_places=3, help_text="Snapshot of the asset's daily rate at time of investing")

    start_date = models.DateField(default=timezone.localdate)
    end_date = models.DateField(null=True, blank=True)
    last_accrued_on = models.DateField(default=timezone.localdate)
    accrued_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = self.start_date + relativedelta(months=self.contract_months)
        super().save(*args, **kwargs)

    @property
    def daily_earning(self):
        return (self.amount * self.daily_return_percent) / Decimal('100')

    @property
    def effective_accrual_date(self):
        """We never accrue past the contract end date."""
        today = timezone.localdate()
        return min(today, self.end_date) if self.end_date else today

    def accrue(self, save=True):
        """Lazily credit daily earnings for each elapsed day since last accrual.
        Safe to call on every dashboard load — it is idempotent per day."""
        target = self.effective_accrual_date
        if self.status != 'active' or target <= self.last_accrued_on:
            return Decimal('0.00')
        days = (target - self.last_accrued_on).days
        gained = self.daily_earning * days
        self.accrued_earnings += gained
        self.last_accrued_on = target
        if self.end_date and timezone.localdate() >= self.end_date:
            self.status = 'matured'
        if save:
            self.save(update_fields=['accrued_earnings', 'last_accrued_on', 'status'])
        return gained

    @property
    def current_value(self):
        return self.amount + self.accrued_earnings

    @property
    def is_matured(self):
        return self.end_date and timezone.localdate() >= self.end_date

    def __str__(self):
        return f"{self.user.username} → {self.asset.name} (${self.amount})"


class InvestorWallet(models.Model):
    """Per-user balance of deposited and earned (withdrawable) funds."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='investor_wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Funds available to invest or withdraw")
    total_deposited = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_withdrawn = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_earned = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    accumulated_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Cumulative withdrawal fee the investor must pay to release withdrawals. Carries over and stacks each unpaid window.")
    total_fees_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def for_user(cls, user):
        wallet, _ = cls.objects.get_or_create(user=user)
        return wallet

    def __str__(self):
        return f"Wallet({self.user.username}): ${self.balance}"


class InvestmentTransaction(models.Model):
    """Ledger entry powering the dashboard's deposits/withdrawals/earnings view."""
    TYPES = [
        ('deposit', 'Deposit'),
        ('investment', 'Investment'),
        ('earning', 'Earning'),
        ('withdrawal', 'Withdrawal'),
        ('fee', 'Withdrawal Fee'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='investment_transactions')
    investment = models.ForeignKey(Investment, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    tx_type = models.CharField(max_length=20, choices=TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    reference = models.CharField(max_length=255, blank=True, null=True)
    note = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_tx_type_display()} ${self.amount} — {self.user.username}"


class WithdrawalWindow(models.Model):
    """Admin-controlled period during which withdrawals are allowed."""
    FEE_TYPES = [
        ('percent', 'Percentage of withdrawal'),
        ('flat', 'Flat amount'),
    ]
    label = models.CharField(max_length=100, help_text="e.g. 'June 2026 Window'")
    opens_at = models.DateTimeField(help_text="When the window opens")
    closes_at = models.DateTimeField(help_text="When the window closes (e.g. 2 days later)")
    fee_type = models.CharField(max_length=10, choices=FEE_TYPES, default='percent', help_text="Charge the fee as a percentage of the withdrawal, or a flat amount")
    fee_percent = models.DecimalField(max_digits=6, decimal_places=2, default=5, help_text="Used when fee type is 'Percentage' — e.g. 5 for 5%")
    fee_flat_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Used when fee type is 'Flat amount' — e.g. 2500.00")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-opens_at']

    @classmethod
    def current(cls):
        """Return the currently-open window, if any."""
        now = timezone.now()
        return cls.objects.filter(is_active=True, opens_at__lte=now, closes_at__gte=now).first()

    @property
    def is_open(self):
        return self.is_active and self.opens_at <= timezone.now() <= self.closes_at

    def compute_fee(self, amount):
        """The fee to release a withdrawal of `amount`."""
        if self.fee_type == 'flat':
            return self.fee_flat_amount
        return (Decimal(amount) * self.fee_percent) / Decimal('100')

    @property
    def fee_display(self):
        if self.fee_type == 'flat':
            return f"${self.fee_flat_amount} flat"
        return f"{self.fee_percent}%"

    def __str__(self):
        return f"{self.label} ({self.opens_at:%b %d} – {self.closes_at:%b %d})"


class WithdrawalRequest(models.Model):
    STATUS_CHOICES = [
        ('pending_fee', 'Awaiting Fee Payment'),
        ('approved', 'Fee Paid — Awaiting Payout'),
        ('paid', 'Paid'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdrawal_requests')
    window = models.ForeignKey(WithdrawalWindow, on_delete=models.SET_NULL, null=True, blank=True, related_name='requests')
    amount = models.DecimalField(max_digits=12, decimal_places=2, help_text="Amount the investor will receive once the fee is paid")
    fee = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Fee the investor must PAY to release this withdrawal")
    fee_paid = models.BooleanField(default=False)
    payout_method = models.CharField(max_length=100, blank=True, null=True, help_text="Bank / crypto / PayPal details")
    payout_details = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_fee')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def net_payout(self):
        # The fee is paid separately by the investor, so the full amount is paid out.
        return self.amount

    def __str__(self):
        return f"Withdrawal ${self.amount} — {self.user.username} ({self.status})"


# ==========================================================================
# Ryder AI Assistant — chatbot config + conversations
# ==========================================================================
class ChatConfig(models.Model):
    """Admin-managed config for the AI assistant. The client pastes their
    DeepSeek API key here (no redeploy needed)."""
    name = models.CharField(max_length=100, default="Ryder Assistant")
    provider = models.CharField(max_length=50, default="deepseek")
    api_key = models.CharField(max_length=255, blank=True, help_text="DeepSeek API key (the client buys this)")
    base_url = models.CharField(max_length=255, default="https://api.deepseek.com", help_text="OpenAI-compatible base URL")
    model_name = models.CharField(max_length=100, default="deepseek-chat", help_text="e.g. deepseek-chat")
    extra_instructions = models.TextField(blank=True, help_text="Optional extra persona/policy instructions appended to the system prompt")
    is_enabled = models.BooleanField(default=True)
    human_handoff_enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "AI Assistant Config"
        verbose_name_plural = "AI Assistant Config"

    @classmethod
    def get_active(cls):
        return cls.objects.filter(is_enabled=True).first()

    def __str__(self):
        return f"{self.name} ({self.model_name})"


class ChatConversation(models.Model):
    STATUS_CHOICES = [
        ('ai_active', 'AI Active'),
        ('human_requested', 'Human Requested'),
        ('human_active', 'Human Active'),
        ('closed', 'Closed'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='chat_conversations')
    session_key = models.CharField(max_length=120, db_index=True, help_text="Anonymous session identifier")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ai_active')
    assigned_agent = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_chats')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        who = self.user.username if self.user else f"guest:{self.session_key[:8]}"
        return f"Chat with {who} ({self.get_status_display()})"


class ChatMessage(models.Model):
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
        ('agent', 'Human Agent'),
        ('system', 'System'),
    ]
    conversation = models.ForeignKey(ChatConversation, on_delete=models.CASCADE, related_name='messages')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}"

class CryptoDeposit(models.Model):
    STATUS_CHOICES = [
        # Deposit intent created; we've shown the user the exact tagged amount to
        # send but no transaction hash has been submitted/verified yet.
        ('awaiting_payment', 'Awaiting Payment'),
        ('pending', 'Pending Verification'),
        ('verified', 'Verified & Credited'),
        ('failed', 'Verification Failed'),
    ]
    CRYPTO_CHOICES = [
        ('BTC', 'Bitcoin (BTC)'),
        ('ETH', 'Ethereum (ETH)'),
        ('USDT', 'Tether (USDT TRC20)'),
    ]
    # What this crypto payment is FOR: funding the wallet, or paying the
    # cumulative withdrawal-release fee. Decides what happens on verification.
    PURPOSE_CHOICES = [
        ('deposit', 'Wallet Funding'),
        ('fee', 'Withdrawal Release Fee'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crypto_deposits')
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES, default='deposit')
    crypto_currency = models.CharField(max_length=10, choices=CRYPTO_CHOICES)
    amount_usd = models.DecimalField(max_digits=12, decimal_places=2)
    # The EXACT, uniquely-tagged crypto amount the user must send. Uniqueness of
    # this value among outstanding deposits is what ties an on-chain payment to a
    # specific user's deposit intent (prevents claiming someone else's payment).
    crypto_amount = models.DecimalField(max_digits=18, decimal_places=8)
    # Null until the user submits a hash — a deposit is created at "generate
    # payment" time, before any transaction exists. unique=True still holds:
    # Postgres allows multiple NULLs, so many awaiting_payment rows coexist.
    tx_hash = models.CharField(max_length=255, unique=True, null=True, blank=True,
                               help_text="Blockchain Transaction ID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.crypto_currency} Deposit - {self.user.username} - ${self.amount_usd}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True, help_text="ISO 3166-1 alpha-2 country code")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    network = models.CharField(max_length=100, null=True, blank=True)
    browser = models.CharField(max_length=100, null=True, blank=True)
    connection_type = models.CharField(max_length=50, null=True, blank=True)
    is_active_online = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Profile: {self.user.username}"


# ==========================================================
# Push Notification Models
# ==========================================================

class AdminDevice(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_devices')
    push_token = models.CharField(max_length=255, unique=True, help_text="Expo Push Token for iOS/Android")
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Device for {self.user.username} ({self.push_token[:10]}...)"


