from django.contrib import admin
from .models import (
    SiteContent, NewsletterSubscriber, ContactMessage, TeamMember, BlogPost,
    Category, VehicleFeature, Vehicle, VehicleImage, Review,
    Job, JobApplication, FinancingApplication, GalleryImage, TradeInRequest, RentalRequest, Shipment,
    GeminiAPIKey, BulkImport, InstallmentPlan, PaymentTransaction
)
from django.urls import path
from django.template.response import TemplateResponse
from .utils import process_bulk_import
from django.contrib import messages

@admin.register(BulkImport)
class BulkImportAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', self.admin_site.admin_view(self.bulk_import_view), name='core_bulkimport_changelist'),
        ]
        return custom_urls + urls

    def bulk_import_view(self, request):
        if request.method == 'POST':
            car_list_text = request.POST.get('car_list', '')
            if car_list_text:
                results = process_bulk_import(car_list_text)
                return TemplateResponse(request, 'admin/bulk_import.html', {'results': results, 'car_list_text': car_list_text, 'title': 'AI Bulk Importer'})
            else:
                messages.error(request, "Please enter at least one car.")
        return TemplateResponse(request, 'admin/bulk_import.html', {'title': 'AI Bulk Importer'})

@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    list_display = ('key', 'updated_at')
    search_fields = ('key', 'value')

@admin.register(GeminiAPIKey)
class GeminiAPIKeyAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('key',)

@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'submitted_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('name', 'email', 'phone', 'message', 'submitted_at')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    search_fields = ('name', 'role')
    list_editable = ('order',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_at', 'is_published')
    search_fields = ('title', 'content')
    list_filter = ('is_published', 'published_at')
    prepopulated_fields = {'slug': ('title',)}

# Vehicle Marketplace
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(VehicleFeature)
class VehicleFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class VehicleImageInline(admin.TabularInline):
    model = VehicleImage
    extra = 1

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'category', 'price_per_day', 'status', 'is_featured')
    list_filter = ('status', 'financing_eligible', 'is_featured', 'category')
    search_fields = ('make', 'model', 'year')
    prepopulated_fields = {'slug': ('make', 'model', 'year')}
    inlines = [VehicleImageInline]
    filter_horizontal = ('features',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'vehicle', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('reviewer_name', 'title', 'content')

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('caption', 'order')
    list_editable = ('order',)

# Applications & Jobs
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description', 'location')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'job', 'email', 'status', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('full_name', 'email')
    readonly_fields = ('job', 'full_name', 'email', 'phone', 'resume', 'submitted_at')

@admin.register(FinancingApplication)
class FinancingApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vehicle', 'email', 'status', 'address', 'submitted_at')
    list_filter = ('status', 'submitted_at')
    search_fields = ('full_name', 'email')
    readonly_fields = (
        'vehicle', 'full_name', 'email', 'phone', 'country', 'address',
        'government_id_file', 'drivers_license_file', 'proof_of_income_file',
        'employment_details', 'business_details', 'submitted_at'
    )

@admin.register(TradeInRequest)
class TradeInRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'year', 'make', 'model', 'status', 'pickup_address', 'offer_amount', 'submitted_at')
    list_filter = ('status', 'condition', 'submitted_at')
    search_fields = ('full_name', 'email', 'make', 'model', 'vin')

@admin.register(RentalRequest)
class RentalRequestAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vehicle', 'start_date', 'end_date', 'status', 'delivery_address', 'total_cost', 'amount_paid', 'submitted_at')
    list_filter = ('status', 'start_date')
    search_fields = ('full_name', 'email', 'vehicle__name')

@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ('tracking_id', 'customer_name', 'vehicle', 'status', 'tracking_provider', 'estimated_delivery_date', 'current_location', 'updated_at')
    list_filter = ('status', 'estimated_delivery_date')
    search_fields = ('tracking_id', 'customer_name', 'vehicle__name', 'delivery_address')
    readonly_fields = ('tracking_id', 'created_at', 'updated_at')

@admin.register(InstallmentPlan)
class InstallmentPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'vehicle', 'tier', 'principal_balance', 'accumulated_penalty_interest', 'is_vehicle_released', 'is_fully_paid')
    list_filter = ('tier', 'is_vehicle_released', 'is_fully_paid')
    search_fields = ('user__username', 'vehicle__name')

@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'payment_type', 'status', 'created_at')
    list_filter = ('payment_type', 'status', 'created_at')
    search_fields = ('user__username', 'transaction_id')
