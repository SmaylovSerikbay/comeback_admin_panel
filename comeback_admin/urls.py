"""
URL configuration for comeback_admin project.
Верстка — только admin-next (Next.js). Django отдаёт API и админку.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('admin_api.urls')),
    path('payment-gateway/', include('payment_gateway.urls', namespace='payment_gateway')),
    path('', lambda r: redirect('/admin/'), name='home'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
