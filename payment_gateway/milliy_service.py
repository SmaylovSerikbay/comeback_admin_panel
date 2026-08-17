"""
Сервис интеграции с эквайрингом Milliy Ecom (НБУ).

Реализовано по документации: api/Milliy Ecom.html

Поток платежа (REDIRECT):
1. GET  /auth/token/public-key  -> публичный RSA ключ + identityToken
2. POST /auth/token/init        -> accessToken / refreshToken (username/password шифруются RSA)
3. POST /payment/init           -> transactionId + paymentUrl (редирект клиента)
4. POST /payment/status         -> проверка статуса транзакции
5. Callback (Basic Auth)        -> уведомления о статусе операции

Подпись запроса: X-SIGNATURE = HMAC_SHA256(SECRET_KEY, X-TIMESTAMP + '.' + request_body)
Для GET-запросов request_body = "".
"""

import base64
import hashlib
import hmac
import json
import logging
import time
import uuid

import requests
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_der_public_key
from decouple import config

logger = logging.getLogger(__name__)

# ---- Конфигурация из .env -------------------------------------------------
MILLIY_API_KEY = config('MILLIY_API_KEY', default='')
MILLIY_SECRET_KEY = config('MILLIY_SECRET_KEY', default='')
MILLIY_BASE_URL = config('MILLIY_BASE_URL', default='https://ecom.nbu.uz/epgate')
MILLIY_USERNAME = config('MILLIY_USERNAME', default='')
MILLIY_PASSWORD = config('MILLIY_PASSWORD', default='')
MILLIY_CALLBACK_USERNAME = config('MILLIY_CALLBACK_USERNAME', default='comeback_milliy')
MILLIY_CALLBACK_PASSWORD = config('MILLIY_CALLBACK_PASSWORD', default='comeback_milliy_cb_2025')

# Внутренний кеш токенов и ключей (на время работы процесса)
_cache = {
    'pub_key': None,
    'identity_token': None,
    'access_token': None,
    'refresh_token': None,
    'expires_at': 0,
}


class MilliyError(Exception):
    """Ошибка API Milliy Ecom."""


def log_message(msg):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    logger.info(f'[{timestamp}] {msg}')
    print(f'[{timestamp}] {msg}')


def _raise_if_error(data):
    """Проверка единого формата ответа: status.code == 0 — успех."""
    status = data.get('status') or {}
    code = status.get('code')
    if code not in (0, None):
        raise MilliyError(f"{status.get('message', 'Ошибка Milliy Ecom')} (code={code})")


def _signature(timestamp, body=''):
    """HMAC-SHA256 по алгоритму Milliy Ecom."""
    msg = f'{timestamp}.{body}'.encode('utf-8')
    return hmac.new(
        MILLIY_SECRET_KEY.encode('utf-8'),
        msg,
        hashlib.sha256,
    ).hexdigest()


def _headers(body='', auth_token=None):
    """Обязательные заголовки запроса Milliy Ecom."""
    timestamp = str(int(time.time()))
    headers = {
        'X-API-KEY': MILLIY_API_KEY,
        'X-TIMESTAMP': timestamp,
        'X-REQUEST-ID': str(uuid.uuid4()),
        'X-SIGNATURE': _signature(timestamp, body),
    }
    if auth_token:
        headers['X-Auth-Token'] = auth_token
    return headers


def _post(url, body_dict, auth_token=None):
    """POST с JSON-телом и корректной подписью."""
    body = json.dumps(body_dict, separators=(',', ':'))
    headers = _headers(body, auth_token)
    headers['Content-Type'] = 'application/json'
    resp = requests.post(url, data=body.encode('utf-8'), headers=headers, timeout=30)
    return _parse_response(resp)


def _get(url):
    headers = _headers()
    resp = requests.get(url, headers=headers, timeout=30)
    return _parse_response(resp)


def _parse_response(resp):
    try:
        data = resp.json()
    except ValueError:
        raise MilliyError(f'Milliy Ecom: не JSON ответ {resp.status_code}: {resp.text[:300]}')
    if resp.status_code != 200:
        raise MilliyError(f'Milliy Ecom HTTP {resp.status_code}: {resp.text[:300]}')
    _raise_if_error(data)
    return data


