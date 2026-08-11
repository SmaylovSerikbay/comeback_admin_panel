#!/usr/bin/env python
"""
Скрипт для создания тестовых пользователей (идемпотентный: можно запускать многократно).
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comeback_admin.settings')
django.setup()

from django.contrib.auth.models import User
from video_manager.models import UserRole


def create_users():
    print("🚀 Создание пользователей для ComeBack Admin Panel...")

    # 1. Администратор — get_or_create, без дубликатов
    admin_user, admin_created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@comeback.uz',
            'first_name': 'Администратор',
            'last_name': 'ComeBack',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    admin_user.set_password('admin123')
    admin_user.is_staff = True
    admin_user.is_superuser = True
    admin_user.save()
    role, _ = UserRole.objects.get_or_create(user=admin_user, defaults={'role': 'admin'})
    role.role = 'admin'
    role.save()
    print("✅ Администратор готов:" if admin_created else "⚠️  Администратор уже существовал (пароль обновлён)")
    print("   Логин: admin   Пароль: admin123")

    # 2. Кассир — get_or_create
    cashier_user, cashier_created = User.objects.get_or_create(
        username='cashier',
        defaults={
            'email': 'cashier@comeback.uz',
            'first_name': 'Кассир',
            'last_name': 'ComeBack',
            'is_staff': True,
        }
    )
    cashier_user.set_password('cashier123')
    cashier_user.is_staff = True
    cashier_user.save()
    role2, _ = UserRole.objects.get_or_create(user=cashier_user, defaults={'role': 'cashier'})
    role2.role = 'cashier'
    role2.save()
    print("✅ Кассир готов:" if cashier_created else "⚠️  Кассир уже существовал (пароль обновлён)")
    print("   Логин: cashier   Пароль: cashier123")

    print("\n🎯 Пользователи готовы к использованию!")


if __name__ == '__main__':
    create_users()
