"""
Models for Video Manager app
"""

from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class VideoObject(models.Model):
    """Model for video objects that will be placed in AR"""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('Название видео', max_length=200)
    description = models.TextField('Описание', blank=True)
    
    # GPS coordinates
    latitude = models.FloatField(
        'Широта',
        validators=[MinValueValidator(-90), MaxValueValidator(90)],
        help_text='Широта от -90 до 90 градусов'
    )
    longitude = models.FloatField(
        'Долгота', 
        validators=[MinValueValidator(-180), MaxValueValidator(180)],
        help_text='Долгота от -180 до 180 градусов'
    )
    
    # Video file or URL
    video_file = models.FileField(
        'Видео файл',
        upload_to='videos/',
        blank=True,
        null=True,
        help_text='Загрузите видео файл или укажите URL ниже'
    )
    video_url = models.URLField(
        'URL видео',
        blank=True,
        help_text='URL видео (если не загружен файл)'
    )
    
    # Metadata
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('Дата обновления', auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Создано пользователем'
    )
    
    is_active = models.BooleanField('Активно', default=True)
    
    class Meta:
        verbose_name = 'Видео объект'
        verbose_name_plural = 'Видео объекты'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} ({self.latitude}, {self.longitude})"
    
    @property
    def video_source(self):
        """Get video source URL"""
        if self.video_file:
            return self.video_file.url
        return self.video_url
    
    def to_firebase_dict(self):
        """Convert to Firebase format"""
        return {
            'id': str(self.id),
            'x': float(self.latitude),  # Firebase uses x for latitude
            'y': float(self.longitude), # Firebase uses y for longitude
            'objectType': 'video',
            'objectURL': self.video_source,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'created_by': self.created_by.username,
            'is_active': self.is_active,
        }


class UserRole(models.Model):
    """Extended user roles for the system"""
    
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('cashier', 'Кассир'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        'Роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default='cashier'
    )
    
    class Meta:
        verbose_name = 'Роль пользователя'
        verbose_name_plural = 'Роли пользователей'
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
