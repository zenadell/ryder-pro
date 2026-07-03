from django.contrib import admin
from django.utils.html import format_html
from .models import (
    SiteContent, NewsletterSubscriber, ContactMessage, TeamMember, BlogPost,
    Category, VehicleFeature, Vehicle, VehicleImage, Review,
    Job, JobApplication, FinancingApplication, GalleryImage, TradeInRequest, RentalRequest, Shipment,
    GeminiAPIKey, BulkImport, InstallmentPlan, PaymentTransaction,
    InvestmentAsset, Investment, InvestorWallet, InvestmentTransaction,
    WithdrawalWindow, WithdrawalRequest,
    ChatConfig, ChatConversation, ChatMessage,
    UserProfile,
)
from django.urls import path
from django.template.response import TemplateResponse
from .utils import process_bulk_import
from django.contrib import messages
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# ---- UserProfile inline on User admin ----
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Geolocation & Profile'
    readonly_fields = ('ip_address', 'city', 'country', 'country_code', 'latitude', 'longitude', 'last_login_at')
    fields = ('ip_address', 'city', 'country', 'country_code', 'latitude', 'longitude', 'last_login_at')

class CustomUserAdmin(BaseUserAdmin):
    inlines = list(BaseUserAdmin.inlines) + [UserProfileInline]
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'get_location')
    
    def get_location(self, obj):
        try:
            p = obj.profile
            if p.country:
                flag = ''
                if p.country_code:
                    flag = format_html('<img src="https://flagcdn.com/16x12/{}.png" style="vertical-align:middle;margin-right:4px;" />', p.country_code.lower())
                return format_html('{}{}, {}', flag, p.city or "", p.country)
        except UserProfile.DoesNotExist:
            pass
        return '—'
    get_location.short_description = 'Location'

# Unregister default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


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


# ---- Ryder Invest ----
@admin.register(InvestmentAsset)
class InvestmentAssetAdmin(admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'total_value', 'amount_funded', 'funded_percent', 'daily_return_percent', 'min_investment', 'is_active', 'is_featured')
    list_filter = ('asset_type', 'is_active', 'is_featured')
    list_editable = ('is_active', 'is_featured', 'daily_return_percent')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'asset', 'amount', 'contract_months', 'daily_return_percent', 'accrued_earnings', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'asset__asset_type', 'start_date')
    search_fields = ('user__username', 'asset__name')
    readonly_fields = ('accrued_earnings', 'last_accrued_on', 'created_at')


@admin.register(InvestorWallet)
class InvestorWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'accumulated_fee', 'total_deposited', 'total_withdrawn', 'total_earned', 'total_fees_paid', 'updated_at')
    search_fields = ('user__username',)


@admin.register(InvestmentTransaction)
class InvestmentTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'tx_type', 'amount', 'status', 'investment', 'created_at')
    list_filter = ('tx_type', 'status', 'created_at')
    search_fields = ('user__username', 'reference')


@admin.register(WithdrawalWindow)
class WithdrawalWindowAdmin(admin.ModelAdmin):
    list_display = ('label', 'opens_at', 'closes_at', 'fee_type', 'fee_percent', 'fee_flat_amount', 'is_active', 'is_open')
    list_filter = ('is_active', 'fee_type')
    list_editable = ('is_active', 'fee_type', 'fee_percent', 'fee_flat_amount')


@admin.register(WithdrawalRequest)
class WithdrawalRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'fee', 'fee_paid', 'net_payout', 'status', 'window', 'created_at', 'processed_at')
    list_filter = ('status', 'fee_paid', 'created_at')
    search_fields = ('user__username',)
    readonly_fields = ('created_at',)


# ---- Ryder AI Assistant ----
@admin.register(ChatConfig)
class ChatConfigAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'model_name', 'is_enabled', 'human_handoff_enabled')
    list_editable = ('is_enabled', 'human_handoff_enabled')


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 0
    readonly_fields = ('role', 'content', 'created_at')
    can_delete = False


@admin.register(ChatConversation)
class ChatConversationAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'status', 'assigned_agent', 'updated_at')
    list_filter = ('status', 'updated_at')
    search_fields = ('user__username', 'session_key')
    readonly_fields = ('user', 'session_key', 'created_at', 'updated_at')
    inlines = [ChatMessageInline]
