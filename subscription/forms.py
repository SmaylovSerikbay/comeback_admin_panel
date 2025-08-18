"""
Forms for subscription settings
"""

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column, HTML
from .models import SubscriptionSettings


class SubscriptionSettingsForm(forms.ModelForm):
    """Form for managing subscription settings"""
    
    class Meta:
        model = SubscriptionSettings
        fields = ['price', 'currency', 'duration_minutes', 'is_active']
        widgets = {
            'price': forms.NumberInput(attrs={
                'placeholder': '5000.00',
                'step': '0.01',
                'min': '0.01'
            }),
            'duration_minutes': forms.NumberInput(attrs={
                'placeholder': '30',
                'min': '1',
                'max': '1440'
            }),
            'currency': forms.Select(choices=[
                ('UZS', 'UZS (Узбекский сум)'),
                ('USD', 'USD (Доллар США)'),
                ('EUR', 'EUR (Евро)'),
                ('RUB', 'RUB (Российский рубль)'),
            ])
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-3'
        self.helper.field_class = 'col-lg-9'
        
        self.helper.layout = Layout(
            HTML('''
                <div class="alert alert-info mb-4">
                    <h6><i class="fas fa-info-circle me-2"></i>Настройки подписки</h6>
                    <p class="mb-0">Эти настройки будут автоматически синхронизированы с Firebase и использованы в Unity приложении для системы оплаты.</p>
                </div>
            '''),
            
            Fieldset(
                'Цена и валюта',
                Row(
                    Column('price', css_class='form-group col-md-8 mb-0'),
                    Column('currency', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row'
                ),
                css_class='mb-4'
            ),
            
            Fieldset(
                'Длительность подписки',
                'duration_minutes',
                HTML('''
                    <div class="alert alert-success mt-2">
                        <small>
                            <strong>Примеры:</strong><br>
                            • 30 минут = полчаса доступа к AR контенту<br>
                            • 60 минут = 1 час доступа<br>
                            • 1440 минут = 24 часа (максимум)
                        </small>
                    </div>
                '''),
                css_class='mb-4'
            ),
            
            Fieldset(
                'Статус',
                'is_active',
                HTML('''
                    <div class="alert alert-warning mt-2">
                        <small>
                            <i class="fas fa-exclamation-triangle me-1"></i>
                            Если выключить, система подписки не будет работать в Unity приложении
                        </small>
                    </div>
                '''),
                css_class='mb-4'
            ),
            
            HTML('''
                <div class="alert alert-primary">
                    <h6><i class="fab fa-google me-2"></i>Синхронизация с Firebase</h6>
                    <p class="mb-0">После сохранения настройки автоматически отправятся в Firebase Realtime Database по пути <code>/subscription_settings</code></p>
                </div>
            '''),
            
            Submit('submit', 'Сохранить настройки', css_class='btn btn-primary btn-lg')
        )
