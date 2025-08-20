"""
Models for Payment Gateway app
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class PaymentTransaction(models.Model):
    """Модель для хранения транзакций платежей"""
    
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('success', 'Успешно'),
        ('failed', 'Отклонено'),
        ('cancelled', 'Отменено'),
    ]
    
    # Основные данные платежа
    order_id = models.CharField('ID заказа', max_length=100, unique=True)
    amount = models.IntegerField('Сумма (в суммах)')
    currency = models.CharField('Валюта', max_length=10, default='UZS')
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Детали платежа
    payment_id = models.CharField('ID платежа', max_length=100, blank=True, null=True)
    description = models.CharField('Описание', max_length=500, blank=True)
    
    # Unity данные
    unity_user_id = models.CharField('ID пользователя Unity', max_length=100, blank=True)
    unity_session_id = models.CharField('ID сессии Unity', max_length=100, blank=True)
    
    # FreedomPay данные
    merchant_id = models.CharField('Merchant ID', max_length=50, default='552170')
    salt = models.CharField('Соль', max_length=100)
    signature = models.CharField('Подпись', max_length=100, blank=True)
    
    # Временные метки
    created_at = models.DateTimeField('Создан', auto_now_add=True)
    updated_at = models.DateTimeField('Обновлен', auto_now=True)
    paid_at = models.DateTimeField('Оплачен', null=True, blank=True)
    
    # Пользователь (если авторизован)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Пользователь')
    
    class Meta:
        verbose_name = 'Транзакция платежа'
        verbose_name_plural = 'Транзакции платежей'
        ordering = ['-created_at']
        db_table = 'payment_gateway_transactions'
    
    def __str__(self):
        return f"Заказ {self.order_id} - {self.amount} {self.currency} ({self.get_status_display()})"
    
    @property
    def amount_in_tiyin(self):
        """Конвертация суммы в тийны (1 сум = 100 тийнов)"""
        return self.amount * 100
    
    def mark_as_paid(self, payment_id=None):
        """Отметить платеж как успешный"""
        self.status = 'success'
        self.paid_at = timezone.now()
        if payment_id:
            self.payment_id = payment_id
        self.save()
    
    def mark_as_failed(self):
        """Отметить платеж как неуспешный"""
        self.status = 'failed'
        self.save()
    
    def generate_order_id(self):
        """Генерация уникального ID заказа"""
        if not self.order_id:
            self.order_id = f"order_{uuid.uuid4().hex[:16]}"
        return self.order_id


class PaymentCallback(models.Model):
    """Модель для хранения callback'ов от платежной системы"""
    
    transaction = models.ForeignKey(PaymentTransaction, on_delete=models.CASCADE, related_name='callbacks')
    callback_type = models.CharField('Тип callback', max_length=20)  # 'check', 'result', 'success', 'fail'
    raw_data = models.JSONField('Сырые данные', default=dict)
    processed = models.BooleanField('Обработан', default=False)
    created_at = models.DateTimeField('Получен', auto_now_add=True)
    
    class Meta:
        verbose_name = 'Callback платежа'
        verbose_name_plural = 'Callback\'ы платежей'
        ordering = ['-created_at']
        db_table = 'payment_gateway_callbacks'
    
    def __str__(self):
        return f"Callback {self.callback_type} для {self.transaction.order_id}"


class UnityPaymentSession(models.Model):
    """Модель для сессий платежей Unity"""
    
    session_id = models.CharField('ID сессии', max_length=100, unique=True)
    unity_user_id = models.CharField('ID пользователя Unity', max_length=100)
    amount = models.IntegerField('Сумма (в суммах)')
    description = models.CharField('Описание', max_length=500, blank=True)
    created_at = models.DateTimeField('Создана', auto_now_add=True)
    expires_at = models.DateTimeField('Истекает', null=True, blank=True)
    is_active = models.BooleanField('Активна', default=True)
    
    class Meta:
        verbose_name = 'Сессия платежа Unity'
        verbose_name_plural = 'Сессии платежей Unity'
        ordering = ['-created_at']
        db_table = 'payment_gateway_unity_sessions'
    
    def __str__(self):
        return f"Сессия {self.session_id} - {self.unity_user_id} ({self.amount} UZS)"
