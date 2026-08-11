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
from . import milliy_service
from django.db import models
from decouple import config

logger = logging.getLogger(__name__)

# Конфигурация FreedomPay
MERCHANT_ID = config('FREEDOMPAY_MERCHANT_ID', default="552170")
SECRET_KEY = config('FREEDOMPAY_SECRET_KEY', default="wUQ18x3bzP86MUzn")

# URL для перенаправления - теперь из переменных окружения
# Поддержка как IP адреса, так и домена
SITE_URL = config('SITE_URL', default='http://89.39.95.247')
SITE_DOMAIN = config('SITE_DOMAIN', default='admin.comeback.uz')
USE_HTTPS = config('USE_HTTPS', default=False, cast=bool)


def get_base_url():
    """
    Получить базовый URL для callback'ов
    Автоматически определяет правильный протокол и хост
    """
    protocol = 'https' if USE_HTTPS else 'http'
    
    # Если используется домен, используем его, иначе IP
    if SITE_DOMAIN and SITE_DOMAIN != 'admin.comeback.uz':
        return f"{protocol}://{SITE_DOMAIN}"
    else:
        return SITE_URL


def log_message(msg):
    """Логирование с временными метками"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logger.info(f"[{timestamp}] {msg}")
    print(f"[{timestamp}] {msg}")


def _create_milliy_transaction(amount, description, unity_user_id='', source=''):
    """
    Создание платежа через Milliy Ecom (REDIRECT).
    Возвращает (transaction, payment_url).
    """
    order_id = str(uuid.uuid4())  # Milliy требует orderId в формате UUID
    transaction = PaymentTransaction.objects.create(
        order_id=order_id,
        amount=amount,
        currency='UZS',
        description=description[:500],
        unity_user_id=unity_user_id or '',
        salt=uuid.uuid4().hex[:16],
        merchant_id=(milliy_service.MILLIY_API_KEY or 'milliy')[:50],
        gateway='milliy',
    )

    base_url = get_base_url()
    success_url = f"{base_url}/payment-gateway/milliy/success/"
    fail_url = f"{base_url}/payment-gateway/milliy/fail/"

    milliy_tx_id, payment_url = milliy_service.init_payment(
        amount_tiyin=amount * 100,  # Milliy работает в тийинах
        order_id=order_id,
        success_url=success_url,
        failure_url=fail_url,
        client_id=unity_user_id or None,
    )
    transaction.milliy_transaction_id = milliy_tx_id
    transaction.save()

    log_message(f"🎮 Milliy Ecom создал платёж: {transaction.order_id} на {amount} UZS ({source})")
    return transaction, payment_url


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
        # Парсинг JSON с обработкой ошибок
        body = request.body
        if not body:
            log_message("❌ Unity create-payment: пустое тело запроса")
            return JsonResponse({
                'success': False,
                'error': 'Empty request body. Send JSON with unity_user_id, amount, description'
            }, status=400)
        
        try:
            data = json.loads(body.decode('utf-8') if isinstance(body, bytes) else body)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            log_message(f"❌ Unity create-payment: ошибка парсинга JSON: {e}")
            return JsonResponse({
                'success': False,
                'error': f'Invalid JSON: {str(e)}'
            }, status=400)
        
        unity_user_id = data.get('unity_user_id')
        amount = data.get('amount')
        description = data.get('description', 'Unity Payment')
        
        if not unity_user_id or amount is None:
            return JsonResponse({
                'success': False,
                'error': 'Missing unity_user_id or amount'
            }, status=400)
        
        # Приводим amount к int (Unity может отправить как число или строку)
        try:
            amount = int(amount)
        except (TypeError, ValueError):
            return JsonResponse({
                'success': False,
                'error': f'Invalid amount: must be a number, got {type(amount).__name__}'
            }, status=400)
        
        if amount < 100:
            return JsonResponse({
                'success': False,
                'error': 'Minimum amount is 100 UZS'
            }, status=400)
        
        log_message(f"🎮 Unity create-payment: user_id={unity_user_id}, amount={amount}")

        gateway = data.get('gateway', 'freedom')

        if gateway == 'milliy':
            # Milliy Ecom (альтернативный эквайринг)
            try:
                transaction, payment_url = _create_milliy_transaction(
                    amount=amount,
                    description=description,
                    unity_user_id=unity_user_id,
                    source='unity',
                )
            except milliy_service.MilliyError as e:
                log_message(f"❌ Ошибка Milliy Ecom при создании платежа: {e}")
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                }, status=502)

            return JsonResponse({
                'success': True,
                'order_id': transaction.order_id,
                'milliy_transaction_id': transaction.milliy_transaction_id,
                'payment_url': payment_url,
                'amount': amount,
                'currency': 'UZS',
                'gateway': 'milliy'
            })

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
        
        # Получаем базовый URL
        base_url = get_base_url()
        
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
            "pg_success_url": f"{base_url}/payment-gateway/freedompay/success/",
            "pg_fail_url": f"{base_url}/payment-gateway/freedompay/fail/"
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
        logger.exception("Unity create-payment exception")
        return JsonResponse({
            'success': False,
            'error': str(e),
            'error_type': type(e).__name__
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

    # Редирект в новую админку (шаблон удалён)
    return redirect('/?payment=success')


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
    
    return redirect('/?payment=fail')


def _check_milliy_basic_auth(request):
    """Проверка Basic Auth для callback'ов Milliy Ecom."""
    auth_header = request.META.get('HTTP_AUTHORIZATION', '')
    if not auth_header.startswith('Basic '):
        return False
    try:
        import base64
        decoded = base64.b64decode(auth_header[6:]).decode('utf-8')
        username, _, password = decoded.partition(':')
    except Exception:
        return False
    expected_user = milliy_service.MILLIY_CALLBACK_USERNAME
    expected_pass = milliy_service.MILLIY_CALLBACK_PASSWORD
    return username == expected_user and password == expected_pass


