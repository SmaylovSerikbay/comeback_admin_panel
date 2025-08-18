"""
URLs for subscription management
"""

from django.urls import path
from . import views

app_name = 'subscription'

urlpatterns = [
    path('settings/', views.subscription_settings, name='settings'),
    path('sync-firebase/', views.sync_firebase, name='sync_firebase'),
    path('api/settings/', views.api_subscription_settings, name='api_settings'),
]
