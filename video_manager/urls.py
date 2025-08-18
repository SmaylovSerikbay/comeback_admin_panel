"""
URLs for Video Manager app
"""

from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('', views.video_list, name='list'),
    path('create/', views.video_create, name='create'),
    path('<str:video_id>/edit/', views.video_edit, name='edit'),
    path('<str:video_id>/delete/', views.video_delete, name='delete'),
    path('instructions/', views.instructions, name='instructions'),
    path('clean-firebase/', views.clean_firebase_data, name='clean_firebase'),
]
