from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Q
import json
import random
import string
from .models import OTPCode
from .forms import OTPCodeForm, CashPaymentForm
from firebase_service import FirebaseService

def is_cashier(user):
    """Проверяет, является ли пользователь кассиром"""
    if user.is_superuser:
        return True
    try:
        return hasattr(user, 'userrole') and user.userrole.role == 'cashier'
    except:
        return False

def is_admin_or_cashier(user):
    """Проверяет, является ли пользователь админом или кассиром"""
    if user.is_superuser:
        return True
    try:
        return hasattr(user, 'userrole') and user.userrole.role in ['admin', 'cashier']
    except:
        return False

@login_required
@user_passes_test(is_admin_or_cashier)
def otp_list(request):
    """Список всех OTP кодов"""
    if request.user.is_superuser:
        # Админ видит все коды
        otp_codes = OTPCode.objects.all()
    else:
        # Кассир видит только свои коды
        otp_codes = OTPCode.objects.filter(created_by=request.user)
    
    context = {
        'otp_codes': otp_codes,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'otp_manager/otp_list.html', context)

@login_required
@user_passes_test(is_cashier)
def create_otp(request):
    """Создание нового OTP кода кассиром"""
    if request.method == 'POST':
        form = OTPCodeForm(request.POST)
        if form.is_valid():
            try:
                # Генерируем уникальный 6-значный код
                code = generate_unique_otp()
                
                # Создаем OTP код
                otp_code = form.save(commit=False)
                otp_code.code = code
                otp_code.created_by = request.user
                otp_code.save()
                
                # Сохраняем в Firebase
                firebase_service = FirebaseService()
                firebase_key = firebase_service.add_otp_code(otp_code)
                
                # Обновляем Firebase ключ
                otp_code.firebase_key = firebase_key
                otp_code.save()
                
                messages.success(request, f'OTP код {code} успешно создан!')
                return redirect('otp_manager:otp_list')
                
            except Exception as e:
                messages.error(request, f'Ошибка при создании OTP: {str(e)}')
    else:
        form = OTPCodeForm()
    
    context = {
        'form': form,
        'title': 'Создать OTP код'
    }
    return render(request, 'otp_manager/otp_form.html', context)

@login_required
@user_passes_test(is_cashier)
def cash_payment(request):
    """Страница для создания OTP кода при наличном платеже"""
    if request.method == 'POST':
        form = CashPaymentForm(request.POST)
        if form.is_valid():
            try:
                # Получаем количество билетов
                quantity = form.cleaned_data['quantity']
                
                # Получаем настройки подписки из Firebase
                firebase_service = FirebaseService()
                subscription_settings = firebase_service.get_subscription_settings()
                
                if not subscription_settings:
                    messages.error(request, 'Не удалось получить настройки подписки')
                    return redirect('otp_manager:cash_payment')
                
                # Берем цену, валюту и длительность из настроек
                price_per_ticket = subscription_settings.get('price', 5000)
                currency = subscription_settings.get('currency', 'UZS')
                duration_per_ticket = subscription_settings.get('duration_minutes', 30)
                
                # Создаем ОТДЕЛЬНЫЙ OTP код для КАЖДОГО билета
                otp_codes = []
                
                for i in range(quantity):
                    # Генерируем уникальный 6-значный код для каждого билета
                    code = generate_unique_otp()
                    
                    # Создаем OTP код для одного билета
                    otp_code = OTPCode.objects.create(
                        code=code,
                        amount=price_per_ticket,  # Цена за ОДИН билет
                        quantity=duration_per_ticket,  # Длительность в минутах из настроек
                        currency=currency,
                        created_by=request.user
                    )
                    
                    # Сохраняем в Firebase
                    firebase_key = firebase_service.add_otp_code(otp_code)
                    
                    # Обновляем Firebase ключ
                    otp_code.firebase_key = firebase_key
                    otp_code.save()
                    
                    otp_codes.append(otp_code)
                
                # Показываем сообщение с количеством созданных кодов
                if quantity == 1:
                    messages.success(request, f'Наличный платеж принят! OTP код: {otp_codes[0].code}')
                    return redirect('otp_manager:print_receipt', otp_id=otp_codes[0].id)
                else:
                    messages.success(request, f'Наличный платеж принят! Создано {quantity} OTP кодов')
                    # Перенаправляем на список OTP кодов
                    return redirect('otp_manager:otp_list')
                
            except Exception as e:
                messages.error(request, f'Ошибка при создании OTP: {str(e)}')
    else:
        form = CashPaymentForm()
    
    # Получаем текущие настройки для отображения
    firebase_service = FirebaseService()
    subscription_settings = firebase_service.get_subscription_settings() or {}
    
    context = {
        'form': form,
        'title': 'Наличный платеж - Создать OTP код',
        'subscription_price': subscription_settings.get('price', 5000),
        'subscription_currency': subscription_settings.get('currency', 'UZS'),
        'subscription_duration': subscription_settings.get('duration_minutes', 30)
    }
    return render(request, 'otp_manager/cash_payment.html', context)

@login_required
@user_passes_test(is_admin_or_cashier)
def otp_detail(request, otp_id):
    """Детальная информация об OTP коде"""
    otp_code = get_object_or_404(OTPCode, id=otp_id)
    
    # Проверяем права доступа
    if not request.user.is_superuser and otp_code.created_by != request.user:
        messages.error(request, 'У вас нет прав для просмотра этого кода')
        return redirect('otp_manager:otp_list')
    
    context = {
        'otp_code': otp_code,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'otp_manager/otp_detail.html', context)

@login_required
@user_passes_test(is_admin_or_cashier)
def print_receipt(request, otp_id):
    """Печать чека для OTP кода"""
    otp_code = get_object_or_404(OTPCode, id=otp_id)
    
    # Проверяем права доступа
    if not request.user.is_superuser and otp_code.created_by != request.user:
        messages.error(request, 'У вас нет прав для печати этого чека')
        return redirect('otp_manager:otp_list')
    
    context = {
        'otp_code': otp_code,
        'is_admin': request.user.is_superuser
    }
    return render(request, 'otp_manager/receipt.html', context)

@csrf_exempt
def verify_otp_api(request):
    """API для проверки OTP кода (для Unity)"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        otp_code = data.get('otp_code')
        device_id = data.get('device_id')
        
        if not otp_code or not device_id:
            return JsonResponse({'error': 'Missing otp_code or device_id'}, status=400)
        
        # Проверяем код в Firebase
        firebase_service = FirebaseService()
        result = firebase_service.verify_otp_code(otp_code, device_id)
        
        return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def generate_unique_otp():
    """Генерирует уникальный 6-значный OTP код"""
    while True:
        # Генерируем 6-значный код
        code = ''.join(random.choices(string.digits, k=6))
        
        # Проверяем, что код уникален
        if not OTPCode.objects.filter(code=code).exists():
            return code
