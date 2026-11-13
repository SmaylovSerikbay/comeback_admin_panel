"""
Сервис интеграции с CyberSource Unified Checkout (Visa / Mastercard).

Поток:
1. POST /uc/v1/sessions          -> capture context (JWT) для клиентского SDK.
2. JS SDK на странице оплаты     -> transient token (JWT).
3. POST /pts/v2/payments         -> авторизация/списание по transient token.
4. GET  /pts/v2/payments/{id}    -> проверка статуса (для PENDING).

Аутентификация REST API: HTTP Signature (Shared Secret Key).
Документация: developer.cybersource.com (Unified Checkout, REST Getting Started).

ВНИМАНИЕ: с 2026-2027 CyberSource переводит merchant-ов на OAuth 2.0 + MLE.
HTTP Signature оставлен как рабочий вариант до окончания миграции.
"""

import base64
import hashlib
import hmac
import json
import logging
from datetime import datetime
from decimal import Decimal, InvalidOperation
from email.utils import formatdate

import requests
from decouple import config

logger = logging.getLogger(__name__)

CYBERSOURCE_ENVIRONMENT = config('CYBERSOURCE_ENVIRONMENT', default='test').strip().lower()
CYBERSOURCE_MERCHANT_ID = config('CYBERSOURCE_MERCHANT_ID', default='').strip()
CYBERSOURCE_KEY_ID = config('CYBERSOURCE_KEY_ID', default='').strip()
CYBERSOURCE_SHARED_SECRET = config('CYBERSOURCE_SHARED_SECRET', default='').strip()
CYBERSOURCE_COUNTRY = config('CYBERSOURCE_COUNTRY', default='UZ').strip()
CYBERSOURCE_LOCALE = config('CYBERSOURCE_LOCALE', default='ru_RU').strip()
CYBERSOURCE_CURRENCY = config('CYBERSOURCE_CURRENCY', default='UZS').strip()
CYBERSOURCE_CAPTURE = config('CYBERSOURCE_CAPTURE', default=True, cast=bool)
CYBERSOURCE_TIMEOUT = config('CYBERSOURCE_TIMEOUT', default=30, cast=int)
CYBERSOURCE_ALLOWED_CARD_NETWORKS = ['VISA', 'MASTERCARD']

TEST_HOST = 'apitest.cybersource.com'
PRODUCTION_HOST = 'api.cybersource.com'
SESSIONS_PATH = '/uc/v1/sessions'
PAYMENTS_PATH = '/pts/v2/payments'


