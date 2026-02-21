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
]
