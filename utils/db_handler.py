import psycopg2
import os

class DBHandler:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="test_api_qa", 
            user="postgres", 
            password="1337", 
            host="host.docker.internal", 
            port="5432"
        )
        self.cursor = self.connection.cursor()

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