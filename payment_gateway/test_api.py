#!/usr/bin/env python3
"""
Тестирование API платежного шлюза
"""

import requests
import json
import time

# Базовый URL
BASE_URL = "https://comeback.uz/payment-gateway"

def test_unity_create_payment():
    """Тест создания платежа через Unity API"""
    print("🧪 Тестирование создания платежа Unity...")
    
    url = f"{BASE_URL}/api/unity/create-payment/"
    data = {
        "unity_user_id": "test_user_123",
        "amount": 1000,
        "description": "Test Unity Payment"
    }
    
    try:
        response = requests.post(url, json=data, headers={
            'Content-Type': 'application/json'
        })
        
        print(f"📡 Статус: {response.status_code}")
        print(f"📨 Ответ: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Платеж успешно создан!")
                print(f"   Order ID: {result.get('order_id')}")
                print(f"   Session ID: {result.get('session_id')}")
                print(f"   Payment URL: {result.get('payment_url')}")
                return result.get('order_id')
            else:
                print("❌ Ошибка создания платежа")
                print(f"   Ошибка: {result.get('error')}")
        else:
            print("❌ HTTP ошибка")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")
    
    return None

def test_unity_check_status(order_id):
    """Тест проверки статуса платежа"""
    if not order_id:
        print("❌ Order ID не указан")
        return
    
    print(f"🧪 Тестирование проверки статуса для {order_id}...")
    
    url = f"{BASE_URL}/api/unity/check-status/"
    params = {"order_id": order_id}
    
    try:
        response = requests.get(url, params=params)
        
        print(f"📡 Статус: {response.status_code}")
        print(f"📨 Ответ: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✅ Статус получен!")
                print(f"   Статус: {result.get('status')}")
                print(f"   Сумма: {result.get('amount')} {result.get('currency')}")
            else:
                print("❌ Ошибка получения статуса")
                print(f"   Ошибка: {result.get('error')}")
        else:
            print("❌ HTTP ошибка")
            
    except Exception as e:
        print(f"❌ Ошибка запроса: {e}")

def test_freedompay_callbacks():
    """Тест доступности callback endpoints"""
    print("🧪 Тестирование FreedomPay callback endpoints...")
    
    endpoints = [
        "/freedompay/check/",
        "/freedompay/result/",
        "/freedompay/success/",
        "/freedompay/fail/"
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        try:
            response = requests.get(url)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def test_admin_endpoints():
    """Тест административных endpoints"""
    print("🧪 Тестирование административных endpoints...")
    
    endpoints = [
        "/dashboard/",
        "/test/",
        "/api-docs/"
    ]
    
    for endpoint in endpoints:
        url = f"{BASE_URL}{endpoint}"
        try:
            response = requests.get(url)
            print(f"✅ {endpoint}: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint}: {e}")

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестирования Payment Gateway API")
    print("=" * 50)
    
    # Тест создания платежа
    order_id = test_unity_create_payment()
    
    if order_id:
        print("\n" + "=" * 50)
        # Ждем немного перед проверкой статуса
        time.sleep(2)
        
        # Тест проверки статуса
        test_unity_check_status(order_id)
    
    print("\n" + "=" * 50)
    
    # Тест callback endpoints
    test_freedompay_callbacks()
    
    print("\n" + "=" * 50)
    
    # Тест административных endpoints
    test_admin_endpoints()
    
    print("\n" + "=" * 50)
    print("🏁 Тестирование завершено!")

if __name__ == "__main__":
    main()
