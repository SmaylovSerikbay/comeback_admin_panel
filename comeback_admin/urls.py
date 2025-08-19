"""
URL configuration for comeback_admin project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.views.generic import TemplateView

def redirect_to_dashboard(request):
    """Redirect root URL to dashboard"""
    return redirect('dashboard:home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', include('sales_dashboard.urls', namespace='dashboard')),
    path('videos/', include('video_manager.urls', namespace='videos')),
    path('subscription/', include('subscription.urls', namespace='subscription')),
    path('otp/', include('otp_manager.urls', namespace='otp_manager')),
    # Legal pages
    path('privacy/', TemplateView.as_view(template_name='legal/privacy.html'), name='privacy'),
    path('terms/', TemplateView.as_view(template_name='legal/terms.html'), name='terms'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
