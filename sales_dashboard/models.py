"""
Models for Sales Dashboard app
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PaymentRecord(models.Model):
    """Model for storing payment records"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('success', 'Успешно'),
        ('failed', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]
    
    order_id = models.CharField('ID заказа', max_length=100, unique=True)
    amount = models.IntegerField('Сумма (в суммах)')
    currency = models.CharField('Валюта', max_length=10, default='UZS')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment details
    payment_id = models.CharField('ID платежа', max_length=100, blank=True)
    description = models.CharField('Описание', max_length=500, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    paid_at = models.DateTimeField('Оплачен', null=True, blank=True)
    
    # User info (if available)
    user_id = models.CharField('ID пользователя', max_length=100, blank=True)
    user_info = models.JSONField('Информация о пользователе', default=dict, blank=True)
    
    # Subscription info
    subscription_duration = models.IntegerField('Длительность подписки (мин)', default=15)
    
    class Meta:
        verbose_name = 'Запись о платеже'
        verbose_name_plural = 'Записи о платежах'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ {self.order_id} - {self.amount} {self.currency} ({self.get_status_display()})"
    
    @property
    def amount_in_tiyin(self):
        """Convert amount to tiyin (1 sum = 100 tiyin)"""
        return self.amount * 100
    
    def mark_as_paid(self):
        """Mark payment as successful"""
        self.status = 'success'
        self.paid_at = timezone.now()
        self.save()


class DailyStats(models.Model):
    """Daily statistics summary"""
    
    date = models.DateField('Дата', unique=True)
    
    # Payment stats
    total_payments = models.IntegerField('Всего платежей', default=0)
    successful_payments = models.IntegerField('Успешных платежей', default=0)
    failed_payments = models.IntegerField('Неуспешных платежей', default=0)
    pending_payments = models.IntegerField('Ожидающих платежей', default=0)
    
    # Revenue stats
    total_revenue = models.IntegerField('Общий доход (сумм)', default=0)
    
    # Subscription stats
    total_subscriptions = models.IntegerField('Всего подписок', default=0)
    active_subscriptions = models.IntegerField('Активных подписок', default=0)
    
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлено', auto_now=True)
    
    class Meta:
        verbose_name = 'Дневная статистика'
        verbose_name_plural = 'Дневная статистика'
        ordering = ['-date']
    
    def __str__(self):
        return f"Статистика за {self.date}: {self.successful_payments} платежей, {self.total_revenue} сум"
