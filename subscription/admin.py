"""
Admin interface for subscription settings
"""

from django.contrib import admin
from .models import SubscriptionSettings


@admin.register(SubscriptionSettings)
class SubscriptionSettingsAdmin(admin.ModelAdmin):
    """Admin interface for subscription settings"""
    
    list_display = ['price', 'currency', 'duration_minutes', 'is_active', 'updated_at', 'updated_by']
    list_filter = ['is_active', 'currency', 'updated_at']
    search_fields = ['currency', 'updated_by']
    
    fieldsets = (
        ('Основные настройки', {
            'fields': ('price', 'currency', 'duration_minutes', 'is_active')
        }),
        ('Информация', {
            'fields': ('updated_by',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['updated_at']
    
    def save_model(self, request, obj, form, change):
        obj.updated_by = request.user.username
        super().save_model(request, obj, form, change)
    
    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of settings
        return False
    
    def has_add_permission(self, request):
        # Only allow one instance
        if SubscriptionSettings.objects.exists():
            return False
        return True
