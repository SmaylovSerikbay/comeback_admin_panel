from django.urls import path
from . import views

app_name = 'otp_manager'

urlpatterns = [
    path('', views.otp_list, name='otp_list'),
    path('create/', views.create_otp, name='create_otp'),
    path('cash-payment/', views.cash_payment, name='cash_payment'),
    path('<uuid:otp_id>/', views.otp_detail, name='otp_detail'),
    path('<uuid:otp_id>/print/', views.print_receipt, name='print_receipt'),
    path('api/verify/', views.verify_otp_api, name='verify_otp_api'),
]
