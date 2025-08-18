#!/usr/bin/env python
"""
Скрипт для создания тестовых пользователей
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comeback_admin.settings')
django.setup()

from django.contrib.auth.models import User
from video_manager.models import UserRole

def create_users():
    print("🚀 Создание пользователей для ComeBack Admin Panel...")
    
    # 1. Создание администратора
    try:
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@comeback.uz',
            password='admin123',
            first_name='Администратор',
            last_name='ComeBack',
            is_staff=True,
            is_superuser=True
        )
        
        # Создание роли администратора
        UserRole.objects.create(user=admin_user, role='admin')
        
        print("✅ Администратор создан:")
        print(f"   Логин: admin")
        print(f"   Пароль: admin123")
        print(f"   Email: admin@comeback.uz")
        print(f"   Роль: Администратор")
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            print("⚠️  Администратор уже существует")
            # Обновляем роль если пользователь существует
            try:
                admin_user = User.objects.get(username='admin')
                role, created = UserRole.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})
                if not created:
                    role.role = 'admin'
                    role.save()
                print("✅ Роль администратора обновлена")
            except:
                pass
        else:
            print(f"❌ Ошибка создания администратора: {e}")
    
    # 2. Создание кассира
    try:
        cashier_user = User.objects.create_user(
            username='cashier',
            email='cashier@comeback.uz', 
            password='cashier123',
            first_name='Кассир',
            last_name='ComeBack',
            is_staff=True  # Доступ к админ панели
        )
        
        # Создание роли кассира
        UserRole.objects.create(user=cashier_user, role='cashier')
        
        print("✅ Кассир создан:")
        print(f"   Логин: cashier")
        print(f"   Пароль: cashier123")
        print(f"   Email: cashier@comeback.uz")
        print(f"   Роль: Кассир")
        
    except Exception as e:
        if "UNIQUE constraint failed" in str(e):
            print("⚠️  Кассир уже существует")
            # Обновляем роль если пользователь существует
            try:
                cashier_user = User.objects.get(username='cashier')
                role, created = UserRole.objects.get_or_create(user=cashier_user, defaults={'role': 'cashier'})
                if not created:
                    role.role = 'cashier'
                    role.save()
                print("✅ Роль кассира обновлена")
            except:
                pass
        else:
            print(f"❌ Ошибка создания кассира: {e}")
    
    print("\n🎯 Пользователи готовы к использованию!")
    print("\n📋 Сводка учетных записей:")
    print("=" * 50)
    print("👤 АДМИНИСТРАТОР:")
    print("   Логин: admin")
    print("   Пароль: admin123")
    print("   Возможности:")
    print("   • Добавление/редактирование видео")
    print("   • Управление GPS координатами") 
    print("   • Синхронизация с Firebase")
    print("   • Просмотр детальной статистики")
    print("   • Полный доступ к системе")
    print()
    print("💰 КАССИР:")
    print("   Логин: cashier")
    print("   Пароль: cashier123")
    print("   Возможности:")
    print("   • Просмотр списка платежей")
    print("   • Фильтрация транзакций")
    print("   • Базовая статистика продаж")
    print("   • Мониторинг оплат")
    print()
    print("🌐 Адрес сайта: http://127.0.0.1:8000")
    print("🔧 Админ панель: http://127.0.0.1:8000/admin")

if __name__ == '__main__':
    create_users()
