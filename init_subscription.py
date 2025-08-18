#!/usr/bin/env python
"""
Инициализация настроек подписки и синхронизация с Firebase
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comeback_admin.settings')
django.setup()

from subscription.models import SubscriptionSettings
from firebase_service import firebase_service

def init_subscription_settings():
    print("🔧 Инициализация настроек подписки")
    print("=" * 60)
    
    # Создаем или получаем настройки
    settings = SubscriptionSettings.get_settings()
    
    print(f"✅ Настройки подписки:")
    print(f"   • Цена: {settings.price} {settings.currency}")
    print(f"   • Длительность: {settings.duration_minutes} минут")
    print(f"   • Статус: {'Активна' if settings.is_active else 'Неактивна'}")
    
    # Синхронизируем с Firebase
    if firebase_service.is_initialized():
        print(f"\n🔥 Синхронизация с Firebase...")
        
        firebase_data = settings.to_firebase_dict()
        success = firebase_service.update_subscription_settings(firebase_data)
        
        if success:
            print(f"✅ Настройки успешно синхронизированы с Firebase!")
            print(f"   Путь в Firebase: /subscription_settings")
            
            # Проверяем, что данные записались
            retrieved_settings = firebase_service.get_subscription_settings()
            if retrieved_settings:
                print(f"\n📋 Данные в Firebase:")
                print(f"   • price: {retrieved_settings.get('price')}")
                print(f"   • duration_minutes: {retrieved_settings.get('duration_minutes')}")
                print(f"   • currency: {retrieved_settings.get('currency')}")
                print(f"   • is_active: {retrieved_settings.get('is_active')}")
            else:
                print(f"⚠️  Не удалось получить данные из Firebase для проверки")
        else:
            print(f"❌ Ошибка синхронизации с Firebase")
    else:
        print(f"⚠️  Firebase не подключен, синхронизация пропущена")
    
    print(f"\n🎯 Unity интеграция:")
    print(f"   • Unity будет получать настройки из Firebase")
    print(f"   • Freedom Pay будет использовать цену: {settings.price} {settings.currency}")
    print(f"   • Таймер будет отсчитывать: {settings.duration_minutes} минут")
    
    print(f"\n📱 Доступ к настройкам:")
    print(f"   • Django админка: http://127.0.0.1:8000/subscription/settings/")
    print(f"   • API endpoint: http://127.0.0.1:8000/subscription/api/settings/")
    
    print(f"\n✨ Инициализация завершена!")

if __name__ == '__main__':
    init_subscription_settings()
