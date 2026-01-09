import psycopg2
import os

class DBHandler:
    def __init__(self):
        # Используем os.getenv, чтобы приоритет был у настроек из CI
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "test_api_qa"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "1337"),
            host=os.getenv("DB_HOST", "host.docker.internal"),
            port=os.getenv("DB_PORT", "5432")
        )
        self.connection = psycopg2.connect(...)
        self.cursor = self.connection.cursor()
        self.setup_db()

    def setup_db(self):
        """Создает необходимые таблицы, если их нет"""
        query = """
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            body TEXT NOT NULL,
            user_id INTEGER
        );
        """
        self.cursor.execute(query)
        self.connection.commit()



    def get_posts_count(self):
        self.cursor.execute("SELECT COUNT(*) FROM posts;")
        count = self.cursor.fetchone()[0]
        return count

    # ВОТ ЭТОТ МЕТОД: Проверь, чтобы он был ВНУТРИ класса!
    def get_post_by_title(self, title):
        """Метод ищет запись в базе по заголовку"""
        query = "SELECT id, title, body FROM posts WHERE title = %s;"
        self.cursor.execute(query, (title,))
        return self.cursor.fetchone() 
    
    def create_post(self, title, body, user_id):
        """Автоматически создает пост в базе"""
        query = "INSERT INTO posts (title, body, user_id) VALUES (%s, %s, %s);"
        self.cursor.execute(query, (title, body, user_id))
        self.connection.commit() # ВАЖНО: коммит сохраняет изменения в базе!

    def delete_post_by_title(self, title):
        """Удаляет пост, чтобы не забивать базу"""
        query = "DELETE FROM posts WHERE title = %s;"
        self.cursor.execute(query, (title,))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()