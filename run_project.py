import os
import subprocess

def run_cmd(cmd):
    # Заменяем {pwd} на реальный путь текущей папки
    current_path = os.getcwd()
    # В Windows для Docker пути должны быть без обратных слешей в некоторых случаях, 
    # но os.getcwd() обычно справляется.
    cmd = cmd.replace("${PWD}", current_path)
    
    print(f"🚀 Выполняю: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка при выполнении: {e}")
    except KeyboardInterrupt:
        print("\n⏹ Выполнение прервано пользователем")

def menu():
    print("\n" + "="*30)
    print("🛠 QA Project Control Panel")
    print("="*30)
    print("1. Полная пересборка Docker (build)")
    print("2. Запустить ВСЕ тесты")
    print("3. Запустить только тесты API")
    print("4. Открыть отчет Allure")
    print("5. Выход")
    
    choice = input("\nВыбери действие: ")
    
    if choice == '1':
        run_cmd("docker build -t qa-project-chaos .")
    elif choice == '2':
        # Используем кавычки вокруг пути на случай пробелов в именах папок
        run_cmd('docker run --rm -v "${PWD}:/app" -e PYTHONPATH=/app -w /app qa-project-chaos pytest tests/ --alluredir=allure-results --clean-alluredir')
    elif choice == '3':
        run_cmd('docker run --rm -v "${PWD}:/app" -e PYTHONPATH=/app -w /app qa-project-chaos pytest tests/test_api_db.py --alluredir=allure-results')
    elif choice == '4':
        print("💡 Нажми Ctrl+C в консоли, когда закончишь смотреть отчет, чтобы вернуться в меню.")
        run_cmd("allure serve allure-results")
    elif choice == '5':
        print("Пока! 👋")
        exit()

if __name__ == "__main__":
    while True:  # Этот цикл заставит меню появляться снова и снова
        try:
            menu()
        except KeyboardInterrupt:
            # Если нажал Ctrl+C внутри меню, а не внутри отчета
            print("\n👋 Выход из панели управления...")
            break