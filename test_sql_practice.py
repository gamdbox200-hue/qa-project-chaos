import psycopg2
import pytest

# Используем данные из db_config.py
from db_config import DB_CONFIG

def test_simple_select():
    """Самый простой тест - проверяем, что можем подключиться к БД"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Запрос 1: Сколько всего записей?
    cursor.execute("SELECT COUNT(*) FROM posts;")
    total = cursor.fetchone()[0]
    print(f"\n📊 Всего записей в таблице posts: {total}")
    assert total > 0, "Таблица posts должна содержать записи"
    
    # Запрос 2: Выводим первые 3 записи
    cursor.execute("SELECT id, title FROM posts ORDER BY id LIMIT 3;")
    rows = cursor.fetchall()
    print("\n📝 Первые 3 записи:")
    for row in rows:
        print(f"  ID {row[0]}: {row[1]}")
    
    cursor.close()
    conn.close()
    print("\n✅ Тест пройден!")

def test_data_quality():
    """Проверяем качество данных"""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Проверка 1: Нет ли пустых заголовков
    cursor.execute("SELECT COUNT(*) FROM posts WHERE title IS NULL OR title = '';")
    empty_titles = cursor.fetchone()[0]
    print(f"\n🔍 Записей с пустым заголовком: {empty_titles}")
    assert empty_titles == 0, "Не должно быть пустых заголовков"
    
    # Проверка 2: Все ли user_id положительные
    cursor.execute("SELECT COUNT(*) FROM posts WHERE user_id <= 0;")
    bad_user_ids = cursor.fetchone()[0]
    print(f"🔍 Записей с некорректным user_id: {bad_user_ids}")
    assert bad_user_ids == 0, "Все user_id должны быть положительными"
    
    cursor.close()
    conn.close()
    print("✅ Проверка качества данных пройдена!")

if __name__ == "__main__":
    # Можно запускать без pytest
    test_simple_select()
    test_data_quality()