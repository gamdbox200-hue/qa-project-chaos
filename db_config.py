# Конфигурация для подключения к PostgreSQL
DB_CONFIG = {
    "host": "localhost",
    "database": "test_api_qa",
    "user": "postgres",
    "password": "1337",  # Замени на свой!
    "port": 5432
}

# Функция для проверки подключения
def test_connection():
    try:
        import psycopg2
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(f"✅ Подключение успешно! Версия PostgreSQL: {db_version[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM posts;")
        count = cursor.fetchone()[0]
        print(f"✅ В таблице 'posts' записей: {count}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        print("\nВозможные причины:")
        print("1. PostgreSQL не запущен (проверь в services.msc)")
        print("2. Неверный пароль в DB_CONFIG")
        print("3. База данных 'test_api_qa' не существует")
        return False

if __name__ == "__main__":
    test_connection()