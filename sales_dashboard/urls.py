"""
URLs for Sales Dashboard app
"""

from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('payments/', views.payment_list, name='payments'),
    path('statistics/', views.statistics, name='statistics'),
    path('sync-payments/', views.sync_payments, name='sync_payments'),
]
