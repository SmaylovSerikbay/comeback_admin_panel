from django.contrib import admin
from .models import PaymentTransaction, PaymentCallback, UnityPaymentSession


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'order_id', 'amount', 'currency', 'status', 'unity_user_id',
        'created_at', 'paid_at'
    ]
    list_filter = ['status', 'currency', 'created_at', 'paid_at']
    search_fields = ['order_id', 'unity_user_id', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('order_id', 'amount', 'currency', 'status', 'description')
        }),
        ('Unity данные', {
            'fields': ('unity_user_id', 'unity_session_id'),
            'classes': ('collapse',)
        }),
        ('FreedomPay данные', {
            'fields': ('merchant_id', 'salt', 'signature', 'payment_id'),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at', 'updated_at', 'paid_at'),
            'classes': ('collapse',)
        }),
        ('Пользователь', {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PaymentCallback)
class PaymentCallbackAdmin(admin.ModelAdmin):
    list_display = [
        'transaction', 'callback_type', 'processed', 'created_at'
    ]
    list_filter = ['callback_type', 'processed', 'created_at']
    search_fields = ['transaction__order_id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('transaction', 'callback_type', 'processed')
        }),
        ('Данные', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
        ('Временные метки', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(UnityPaymentSession)
class UnityPaymentSessionAdmin(admin.ModelAdmin):
    list_display = [
        'session_id', 'unity_user_id', 'amount', 'is_active', 'created_at', 'expires_at'
    ]
    list_filter = ['is_active', 'created_at', 'expires_at']
    search_fields = ['session_id', 'unity_user_id']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('session_id', 'unity_user_id', 'amount', 'description', 'is_active')
        }),
        ('Временные метки', {
            'fields': ('created_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