class CyberSourceError(Exception):
    """Ошибка CyberSource API или конфигурации."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


class CyberSourceConfigError(CyberSourceError):
    """Не заданы обязательные параметры CyberSource."""


def log_message(msg):
    logger.info(msg)


def is_configured():
    return bool(
        CYBERSOURCE_MERCHANT_ID
        and CYBERSOURCE_KEY_ID
        and CYBERSOURCE_SHARED_SECRET
    )


def configuration_error():
    missing = [
        name
        for name, value in (
            ('CYBERSOURCE_MERCHANT_ID', CYBERSOURCE_MERCHANT_ID),
            ('CYBERSOURCE_KEY_ID', CYBERSOURCE_KEY_ID),
            ('CYBERSOURCE_SHARED_SECRET', CYBERSOURCE_SHARED_SECRET),
        )
        if not value
    ]
    if missing:
        return (
            'CyberSource не настроен. Заполните в .env: ' + ', '.join(missing) +
            '. Ключи создаются в Business Center -> Payment Configuration -> '
            'Key Management -> REST API keys (Shared Secret).'
        )
    return ''


def _hostname():
    if CYBERSOURCE_ENVIRONMENT == 'production':
        return PRODUCTION_HOST
    return TEST_HOST


def _base_url():
    return f'https://{_hostname()}'


def _require_config():
    if not is_configured():
        raise CyberSourceConfigError(configuration_error())


def _shared_secret_bytes():
    secret = CYBERSOURCE_SHARED_SECRET
    if not secret:
        raise CyberSourceConfigError(configuration_error())
    try:
        return base64.b64decode(secret, validate=True)
    except Exception:
        return secret.encode('utf-8')


def format_amount(amount):
    try:
        return f'{Decimal(str(amount)):.2f}'
    except (InvalidOperation, ValueError):
        raise CyberSourceError(f'Некорректная сумма платежа: {amount!r}')


def _digest(body_bytes):
    return base64.b64encode(hashlib.sha256(body_bytes).digest()).decode('utf-8')


def _build_headers(method, resource, body_bytes=b''):
    _require_config()
    method = method.upper()
    host = _hostname()
    date = formatdate(usegmt=True)
    request_target = f'{method.lower()} {resource}'

    lines = [
        f'host: {host}',
        f'date: {date}',
        f'request-target: {request_target}',
    ]
    if method == 'POST':
        digest = _digest(body_bytes)
        lines.append(f'digest: SHA-256={digest}')
        signed_headers = 'host date request-target digest v-c-merchant-id'
    else:
        digest = None
        signed_headers = 'host date request-target v-c-merchant-id'
    lines.append(f'v-c-merchant-id: {CYBERSOURCE_MERCHANT_ID}')

    signing_string = '\n'.join(lines).encode('utf-8')
    signature = base64.b64encode(
        hmac.new(_shared_secret_bytes(), signing_string, hashlib.sha256).digest()
    ).decode('utf-8')

    headers = {
        'Host': host,
        'Date': date,
        'v-c-merchant-id': CYBERSOURCE_MERCHANT_ID,
        'Signature': (
            f'keyid="{CYBERSOURCE_KEY_ID}", algorithm="HmacSHA256", '
            f'headers="{signed_headers}", signature="{signature}"'
        ),
        'Content-Type': 'application/json',
    }
    if digest:
        headers['Digest'] = f'SHA-256={digest}'
    return headers


def _error_from_response(resp):
    try:
        data = resp.json()
    except ValueError:
        return f'CyberSource HTTP {resp.status_code}: {resp.text[:300]}'
    error = data.get('errorInformation') or {}
    message = error.get('message') or resp.text[:300]
    reason = error.get('reason')
    if reason:
        message = f'{message} ({reason})'
    return f'CyberSource HTTP {resp.status_code}: {message}'


def _request(method, resource, payload=None, expect_json=True):
    _require_config()
    method = method.upper()
    body_bytes = b''
    if payload is not None:
        body_bytes = json.dumps(payload, separators=(',', ':')).encode('utf-8')

    headers = _build_headers(method, resource, body_bytes)
    url = f'{_base_url()}{resource}'

    try:
        resp = requests.request(
            method,
            url,
            data=body_bytes if method == 'POST' else None,
            headers=headers,
            timeout=CYBERSOURCE_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise CyberSourceError(f'CyberSource недоступен: {exc}') from exc

    if resp.status_code >= 400:
        raise CyberSourceError(
            _error_from_response(resp),
            status_code=resp.status_code,
        )

    if not expect_json:
        return resp.text

    try:
        return resp.json()
    except ValueError as exc:
        raise CyberSourceError(
            f'CyberSource вернул не JSON (HTTP {resp.status_code}): {resp.text[:300]}'
        ) from exc


def create_capture_context(amount, currency, order_id, target_origins):
    """
    Создать capture context (JWT) для Unified Checkout JS SDK.
    target_origins — список origin'ов страницы оплаты (scheme://host[:port]).
    """
    origins = []
    for origin in target_origins or []:
        origin = (origin or '').strip().rstrip('/')
        if origin and origin not in origins:
            origins.append(origin)
    if not origins:
        raise CyberSourceConfigError('Не задан targetOrigins для CyberSource.')

    payload = {
        'targetOrigins': origins,
        'country': CYBERSOURCE_COUNTRY,
        'locale': CYBERSOURCE_LOCALE,
        'clientVersion': '1.0',
        'allowedCardNetworks': CYBERSOURCE_ALLOWED_CARD_NETWORKS,
        'allowedPaymentTypes': ['PANENTRY'],
        'completeMandate': {
            'type': 'CAPTURE',
            'consumerAuthentication': '3DS',
        },
        'data': {
            'orderInformation': {
                'amountDetails': {
                    'totalAmount': format_amount(amount),
                    'currency': currency or CYBERSOURCE_CURRENCY,
                },
            },
        },
    }

    capture_context = _request(
        'POST',
        SESSIONS_PATH,
        payload,
        expect_json=False,
    ).strip()
    if not capture_context:
        raise CyberSourceError('CyberSource вернул пустой capture context.')
    log_message(
        f'CyberSource: создан capture context для заказа {order_id} '
        f'на {format_amount(amount)} {currency}'
    )
    return capture_context


def authorize_payment(transient_token, amount, currency, order_id):
    """Авторизовать (и сразу списать) платёж по transient token из Unified Checkout."""
    if not transient_token:
        raise CyberSourceError('Не передан transient token CyberSource.')

    payload = {
        'clientReferenceInformation': {'code': str(order_id)[:50]},
        'processingInformation': {
            'capture': CYBERSOURCE_CAPTURE,
            'commerceIndicator': 'internet',
        },
        'tokenInformation': {'transientTokenJwt': transient_token},
        'orderInformation': {
            'amountDetails': {
                'totalAmount': format_amount(amount),
                'currency': currency or CYBERSOURCE_CURRENCY,
            },
        },
    }
    result = _request('POST', PAYMENTS_PATH, payload)
    log_message(
        f'CyberSource: авторизация заказа {order_id} -> '
        f"{result.get('status')} ({result.get('id')})"
    )
    return result


def get_payment(payment_id):
    """Получить детали платежа по CyberSource transaction id."""
    if not payment_id:
        raise CyberSourceError('Не передан CyberSource transaction id.')
    resource = f'{PAYMENTS_PATH}/{payment_id}'
    return _request('GET', resource)


def _decode_jwt_payload(token):
    try:
        parts = token.split('.')
        if len(parts) < 2:
            raise ValueError('not a JWT')
        segment = parts[1]
        segment += '=' * (-len(segment) % 4)
        decoded = base64.urlsafe_b64decode(segment.encode('utf-8'))
        return json.loads(decoded.decode('utf-8'))
    except Exception as exc:
        raise CyberSourceError('Не удалось декодировать capture context JWT.') from exc


def _deep_find(obj, key):
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for value in obj.values():
            found = _deep_find(value, key)
            if found is not None:
                return found
    elif isinstance(obj, list):
        for item in obj:
            found = _deep_find(item, key)
            if found is not None:
                return found
    return None


def extract_client_library(capture_context):
    """
    Достать URL и integrity клиентской библиотеки Unified Checkout
    из capture context (их нельзя хардкодить).
    """
    payload = _decode_jwt_payload(capture_context)
    client_library = _deep_find(payload, 'clientLibrary')
    integrity = _deep_find(payload, 'clientLibraryIntegrity')
    if not client_library:
        raise CyberSourceError(
            'В capture context отсутствует clientLibrary. '
            'Проверьте ответ Sessions API.'
        )
    if client_library.startswith('/'):
        client_library = f'{_base_url()}{client_library}'
    return client_library, integrity or ''


def is_success_status(status):
    return (status or '').upper() in ('AUTHORIZED', 'CAPTURED', 'COMPLETED')


def is_pending_status(status):
    return (status or '').upper() in (
        'PENDING',
        'AUTHORIZED_PENDING_REVIEW',
        'PARTIAL_AUTHORIZED',
        'CHALLENGE',
    )


def is_failed_status(status):
    return (status or '').upper() in (
        'DECLINED',
        'FAILED',
        'AUTHENTICATION_FAILED',
        'AUTHORIZED_RISK_DECLINED',
    )


def response_message(result):
    result = result or {}
    error = result.get('errorInformation') or {}
    message = error.get('message') or ''
    reason = error.get('reason') or ''
    if message and reason:
        return f'{message} ({reason})'
    return message or reason or result.get('message') or ''
