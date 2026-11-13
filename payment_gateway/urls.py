from django.urls import path
from django.shortcuts import redirect
from . import views

app_name = 'payment_gateway'

urlpatterns = [
    path('', lambda r: redirect('/admin/')),
    # Unity API endpoints
    path('api/unity/create-payment/', views.unity_create_payment, name='unity_create_payment'),
    path('api/unity/check-status/', views.unity_check_payment_status, name='unity_check_status'),
    path('api/unity/health/', views.unity_health_check, name='unity_health_check'),
    path('api/unity/server-info/', views.unity_server_info, name='unity_server_info'),
    # FreedomPay callbacks
    path('freedompay/check/', views.freedompay_check, name='freedompay_check'),
    path('freedompay/result/', views.freedompay_result, name='freedompay_result'),
    path('freedompay/success/', views.freedompay_success, name='freedompay_success'),
    path('freedompay/fail/', views.freedompay_fail, name='freedompay_fail'),
    # Milliy Ecom callbacks
    path('milliy/callback/', views.milliy_callback, name='milliy_callback'),
    path('milliy/success/', views.milliy_success, name='milliy_success'),
    path('milliy/fail/', views.milliy_fail, name='milliy_fail'),
    # CyberSource Unified Checkout (Visa/Mastercard)
    path('cybersource/checkout/', views.cybersource_checkout, name='cybersource_checkout'),
    path('cybersource/complete/', views.cybersource_complete, name='cybersource_complete'),
    path('cybersource/success/', views.cybersource_success, name='cybersource_success'),
    path('cybersource/fail/', views.cybersource_fail, name='cybersource_fail'),
]
