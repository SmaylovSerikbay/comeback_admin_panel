"""
Admin configuration for Sales Dashboard
"""

from django.contrib import admin
from .models import PaymentRecord, DailyStats

@admin.register(PaymentRecord)
class PaymentRecordAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'amount', 'currency', 'status', 'created_at', 'paid_at']
    list_filter = ['status', 'currency', 'created_at']
    search_fields = ['order_id', 'payment_id', 'user_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order_id', 'amount', 'currency', 'status', 'description')
        }),
        ('Платежная информация', {
            'fields': ('payment_id', 'paid_at')
        }),
        ('Пользователь', {
            'fields': ('user_id', 'user_info')
        }),
        ('Подписка', {
            'fields': ('subscription_duration',)
        }),
        ('Системная информация', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_payments', 'successful_payments', 'total_revenue']
    list_filter = ['date']
    readonly_fields = ['created_at', 'updated_at']