@csrf_exempt
@require_http_methods(["POST"])
def milliy_callback(request):
    """
    Callback от Milliy Ecom — уведомление о статусе операции.
    Аутентификация: Basic Auth. Формат данных: JSON.
    """
    log_message("▶ MILLIY CALLBACK получен")
    log_message(f"📨 Данные: {request.body.decode('utf-8', errors='replace')[:1000]}")

    if not _check_milliy_basic_auth(request):
        log_message("❌ Milliy callback: некорректные Basic Auth данные")
        return HttpResponse("UNAUTHORIZED", status=401)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        log_message(f"❌ Milliy callback: невалидный JSON: {e}")
        return HttpResponse("ERROR", status=400)

    order_id = data.get('orderId')
    status = data.get('status')
    transaction_id = data.get('transactionId')
    error_code = data.get('errorCode')

    if not order_id or not status:
        log_message("❌ Milliy callback: нет orderId или status")
        return HttpResponse("ERROR", status=400)

    try:
        transaction = PaymentTransaction.objects.get(order_id=order_id)
    except PaymentTransaction.DoesNotExist:
        log_message(f"❌ Milliy callback: заказ {order_id} не найден")
        return HttpResponse("ERROR", status=400)

    PaymentCallback.objects.create(
        transaction=transaction,
        callback_type=f"milliy_{status.lower()}",
        raw_data=data,
        processed=True,
    )

    if status == "SUCCESS":
        log_message(f"✅ Milliy callback: платёж {order_id} успешен")
        transaction.mark_as_paid(transaction_id or transaction.milliy_transaction_id)
    elif status == "FAILED":
        log_message(f"❌ Milliy callback: платёж {order_id} отклонён (errorCode={error_code})")
        transaction.mark_as_failed()
    elif status == "EXPIRED":
        log_message(f"⚠️ Milliy callback: сессия {order_id} истекла")
        transaction.status = 'cancelled'
        transaction.save()
    elif status == "REFUNDED":
        log_message(f"↩️ Milliy callback: платёж {order_id} возвращён")
        transaction.status = 'cancelled'
        transaction.save()
    else:
        log_message(f"⚠️ Milliy callback: неизвестный статус {status} для {order_id}")

    return HttpResponse("OK", status=200)


