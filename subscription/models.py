"""
Models for subscription settings
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class SubscriptionSettings(models.Model):
    """
    Singleton model for subscription settings
    Stores price and duration that Unity app will use
    """
    
    # Price settings
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=5000.00,
        validators=[MinValueValidator(0.01)],
        verbose_name='Цена подписки (сум)',
        help_text='Цена в сумах за подписку'
    )
    
    # Duration settings  
    duration_minutes = models.PositiveIntegerField(
        default=30,
        validators=[MinValueValidator(1), MaxValueValidator(1440)],  # Max 24 hours
        verbose_name='Длительность подписки (минуты)',
        help_text='Количество минут доступа к AR контенту'
    )
    
    # Additional settings
    currency = models.CharField(
        max_length=10,
        default='UZS',
        verbose_name='Валюта',
        help_text='Код валюты (UZS, USD, EUR и т.д.)'
    )
    
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активно',
        help_text='Включить/выключить систему подписки'
    )
    
    # Metadata
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлено'
    )
    
    updated_by = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Обновил'
    )
    
    class Meta:
        verbose_name = 'Настройки подписки'
        verbose_name_plural = 'Настройки подписки'
        
    def save(self, *args, **kwargs):
        # Ensure only one instance exists (Singleton pattern)
        if not self.pk and SubscriptionSettings.objects.exists():
            # Update existing instance instead of creating new one
            existing = SubscriptionSettings.objects.first()
            existing.price = self.price
            existing.duration_minutes = self.duration_minutes
            existing.currency = self.currency
            existing.is_active = self.is_active
            existing.updated_by = self.updated_by
            existing.save()
            return existing
        return super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get current subscription settings"""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'price': 5000.00,
                'duration_minutes': 30,
                'currency': 'UZS',
                'is_active': True
            }
        )
        return settings
    
    def to_firebase_dict(self):
        """Convert to Firebase-compatible format for Unity"""
        return {
            'price': float(self.price),
            'duration_minutes': self.duration_minutes,
            'currency': self.currency,
            'is_active': self.is_active,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __str__(self):
        return f'{self.price} {self.currency} за {self.duration_minutes} минут'
