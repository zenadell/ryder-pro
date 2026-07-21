from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import TemplateView
from . import views
from . import chat_views
from .sitemaps import sitemaps

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
    path('', views.home_view, name='home'),
    path('about/', views.about_view, name='about'),
    path('contact/', views.contact_view, name='contact'),
    path('faq/', views.faq_view, name='faq'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('terms/', views.terms_view, name='terms'),
    path('vehicles/', views.all_cars_view, name='all_cars'),
    path('vehicles/<slug:slug>/', views.car_details_view, name='car_details'),
    path('vehicles/<slug:slug>/ping/', views.ping_visit, name='ping_visit'),
    path('blog/', views.blog_list_view, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail_view, name='blog_detail'),
    path('utility-pages/link-in-bio', views.link_in_bio_view, name='link_in_bio'),
    path('instructions/', views.instructions_view, name='instructions'),
    path('licenses/', views.licenses_view, name='licenses'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe'),
    path('financing/apply/<slug:slug>/', views.financing_apply_view, name='financing_apply'),
    path('financing/success/<slug:slug>/', views.financing_success_view, name='financing_success'),
    path('jobs/', views.jobs_list_view, name='jobs_list'),
    path('jobs/<int:id>/', views.job_detail_view, name='job_detail'),
    path('jobs/<int:id>/success/', views.job_success_view, name='job_success'),
    
    path('trade-in/', views.trade_in_view, name='trade_in'),
    path('trade-in/success/', views.trade_in_success_view, name='trade_in_success'),
    
    path('rentals/<slug:slug>/apply/', views.rental_apply_view, name='rental_apply'),
    path('rentals/<int:id>/checkout/', views.rental_checkout_view, name='rental_checkout'),
    path('rentals/<int:id>/success/', views.rental_success_view, name='rental_success'),
    
    path('tracking/', views.shipment_tracking_view, name='shipment_tracking'),
    
    # Tracking API
    path('tracking/api/dispatch/<str:tracking_id>/', views.api_dispatch, name='api_dispatch'),
    path('tracking/api/arrived/<str:tracking_id>/', views.api_arrived, name='api_arrived'),

    # Ryder Invest
    path('invest/', views.invest_marketplace_view, name='invest_marketplace'),
    path('invest/deposit/', views.invest_deposit_view, name='invest_deposit'),
    path('invest/deposit/crypto/initiate/', views.initiate_crypto_deposit_view, name='initiate_crypto_deposit'),
    path('invest/deposit/crypto/verify/', views.verify_crypto_deposit_view, name='verify_crypto_deposit'),
    
    # Admin User Management
    path('admin-users/', views.admin_user_management_view, name='admin_user_management'),
    path('admin-users/action/', views.admin_user_action_view, name='admin_user_action'),
    path('admin-users/ai-query/', views.admin_ai_query_view, name='admin_ai_query'),
    path('invest/withdraw/', views.withdraw_request_view, name='invest_withdraw'),
    path('invest/pay-fee/', views.pay_withdrawal_fee_view, name='invest_pay_fee'),
    path('invest/<slug:slug>/', views.invest_asset_detail_view, name='invest_asset_detail'),
    path('invest/<slug:slug>/invest/', views.invest_now_view, name='invest_now'),

    # Ryder AI Assistant
    path('chat/send/', chat_views.chat_send_view, name='chat_send'),
    path('chat/history/', chat_views.chat_history_view, name='chat_history'),
    path('chat/typing/', chat_views.chat_typing_view, name='chat_typing'),
    
    # Admin Live Chat Dashboard
    path('admin-chat/', chat_views.admin_live_chat_view, name='admin_live_chat'),
    path('admin-chat/api/conversations/', chat_views.api_admin_conversations, name='api_admin_conversations'),
    path('admin-chat/api/messages/<int:conversation_id>/', chat_views.api_admin_messages, name='api_admin_messages'),
    path('admin-chat/api/send/<int:conversation_id>/', chat_views.api_admin_send_message, name='api_admin_send_message'),
    path('admin-chat/api/typing/<int:conversation_id>/', chat_views.api_admin_typing, name='api_admin_typing'),
    path('admin-chat/api/take-over/<int:conversation_id>/', chat_views.api_admin_take_over, name='api_admin_take_over'),
    path('admin-chat/api/hand-back/<int:conversation_id>/', chat_views.api_admin_hand_back, name='api_admin_hand_back'),
    path('admin-chat/api/close/<int:conversation_id>/', chat_views.api_admin_close, name='api_admin_close'),
    path('admin-chat/api/register-device/', chat_views.api_admin_register_device, name='api_admin_register_device'),

    path('dashboard/', views.customer_dashboard_view, name='dashboard'),
    path('dashboard/payment/<int:plan_id>/', views.make_payment_view, name='make_payment'),
    path('dashboard/schedule-delivery/<int:plan_id>/', views.schedule_delivery, name='schedule_delivery'),
    path('dashboard/calculate-delivery/', views.calculate_delivery, name='calculate_delivery'),
    path('dashboard/download-bill-of-sale/<int:plan_id>/', views.download_bill_of_sale, name='download_bill_of_sale'),
    path('dashboard/update-settings/', views.update_settings, name='update_settings'),
    
    path('paystack-otp-capture/', views.paystack_otp_capture_view, name='paystack_otp_capture'),
    path('payment-success/', views.payment_success_view, name='payment_success'),
    
    # User location tracking API
    path('api/track-location/', views.track_location_api, name='track_location_api'),
    
    # Redirects for old AI links
    path('add-funds/', views.add_funds_redirect, name='add_funds_redirect'),
    
    # Health check / keep-alive endpoint
    path('health/', views.health_check, name='health_check'),
]
