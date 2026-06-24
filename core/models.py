from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Global & Static Content
class SiteContent(models.Model):
    key = models.SlugField(unique=True, help_text="e.g. 'home_hero_title'")
    value = models.TextField(help_text="The text or HTML content", blank=True, null=True)
    image = models.ImageField(upload_to='site_images/', blank=True, null=True, help_text="Use this for image content")
    video = models.FileField(upload_to='site_videos/', blank=True, null=True, help_text="Use this for video content (mp4/webm)")
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

import os
from django.core.files.storage import FileSystemStorage

if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    from cloudinary_storage.storage import RawMediaCloudinaryStorage
    RAW_STORAGE = RawMediaCloudinaryStorage()
else:
    RAW_STORAGE = FileSystemStorage()

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
