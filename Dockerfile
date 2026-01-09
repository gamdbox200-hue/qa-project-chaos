# Используем официальный образ Playwright (в нем уже есть Python и браузеры)
FROM mcr.microsoft.com/playwright/python:v1.57.0-jammy

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект в контейнер
COPY . .

# Команда по умолчанию: запускаем тесты и генерируем отчет
CMD ["pytest", "-v", "tests/test_network_mock.py", "--html=report.html", "--self-contained-html"]