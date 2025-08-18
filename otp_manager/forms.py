from django import forms
from .models import OTPCode

class OTPCodeForm(forms.ModelForm):
    """Форма для создания OTP кода кассиром"""
    
    class Meta:
        model = OTPCode
        fields = ['amount', 'quantity', 'currency']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите сумму',
                'min': '0.01',
                'step': '0.01'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество чеков',
                'min': '1',
                'max': '10'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['currency'].choices = [
            ('UZS', 'Узбекский сум'),
            ('USD', 'Доллар США'),
            ('EUR', 'Евро'),
        ]
        self.fields['amount'].label = "Сумма оплаты"
        self.fields['quantity'].label = "Количество чеков"
        self.fields['currency'].label = "Валюта"
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount <= 0:
            raise forms.ValidationError('Сумма должна быть больше нуля')
        return amount
    
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError('Количество чеков должно быть не менее 1')
        if quantity > 10:
            raise forms.ValidationError('Максимальное количество чеков - 10')
        return quantity

class CashPaymentForm(forms.Form):
    """Упрощенная форма для наличного платежа - только количество билетов"""
    
    quantity = forms.IntegerField(
        label="Количество билетов",
        min_value=1,
        max_value=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control form-control-lg',
            'placeholder': 'Введите количество билетов',
            'min': '1',
            'max': '10',
            'style': 'font-size: 1.2rem; text-align: center;'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].help_text = "Цена и длительность берутся из настроек подписки"
