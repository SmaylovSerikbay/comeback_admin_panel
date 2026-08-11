#!/usr/bin/env python
"""
Очистка некорректных данных из Firebase
Удаляет записи с Django-структурой, оставляет только Unity-совместимые
"""

import os
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'comeback_admin.settings')
django.setup()

from firebase_service import firebase_service

def clean_firebase_data():
    print("🧹 Очистка некорректных данных из Firebase")
    print("=" * 60)
    
    # Проверяем подключение к Firebase
    if not firebase_service.is_initialized():
        print("❌ Firebase не подключен!")
        return
    
    print("✅ Firebase подключен, получаем данные...")
    
    # Получаем все объекты из Firebase
    firebase_objects = firebase_service.get_all_video_objects()
    
    if not firebase_objects:
        print("📭 В Firebase нет объектов")
        return
    
    print(f"📦 Найдено {len(firebase_objects)} объектов в Firebase")
    
    valid_count = 0
    invalid_count = 0
    cleaned_count = 0
    
    # Анализируем каждый объект
    for firebase_id, firebase_data in firebase_objects.items():
        print(f"\n🔍 Анализ объекта: {firebase_id}")
        
        # Проверяем структуру Unity (правильная)
        has_unity_structure = all(key in firebase_data for key in ['name', 'objectType', 'x', 'y'])
        
        # Проверяем структуру Django (неправильная)
        has_django_structure = any(key in firebase_data for key in [
            'created_at', 'created_by', 'description', 'title', 'is_active', 'id'
        ])
        
        if has_unity_structure and not has_django_structure:
            print(f"   ✅ Правильная структура Unity")
            print(f"      - name: {firebase_data.get('name')}")
            print(f"      - objectType: {firebase_data.get('objectType')}")
            print(f"      - координаты: {firebase_data.get('x')}, {firebase_data.get('y')}")
            valid_count += 1
            
        elif has_django_structure:
            print(f"   ❌ Неправильная структура Django:")
            for key in ['created_at', 'created_by', 'description', 'title', 'is_active', 'id']:
                if key in firebase_data:
                    print(f"      - {key}: {firebase_data[key]}")
            
            invalid_count += 1
            
            # Спрашиваем пользователя
            while True:
                choice = input(f"   ❓ Удалить этот объект? (y/n): ").lower().strip()
                if choice in ['y', 'yes', 'д', 'да']:
                    try:
                        firebase_service.delete_video_object(firebase_id)
                        print(f"   🗑️  Объект удален")
                        cleaned_count += 1
                    except Exception as e:
                        print(f"   ❌ Ошибка удаления: {str(e)}")
                    break
                elif choice in ['n', 'no', 'н', 'нет']:
                    print(f"   ⏭️  Объект пропущен")
                    break
                else:
                    print("   ❓ Введите y (да) или n (нет)")
        else:
            print(f"   ⚠️  Неопределенная структура")
            print(f"      Ключи: {list(firebase_data.keys())}")
    
    print("\n" + "=" * 60)
    print("🎉 Анализ завершен!")
    print(f"📊 Статистика:")
    print(f"   • Правильных объектов (Unity): {valid_count}")
    print(f"   • Неправильных объектов (Django): {invalid_count}")
    print(f"   • Очищено объектов: {cleaned_count}")
    print(f"   • Всего проанализировано: {len(firebase_objects)}")
    
    if cleaned_count > 0:
        print(f"\n✨ Firebase очищен! Unity приложение будет работать корректно.")
    elif valid_count == len(firebase_objects):
        print(f"\n✨ Firebase уже чист! Все объекты имеют правильную структуру.")
    else:
        print(f"\n⚠️  Остались объекты с неправильной структурой.")

if __name__ == '__main__':
    clean_firebase_data()