@csrf_exempt
@require_http_methods(["GET", "POST"])
def milliy_success(request):
    """Страница успешного платежа Milliy Ecom."""
    if request.GET:
        log_message("✅ Получен GET запрос на milliy/success")
        log_message(f"📨 GET параметры: {dict(request.GET)}")
        order_id = request.GET.get('orderId') or request.GET.get('order_id')
        if order_id:
            try:
                transaction = PaymentTransaction.objects.get(order_id=order_id)
                if transaction.status == 'pending':
                    transaction.mark_as_paid(transaction.milliy_transaction_id)
                    PaymentCallback.objects.create(
                        transaction=transaction,
                        callback_type='milliy_success',
                        raw_data=dict(request.GET),
                        processed=True,
                    )
                    log_message(f"✅ Milliy: установлен статус 'success' для {order_id}")
                else:
                    log_message(f"ℹ️ Milliy: транзакция {order_id} уже в статусе {transaction.status}")
            except PaymentTransaction.DoesNotExist:
                log_message(f"❌ Milliy: заказ {order_id} не найден")

    return redirect('/?payment=success')


@csrf_exempt
@require_http_methods(["GET", "POST"])
def milliy_fail(request):
    """Страница неуспешного платежа Milliy Ecom."""
    if request.GET:
        log_message("❌ Получен GET запрос на milliy/fail")
        log_message(f"📨 GET параметры: {dict(request.GET)}")
        order_id = request.GET.get('orderId') or request.GET.get('order_id')
        if order_id:
            try:
                transaction = PaymentTransaction.objects.get(order_id=order_id)
                if transaction.status == 'pending':
                    transaction.mark_as_failed()
                    PaymentCallback.objects.create(
                        transaction=transaction,
                        callback_type='milliy_fail',
                        raw_data=dict(request.GET),
                        processed=True,
                    )
                    log_message(f"❌ Milliy: установлен статус 'failed' для {order_id}")
                else:
                    log_message(f"ℹ️ Milliy: транзакция {order_id} уже в статусе {transaction.status}")
            except PaymentTransaction.DoesNotExist:
                log_message(f"❌ Milliy: заказ {order_id} не найден")

    return redirect('/?payment=fail')


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
        
        # Получаем базовый URL
        base_url = get_base_url()
        
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
            "pg_success_url": f"{base_url}/payment-gateway/freedompay/success/",
            "pg_fail_url": f"{base_url}/payment-gateway/freedompay/fail/"
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
    base_url = get_base_url()
    return render(request, 'payment_gateway/api_docs.html', {
        'title': 'API Документация',
        'site_url': base_url,
        'base_url': base_url
    })


@csrf_exempt
@require_http_methods(["GET"])
def unity_health_check(request):
    """
    Health check endpoint для Unity - проверка доступности сервера
    """
    try:
        # Проверяем доступ к базе данных
        from django.db import connection
        connection.ensure_connection()
        
        base_url = get_base_url()
        
        return JsonResponse({
            'success': True,
            'status': 'healthy',
            'server_time': timezone.now().isoformat(),
            'base_url': base_url,
            'endpoints': {
                'create_payment': f'{base_url}/payment-gateway/api/unity/create-payment/',
                'check_status': f'{base_url}/payment-gateway/api/unity/check-status/'
            },
            'version': '1.0',
            'merchant_id': MERCHANT_ID
        })
    except Exception as e:
        log_message(f"❌ Health check failed: {e}")
        return JsonResponse({
            'success': False,
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def unity_server_info(request):
    """
    Endpoint для получения информации о сервере Unity
    Используется для диагностики проблем с подключением
    """
    try:
        base_url = get_base_url()
        
        info = {
            'success': True,
            'server_info': {
                'base_url': base_url,
                'site_url': SITE_URL,
                'domain': SITE_DOMAIN,
                'use_https': USE_HTTPS,
                'protocol': 'https' if USE_HTTPS else 'http'
            },
            'endpoints': {
                'create_payment': f'{base_url}/payment-gateway/api/unity/create-payment/',
                'check_status': f'{base_url}/payment-gateway/api/unity/check-status/',
                'health_check': f'{base_url}/payment-gateway/api/unity/health/',
                'server_info': f'{base_url}/payment-gateway/api/unity/server-info/'
            },
            'freedompay': {
                'merchant_id': MERCHANT_ID,
                'success_url': f'{base_url}/payment-gateway/freedompay/success/',
                'fail_url': f'{base_url}/payment-gateway/freedompay/fail/'
            },
            'server_time': timezone.now().isoformat(),
            'version': '1.0'
        }
        
        log_message(f"📊 Unity запросил информацию о сервере")
        
        return JsonResponse(info)
        
    except Exception as e:
        log_message(f"❌ Ошибка получения информации о сервере: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
