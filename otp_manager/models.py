from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid

class OTPCode(models.Model):
    """Модель для OTP кодов активации AR"""
    
    STATUS_CHOICES = [
        ('active', 'Активен'),
        ('used', 'Использован'),
        ('expired', 'Истек'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=6, unique=True, help_text="6-значный OTP код")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Сумма оплаты")
    quantity = models.IntegerField(default=1, help_text="Количество чеков/активаций")
    currency = models.CharField(max_length=10, default='UZS', help_text="Валюта")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, help_text="Кассир, создавший код")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Время создания")
    used_at = models.DateTimeField(null=True, blank=True, help_text="Время использования")
    device_id = models.CharField(max_length=255, blank=True, null=True, help_text="ID устройства, использовавшего код")
    firebase_key = models.CharField(max_length=255, blank=True, null=True, help_text="Ключ в Firebase")
    
    class Meta:
        verbose_name = "OTP код"
        verbose_name_plural = "OTP коды"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"OTP {self.code} - {self.amount} {self.currency} ({self.quantity} чеков)"
    
    @property
    def is_active(self):
        """Проверяет, активен ли код"""
        return self.status == 'active'
    
    @property
    def can_use(self):
        """Проверяет, можно ли использовать код"""
        return self.is_active and not self.is_expired
    
    @property
    def is_expired(self):
        """Проверяет, истек ли код (24 часа)"""
        if self.created_at:
            return timezone.now() - self.created_at > timezone.timedelta(hours=24)
        return False
    
    def mark_as_used(self, device_id=None):
        """Помечает код как использованный"""
        self.status = 'used'
        self.used_at = timezone.now()
        if device_id:
            self.device_id = device_id
        self.save()
    
    def mark_as_expired(self):
        """Помечает код как истекший"""
        self.status = 'expired'
        self.save()
