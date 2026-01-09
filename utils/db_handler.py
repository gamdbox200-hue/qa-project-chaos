import psycopg2
import os

class DBHandler:
    def __init__(self):
        # Подключаемся, используя переменные окружения или значения по умолчанию
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME", "test_api_qa"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "1337"),
            host=os.getenv("DB_HOST", "host.docker.internal"),
            port=os.getenv("DB_PORT", "5432")
        )
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

    def create_post(self, title, body, user_id):
        query = "INSERT INTO posts (title, body, user_id) VALUES (%s, %s, %s);"
        self.cursor.execute(query, (title, body, user_id))
        self.connection.commit()

    def delete_post_by_title(self, title):
        query = "DELETE FROM posts WHERE title = %s;"
        self.cursor.execute(query, (title,))
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()