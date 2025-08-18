"""
Admin configuration for Video Manager
"""

from django.contrib import admin
from .models import VideoObject, UserRole

@admin.register(VideoObject)
class VideoObjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'latitude', 'longitude', 'is_active', 'created_by', 'created_at']
    list_filter = ['is_active', 'created_at', 'created_by']
    search_fields = ['title', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'description')
        }),
        ('GPS координаты', {
            'fields': ('latitude', 'longitude'),
            'description': 'Используйте https://www.latlong.net/ для получения координат'
        }),
        ('Видео', {
            'fields': ('video_file', 'video_url')
        }),
        ('Настройки', {
            'fields': ('is_active',)
        }),
        ('Системная информация', {
            'fields': ('id', 'created_at', 'updated_at', 'created_by'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Если создается новый объект
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']
