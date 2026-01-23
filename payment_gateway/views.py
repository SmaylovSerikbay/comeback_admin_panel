"""
Views for Payment Gateway app
"""

import hashlib
import uuid
import json
import logging
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.conf import settings
from .models import PaymentTransaction, PaymentCallback, UnityPaymentSession
from django.db import models

logger = logging.getLogger(__name__)

# Конфигурация FreedomPay
MERCHANT_ID = "552170"
SECRET_KEY = "wUQ18x3bzP86MUzn"

# URL для перенаправления
SITE_URL = "https://admin.comeback.uz"  # Боевой домен


def log_message(msg):
    """Логирование с временными метками"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] {msg}")
    print(f"[{timestamp}] {msg}")


def generate_signature(params_dict, script_name="payment.php"):
    """
    Генерация подписи по алгоритму FreedomPay
    """
    # 1. Сортируем параметры по алфавиту
    sorted_keys = sorted(params_dict.keys())
    
    # 2. Создаем массив значений в алфавитном порядке
    values = [str(params_dict[key]) for key in sorted_keys]
    
    # 3. Добавляем имя скрипта в начало
    values.insert(0, script_name)
    
    # 4. Добавляем SECRET_KEY в конец
    values.append(SECRET_KEY)
    
    # 5. Склеиваем через ';'
    sign_string = ';'.join(values)
    
    # 6. MD5 хеш
    signature = hashlib.md5(sign_string.encode('utf-8')).hexdigest()
    
    return signature, sign_string


def verify_signature(params_dict, received_signature):
    """Проверка подписи от FreedomPay"""
    try:
        # Убираем подпись из параметров для проверки
        params_copy = params_dict.copy()
        if 'pg_sig' in params_copy:
            del params_copy['pg_sig']
        
        # Определяем имя скрипта
        if 'pg_result' in params_copy:
            script_name = "result.php"
        else:
            script_name = "check.php"
        
        # Генерируем ожидаемую подпись
        expected_signature, check_string = generate_signature(params_copy, script_name)
        
        log_message(f"🔍 Проверка подписи:")
        log_message(f"   Получена: {received_signature}")
        log_message(f"   Ожидаем: {expected_signature}")
        log_message(f"   Строка: {check_string}")
        
        return expected_signature == received_signature
    except Exception as e:
        log_message(f"❌ Ошибка проверки подписи: {e}")
        return False


@csrf_exempt
@require_http_methods(["POST"])
def unity_create_payment(request):
    """
    API endpoint для Unity - создание платежа
    """
    try:
        data = json.loads(request.body)
        unity_user_id = data.get('unity_user_id')
        amount = data.get('amount')
        description = data.get('description', 'Unity Payment')
        
        if not unity_user_id or not amount:
            return JsonResponse({
                'success': False,
                'error': 'Missing unity_user_id or amount'
            }, status=400)
        
        # Создаем сессию платежа
        session_id = f"unity_{uuid.uuid4().hex[:16]}"
        session = UnityPaymentSession.objects.create(
            session_id=session_id,
            unity_user_id=unity_user_id,
            amount=amount,
            description=description,
            expires_at=timezone.now() + timedelta(hours=1)
        )
        
        # Создаем транзакцию
        transaction = PaymentTransaction.objects.create(
            order_id=f"unity_{uuid.uuid4().hex[:16]}",
            amount=amount,
            currency='UZS',
            description=description,
            unity_user_id=unity_user_id,
            unity_session_id=session_id,
            salt=uuid.uuid4().hex[:16],
            merchant_id=MERCHANT_ID
        )
        
        # Генерируем подпись
        params = {
            "pg_merchant_id": MERCHANT_ID,
            "pg_amount": str(amount),
            "pg_currency": "UZS",
            "pg_description": description,
            "pg_salt": transaction.salt,
            "pg_language": "ru",
            "pg_order_id": transaction.order_id,
            "payment_origin": "unity_app",
            "pg_success_url": "https://admin.comeback.uz/payment-gateway/freedompay/success/",
            "pg_fail_url": "https://admin.comeback.uz/payment-gateway/freedompay/fail/"
        }
        
        signature, sign_string = generate_signature(params)
        transaction.signature = signature
        transaction.save()
        
        # Формируем URL для перенаправления
        query_parts = []
        sorted_keys = sorted(params.keys())
        for key in sorted_keys:
            query_parts.append(f"{key}={params[key]}")
        query_parts.append(f"pg_sig={signature}")
        
        payment_url = f"https://api.freedompay.uz/payment.php?{'&'.join(query_parts)}"
        
        log_message(f"🎮 Unity создал платеж: {transaction.order_id} на {amount} UZS")
        
        return JsonResponse({
            'success': True,
            'order_id': transaction.order_id,
            'session_id': session_id,
            'payment_url': payment_url,
            'amount': amount,
            'currency': 'UZS'
        })
        
    except Exception as e:
        log_message(f"❌ Ошибка создания платежа Unity: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def unity_check_payment_status(request):
    """
    API endpoint для Unity - проверка статуса платежа
    """
    try:
        order_id = request.GET.get('order_id')
        session_id = request.GET.get('session_id')
        
        if not order_id and not session_id:
            return JsonResponse({
                'success': False,
                'error': 'Missing order_id or session_id'
            }, status=400)
        
        # Ищем транзакцию
        if order_id:
            transaction = PaymentTransaction.objects.filter(order_id=order_id).first()
        else:
            transaction = PaymentTransaction.objects.filter(unity_session_id=session_id).first()
        
        if not transaction:
            return JsonResponse({
                'success': False,
                'error': 'Transaction not found'
            }, status=404)
        
        log_message(f"🎮 Unity запрашивает статус для {transaction.order_id}: {transaction.status}")
        
        return JsonResponse({
            'success': True,
            'order_id': transaction.order_id,
            'status': transaction.status,
            'amount': transaction.amount,
            'currency': transaction.currency,
            'created_at': transaction.created_at.isoformat(),
            'paid_at': transaction.paid_at.isoformat() if transaction.paid_at else None
        })
        
    except Exception as e:
        log_message(f"❌ Ошибка проверки статуса Unity: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def freedompay_check(request):
    """
    Callback от FreedomPay - проверка заказа
    """
    log_message("▶ CHECK запрос получен от FreedomPay")
    log_message(f"📨 Данные: {dict(request.POST)}")
    
    # Проверяем подпись
    pg_sig = request.POST.get('pg_sig')
    if pg_sig:
        if verify_signature(dict(request.POST), pg_sig):
            log_message("✅ Подпись CHECK корректна")
        else:
            log_message("❌ Некорректная подпись CHECK")
            return HttpResponse("ERROR", status=400)
    else:
        log_message("⚠️ Подпись CHECK отсутствует")
    
    # Получаем данные заказа
    pg_order_id = request.POST.get('pg_order_id')
    pg_amount = request.POST.get('pg_amount')
    
    log_message(f"🆔 Order ID: {pg_order_id}")
    log_message(f"💰 Amount: {pg_amount} UZS")
    
    # Ищем транзакцию
    try:
        transaction = PaymentTransaction.objects.get(order_id=pg_order_id)
        
        # Создаем callback запись
        PaymentCallback.objects.create(
            transaction=transaction,
            callback_type='check',
            raw_data=dict(request.POST),
            processed=True
        )
        
        log_message(f"✅ CHECK обработан для заказа {pg_order_id}")
        
    except PaymentTransaction.DoesNotExist:
        log_message(f"❌ Заказ {pg_order_id} не найден")
        return HttpResponse("ERROR", status=400)
    
    return HttpResponse("OK", status=200)


@csrf_exempt
@require_http_methods(["POST"])
def freedompay_result(request):
    """
    Callback от FreedomPay - результат платежа
    """
    log_message("▶ RESULT запрос получен от FreedomPay")
    log_message(f"📨 Данные: {dict(request.POST)}")
    
    # Проверяем подпись
    pg_sig = request.POST.get('pg_sig')
    if pg_sig:
        if verify_signature(dict(request.POST), pg_sig):
            log_message("✅ Подпись RESULT корректна")
        else:
            log_message("❌ Некорректная подпись RESULT")
            return HttpResponse("ERROR", status=400)
    else:
        log_message("⚠️ Подпись RESULT отсутствует")
    
    # Обрабатываем результат платежа
    pg_result = request.POST.get('pg_result')
    pg_payment_id = request.POST.get('pg_payment_id')
    pg_order_id = request.POST.get('pg_order_id')
    pg_amount = request.POST.get('pg_amount')
    
    log_message(f"🆔 Order ID: {pg_order_id}")
    log_message(f"💳 Payment ID: {pg_payment_id}")
    log_message(f"💰 Amount: {pg_amount} UZS")
    log_message(f"📊 Result: {pg_result}")
    
    try:
        transaction = PaymentTransaction.objects.get(order_id=pg_order_id)
        
        # Создаем callback запись
        PaymentCallback.objects.create(
            transaction=transaction,
            callback_type='result',
            raw_data=dict(request.POST),
            processed=True
        )
        
        if pg_result == "1":
            log_message(f"✅ Платеж успешен! Payment ID: {pg_payment_id}")
            transaction.mark_as_paid(pg_payment_id)
        else:
            log_message(f"❌ Платеж не прошел. Результат: {pg_result}")
            transaction.mark_as_failed()
        
        log_message(f"✅ RESULT обработан для заказа {pg_order_id}")
        
    except PaymentTransaction.DoesNotExist:
        log_message(f"❌ Заказ {pg_order_id} не найден")
        return HttpResponse("ERROR", status=400)
    
    return HttpResponse("OK", status=200)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def freedompay_success(request):
    """
    Страница успешного платежа
    """
    if request.method == "POST":
        log_message("✅ Получен POST callback на /success")
        log_message(f"📨 POST данные: {dict(request.POST)}")
        
        # Обрабатываем как успешный callback
        if request.POST:
            pg_order_id = request.POST.get('pg_order_id')
            if pg_order_id:
                try:
                    transaction = PaymentTransaction.objects.get(order_id=pg_order_id)
                    transaction.mark_as_paid()
                    
                    # Создаем callback запись
                    PaymentCallback.objects.create(
                        transaction=transaction,
                        callback_type='success',
                        raw_data=dict(request.POST),
                        processed=True
                    )
                    
                    log_message(f"✅ Установлен статус 'success' для Order ID: {pg_order_id}")
                except PaymentTransaction.DoesNotExist:
                    log_message(f"❌ Заказ {pg_order_id} не найден")
        
        return HttpResponse("OK", status=200)
    
    # GET запрос - проверяем параметры FreedomPay и обновляем статус
    if request.GET:
        log_message("✅ Получен GET запрос на /success с параметрами")
        log_message(f"📨 GET параметры: {dict(request.GET)}")
        
        pg_order_id = request.GET.get('pg_order_id')
        if pg_order_id:
            try:
                transaction = PaymentTransaction.objects.get(order_id=pg_order_id)
                if transaction.status == 'pending':
                    transaction.mark_as_paid()
                    
                    # Создаем callback запись
                    PaymentCallback.objects.create(
                        transaction=transaction,
                        callback_type='success',
                        raw_data=dict(request.GET),
                        processed=True
                    )
                    
                    log_message(f"✅ Установлен статус 'success' для Order ID: {pg_order_id}")
                else:
                    log_message(f"ℹ️ Транзакция {pg_order_id} уже имеет статус: {transaction.status}")
            except PaymentTransaction.DoesNotExist:
                log_message(f"❌ Заказ {pg_order_id} не найден")
    
    return render(request, 'payment_gateway/success.html')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def freedompay_fail(request):
    """
    Страница неуспешного платежа
    """
    if request.method == "POST":
        log_message("❌ Получен POST callback на /fail")
        log_message(f"📨 POST данные: {dict(request.POST)}")
        
        # Обрабатываем как неуспешный callback
        if request.POST:
            pg_order_id = request.POST.get('pg_order_id')
            if pg_order_id:
                try:
                    transaction = PaymentTransaction.objects.get(order_id=pg_order_id)
                    transaction.mark_as_failed()
                    
                    # Создаем callback запись
                    PaymentCallback.objects.create(
                        transaction=transaction,
                        callback_type='fail',
                        raw_data=dict(request.POST),
                        processed=True
                    )
                    
                    log_message(f"❌ Установлен статус 'failed' для Order ID: {pg_order_id}")
                except PaymentTransaction.DoesNotExist:
                    log_message(f"❌ Заказ {pg_order_id} не найден")
        
        return HttpResponse("OK", status=200)
    
    # GET запрос - проверяем параметры FreedomPay и обновляем статус
    if request.GET:
        log_message("❌ Получен GET запрос на /fail с параметрами")
        log_message(f"📨 GET параметры: {dict(request.GET)}")
        
        pg_order_id = request.GET.get('pg_order_id')
        if pg_order_id:
            try:
                transaction = PaymentTransaction.objects.get(order_id=pg_order_id)
                if transaction.status == 'pending':
                    transaction.mark_as_failed()
                    
                    # Создаем callback запись
                    PaymentCallback.objects.create(
                        transaction=transaction,
                        callback_type='fail',
                        raw_data=dict(request.GET),
                        processed=True
                    )
                    
                    log_message(f"❌ Установлен статус 'failed' для Order ID: {pg_order_id}")
                else:
                    log_message(f"ℹ️ Транзакция {pg_order_id} уже имеет статус: {transaction.status}")
            except PaymentTransaction.DoesNotExist:
                log_message(f"❌ Заказ {pg_order_id} не найден")
    
    return render(request, 'payment_gateway/fail.html')


@login_required
def payment_dashboard(request):
    """
    Дашборд для администраторов - просмотр всех платежей
    """
    transactions = PaymentTransaction.objects.all().order_by('-created_at')
    
    # Статистика
    stats = {
        'total': transactions.count(),
        'pending': transactions.filter(status='pending').count(),
        'success': transactions.filter(status='success').count(),
        'failed': transactions.filter(status='failed').count(),
        'total_amount': transactions.filter(status='success').aggregate(
            total=models.Sum('amount')
        )['total'] or 0
    }
    
    context = {
        'transactions': transactions,
        'stats': stats,
        'title': 'Дашборд платежей'
    }
    
    return render(request, 'payment_gateway/dashboard.html', context)


@login_required
def transaction_detail(request, order_id):
    """
    Детальная информация о транзакции
    """
    try:
        transaction = PaymentTransaction.objects.get(order_id=order_id)
        callbacks = transaction.callbacks.all().order_by('-created_at')
        
        context = {
            'transaction': transaction,
            'callbacks': callbacks,
            'title': f'Транзакция {order_id}'
        }
        
        return render(request, 'payment_gateway/transaction_detail.html', context)
        
    except PaymentTransaction.DoesNotExist:
        return render(request, 'payment_gateway/error.html', {
            'error': 'Транзакция не найдена',
            'title': 'Ошибка'
        })


def test_payment_form(request):
    """
    Тестовая форма для создания платежа (для разработки)
    """
    if request.method == 'POST':
        amount = request.POST.get('amount', '1000')
        description = request.POST.get('description', 'Test Payment')
        
        # Создаем тестовый платеж
        transaction = PaymentTransaction.objects.create(
            order_id=f"test_{uuid.uuid4().hex[:16]}",
            amount=int(amount),
            currency='UZS',
            description=description,
            salt=uuid.uuid4().hex[:16],
            merchant_id=MERCHANT_ID
        )
        
        # Генерируем подпись
        params = {
            "pg_merchant_id": MERCHANT_ID,
            "pg_amount": str(amount),
            "pg_currency": "UZS",
            "pg_description": description,
            "pg_salt": transaction.salt,
            "pg_language": "ru",
            "pg_order_id": transaction.order_id,
            "payment_origin": "test_form",
            "pg_success_url": "https://admin.comeback.uz/payment-gateway/freedompay/success/",
            "pg_fail_url": "https://admin.comeback.uz/payment-gateway/freedompay/fail/"
        }
        
        signature, sign_string = generate_signature(params)
        transaction.signature = signature
        transaction.save()
        
        # Формируем URL для перенаправления
        query_parts = []
        sorted_keys = sorted(params.keys())
        for key in sorted_keys:
            query_parts.append(f"{key}={params[key]}")
        query_parts.append(f"pg_sig={signature}")
        
        payment_url = f"https://api.freedompay.uz/payment.php?{'&'.join(query_parts)}"
        
        return redirect(payment_url)
    
    return render(request, 'payment_gateway/test_form.html', {
        'title': 'Тестовая форма платежа'
    })


def api_documentation(request):
    """
    Документация API для Unity разработчиков
    """
    return render(request, 'payment_gateway/api_docs.html', {
        'title': 'API Документация',
        'site_url': SITE_URL
    })