def get_public_key(force=False):
    """Получение публичного RSA ключа и identityToken (кешируется)."""
    if not force and _cache['pub_key']:
        return _cache['pub_key'], _cache['identity_token']
    data = _get(f'{MILLIY_BASE_URL}/auth/token/public-key')
    pub_key = data['data']['pubKey']
    identity_token = data['data'].get('identityToken')
    _cache['pub_key'] = pub_key
    _cache['identity_token'] = identity_token
    log_message('✅ Milliy Ecom: получен публичный ключ')
    return pub_key, identity_token


def _rsa_encrypt(pub_key_b64, text):
    """RSA 2048, PKCS#1 v1.5 padding, результат base64."""
    der = base64.b64decode(pub_key_b64)
    pub_key = load_der_public_key(der)
    encrypted = pub_key.encrypt(text.encode('utf-8'), padding.PKCS1v15())
    return base64.b64encode(encrypted).decode('utf-8')


def _refresh_token():
    """Обновление access token через refresh token."""
    body = {
        'accessToken': _cache['access_token'],
        'refreshToken': _cache['refresh_token'],
    }
    data = _post(f'{MILLIY_BASE_URL}/auth/token/refresh', body)
    _apply_tokens(data['data'])
    return _cache['access_token']


def _apply_tokens(token_data):
    now = time.time()
    _cache['access_token'] = token_data['accessToken']
    _cache['refresh_token'] = token_data.get('refreshToken')
    _cache['expires_at'] = now + int(token_data.get('accessTokenExpire', 7200))
    log_message('✅ Milliy Ecom: access token обновлён')


def get_access_token(force=False):
    """Получение (и кеширование) access token. Возвращает accessToken."""
    now = time.time()
    if not force and _cache['access_token'] and now < _cache['expires_at'] - 60:
        return _cache['access_token']

    # Сначала пробуем refresh-токен
    if _cache['refresh_token']:
        try:
            return _refresh_token()
        except Exception as e:
            log_message(f'⚠️ Milliy Ecom: refresh не сработал ({e}), инициализируем заново')

    if not MILLIY_USERNAME or not MILLIY_PASSWORD:
        raise MilliyError(
            'MILLIY_USERNAME / MILLIY_PASSWORD не настроены в .env. '
            'Для получения access token Milliy Ecom требуются учётные данные мерчанта.'
        )

    pub_key, identity_token = get_public_key()
    body = {
        'username': _rsa_encrypt(pub_key, MILLIY_USERNAME),
        'password': _rsa_encrypt(pub_key, MILLIY_PASSWORD),
        'identityToken': identity_token or '',
    }
    data = _post(f'{MILLIY_BASE_URL}/auth/token/init', body)
    _apply_tokens(data['data'])
    return _cache['access_token']


def init_payment(amount_tiyin, order_id, success_url, failure_url, client_id=None, session_timeout=3600):
    """
    Одноэтапный платёж (REDIRECT).
    amount_tiyin — сумма в минимальных единицах (тийнах); минимально 100000 (1000 UZS).
    Возвращает (transactionId, paymentUrl).
    """
    token = get_access_token()
    payload = {
        'amount': int(amount_tiyin),
        'currency': 860,  # UZS
        'orderId': order_id,
        'paymentType': 'REDIRECT',
        'sessionTimeout': max(300, int(session_timeout)),
        'successUrl': success_url,
        'failureUrl': failure_url,
    }
    if client_id:
        payload['clientId'] = str(client_id)[:100]
    data = _post(f'{MILLIY_BASE_URL}/payment/init', payload, auth_token=token)
    tx = data['data']
    log_message(f'✅ Milliy Ecom: платёж создан orderId={order_id}, transactionId={tx["transactionId"]}')
    return tx['transactionId'], tx.get('url') or tx.get('paymentUrl')


def check_status(order_id):
    """Проверка статуса транзакции по orderId. Возвращает data ответа."""
    token = get_access_token()
    data = _post(f'{MILLIY_BASE_URL}/payment/status', {'orderId': order_id}, auth_token=token)
    return data['data']


def refund(transaction_id, refund_type='DEBIT'):
    """Возврат платежа. refund_type: 'DEBIT' (списание) или 'CREDIT' (пополнение)."""
    token = get_access_token()
    data = _post(
        f'{MILLIY_BASE_URL}/payment/refund',
        {'transactionId': transaction_id, 'type': refund_type},
        auth_token=token,
    )
    return data['data']
