from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import OTPCode

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'amount', 'currency', 'quantity', 'status', 'created_by', 'created_at', 'used_at', 'actions']
    list_filter = ['status', 'currency', 'created_at', 'used_at', 'created_by']
    search_fields = ['code', 'created_by__username']
    readonly_fields = ['code', 'created_at', 'firebase_key']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('code', 'amount', 'currency', 'quantity')
        }),
        ('Статус', {
            'fields': ('status', 'created_at', 'used_at')
        }),
        ('Создатель', {
            'fields': ('created_by', 'device_id')
        }),
        ('Техническая информация', {
            'fields': ('firebase_key',),
            'classes': ('collapse',)
        }),
    )
    
    def get_actions_display(self, obj):
        """Действия для OTP кода"""
        actions_html = []
        
        # Кнопка деталей
        detail_url = reverse('otp_manager:otp_detail', args=[obj.id])
        actions_html.append(f'<a href="{detail_url}" class="btn btn-info btn-sm">👁️ Детали</a>')
        
        # Кнопка печати
        if obj.status == 'active':
            print_url = reverse('otp_manager:print_receipt', args=[obj.id])
            actions_html.append(f'<a href="{print_url}" class="btn btn-success btn-sm">🖨️ Печать</a>')
        
        # Кнопка Firebase
        if obj.firebase_key:
            firebase_url = f"https://console.firebase.google.com/project/comeback-2a6b2/database/comeback-2a6b2-default-rtdb/data/activation_codes/{obj.firebase_key}"
            actions_html.append(f'<a href="{firebase_url}" target="_blank" class="btn btn-warning btn-sm">🔥 Firebase</a>')
        
        return mark_safe(' '.join(actions_html))
    
    get_actions_display.short_description = 'Действия'
    
    def get_queryset(self, request):
        """Фильтруем коды по правам пользователя"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        else:
            # Кассир видит только свои коды
            return qs.filter(created_by=request.user)
    
    def has_add_permission(self, request):
        """Только кассиры могут создавать OTP коды"""
        if request.user.is_superuser:
            return True
        try:
            return hasattr(request.user, 'userrole') and request.user.userrole.role == 'cashier'
        except:
            return False
    
    def has_change_permission(self, request, obj=None):
        """Кассиры могут изменять только свои коды"""
        if request.user.is_superuser:
            return True
        if obj is None:
            return True
        return obj.created_by == request.user
    
    def has_delete_permission(self, request, obj=None):
        """Только админы могут удалять коды"""
        return request.user.is_superuser
