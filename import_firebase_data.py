#!/usr/bin/env python
"""
Импорт существующих данных из Firebase в Django
"""

import os
import django
import uuid

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comeback_admin.settings')
django.setup()

from django.contrib.auth.models import User
from video_manager.models import VideoObject
from firebase_service import firebase_service

def import_firebase_data():
    print("🔥 Импорт данных из Firebase в Django Admin Panel")
    print("=" * 60)
    
    # Проверяем подключение к Firebase
    if not firebase_service.is_initialized():
        print("❌ Firebase не подключен!")
        print("   Настройте Firebase ключи в .env файле")
        return
    
    print("✅ Firebase подключен, получаем данные...")
    
    # Получаем данные из Firebase
    firebase_objects = firebase_service.get_all_video_objects()
    
    if not firebase_objects:
        print("📭 В Firebase нет видео объектов")
        return
    
    print(f"📦 Найдено {len(firebase_objects)} объектов в Firebase")
    
    # Получаем или создаем пользователя для импорта
    try:
        import_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("⚠️  Пользователь admin не найден, создаем...")
        import_user = User.objects.create_user(
            username='admin',
            email='admin@comeback.uz',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
    
    imported_count = 0
    updated_count = 0
    
    # Импортируем каждый объект
    for firebase_id, firebase_data in firebase_objects.items():
        try:
            # Извлекаем данные из Firebase
            title = firebase_data.get('name', firebase_data.get('title', f'Импорт {firebase_id[:8]}'))
            latitude = float(firebase_data.get('x', 0))
            longitude = float(firebase_data.get('y', 0))
            video_url = firebase_data.get('objectURL', '')
            object_type = firebase_data.get('objectType', 'video')
            
            # Пропускаем если не видео
            if object_type != 'video':
                continue
                
            print(f"\n📹 Обработка: {title}")
            print(f"   Координаты: {latitude}, {longitude}")
            print(f"   URL: {video_url[:50]}...")
            
            # Проверяем, существует ли уже такое видео
            existing_videos = VideoObject.objects.filter(
                latitude=latitude,
                longitude=longitude,
                video_url=video_url
            )
            
            if existing_videos.exists():
                # Обновляем существующее видео
                video_obj = existing_videos.first()
                video_obj.title = title
                video_obj.is_active = True
                video_obj.save()
                updated_count += 1
                print(f"   ✅ Обновлено существующее видео")
            else:
                # Создаем новое видео
                video_obj = VideoObject.objects.create(
                    title=title,
                    description=f'Импортировано из Firebase (ID: {firebase_id})',
                    latitude=latitude,
                    longitude=longitude,
                    video_url=video_url,
                    created_by=import_user,
                    is_active=True
                )
                imported_count += 1
                print(f"   ✅ Создано новое видео")
            
        except Exception as e:
            print(f"   ❌ Ошибка при обработке {firebase_id}: {str(e)}")
            continue
    
    print("\n" + "=" * 60)
    print("🎉 Импорт завершен!")
    print(f"📈 Статистика:")
    print(f"   • Новых видео создано: {imported_count}")
    print(f"   • Существующих обновлено: {updated_count}")
    print(f"   • Всего обработано: {imported_count + updated_count}")
    
    if imported_count > 0 or updated_count > 0:
        print(f"\n🌐 Теперь видео доступны в Django админке:")
        print(f"   • Войдите как admin/admin123")
        print(f"   • Перейдите в раздел 'Видео'")
        print(f"   • Все импортированные видео будут видны")
    
    print(f"\n🔄 Синхронизация работает в обе стороны:")
    print(f"   • Django → Firebase (при создании/редактировании)")
    print(f"   • Firebase → Unity (в реальном времени)")

if __name__ == '__main__':
    import_firebase_data()
