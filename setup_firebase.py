#!/usr/bin/env python
"""
Автоматическая настройка Firebase для Django Admin Panel
"""

import json
import os
from pathlib import Path

def setup_firebase():
    print("🔥 Настройка Firebase для ComeBack Admin Panel")
    print("=" * 50)
    
    # Проверяем существование .env файла
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ Файл .env не найден!")
        print("   Создайте файл .env скопировав env_example.txt")
        return
    
    print("📋 Для настройки Firebase нужен Service Account ключ")
    print()
    print("🔗 Инструкция по получению ключа:")
    print("1. Откройте: https://console.firebase.google.com/")
    print("2. Выберите проект: comeback-2a6b2")
    print("3. Настройки проекта → Service Accounts")
    print("4. Generate new private key → Скачайте JSON")
    print()
    
    # Спрашиваем путь к JSON файлу
    json_path = input("📁 Укажите путь к скачанному JSON файлу (или перетащите файл сюда): ").strip().strip('"')
    
    if not os.path.exists(json_path):
        print(f"❌ Файл не найден: {json_path}")
        return
    
    try:
        # Читаем JSON файл
        with open(json_path, 'r', encoding='utf-8') as f:
            firebase_config = json.load(f)
        
        # Извлекаем нужные данные
        project_id = firebase_config.get('project_id', '')
        private_key_id = firebase_config.get('private_key_id', '')
        private_key = firebase_config.get('private_key', '').replace('\\n', '\n')
        client_email = firebase_config.get('client_email', '')
        client_id = firebase_config.get('client_id', '')
        client_cert_url = firebase_config.get('client_x509_cert_url', '')
        
        print("✅ JSON файл успешно прочитан")
        print(f"   Project ID: {project_id}")
        print(f"   Client Email: {client_email}")
        
        # Читаем текущий .env файл
        with open('.env', 'r', encoding='utf-8') as f:
            env_content = f.read()
        
        # Обновляем Firebase настройки
        env_lines = env_content.split('\n')
        updated_lines = []
        
        firebase_keys = {
            'FIREBASE_PROJECT_ID': project_id,
            'FIREBASE_PRIVATE_KEY_ID': private_key_id,
            'FIREBASE_PRIVATE_KEY': f'"{private_key}"',
            'FIREBASE_CLIENT_EMAIL': client_email,
            'FIREBASE_CLIENT_ID': client_id,
            'FIREBASE_CLIENT_CERT_URL': client_cert_url,
        }
        
        for line in env_lines:
            updated = False
            for key, value in firebase_keys.items():
                if line.startswith(f'{key}='):
                    updated_lines.append(f'{key}={value}')
                    updated = True
                    break
            
            if not updated:
                updated_lines.append(line)
        
        # Записываем обновленный .env файл
        with open('.env', 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        print("✅ Файл .env успешно обновлен!")
        print()
        print("🚀 Следующие шаги:")
        print("1. Перезапустите Django сервер")
        print("2. Откройте http://127.0.0.1:8000")
        print("3. Проверьте статус Firebase на главной странице")
        print("4. Добавьте первое видео!")
        print()
        print("🎯 Firebase интеграция готова к работе!")
        
    except json.JSONDecodeError:
        print("❌ Ошибка: Неверный формат JSON файла")
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")

if __name__ == '__main__':
    setup_firebase()
