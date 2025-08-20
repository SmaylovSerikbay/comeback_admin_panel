from django.urls import path
from . import views

app_name = 'payment_gateway'

urlpatterns = [
    # Unity API endpoints
    path('api/unity/create-payment/', views.unity_create_payment, name='unity_create_payment'),
    path('api/unity/check-status/', views.unity_check_payment_status, name='unity_check_status'),
    
    # FreedomPay callbacks
    path('freedompay/check/', views.freedompay_check, name='freedompay_check'),
    path('freedompay/result/', views.freedompay_result, name='freedompay_result'),
    path('freedompay/success/', views.freedompay_success, name='freedompay_success'),
    path('freedompay/fail/', views.freedompay_fail, name='freedompay_fail'),
    
    # Admin dashboard
    path('dashboard/', views.payment_dashboard, name='dashboard'),
    path('transaction/<str:order_id>/', views.transaction_detail, name='transaction_detail'),
    
    # Test and documentation
    path('test/', views.test_payment_form, name='test_form'),
    path('api-docs/', views.api_documentation, name='api_docs'),
]
