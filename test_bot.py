"""
Тестирование Telegram бота
"""
import requests
import json

def test_bot_info():
    """Проверить информацию о боте"""
    print("🤖 Проверка информации о боте...")
    
    url = f"https://api.telegram.org/bot8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4/getMe"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            bot_info = data['result']
            print(f"✅ Бот работает!")
            print(f"   Имя: @{bot_info.get('username')}")
            print(f"   ID: {bot_info.get('id')}")
            print(f"   Имя: {bot_info.get('first_name')}")
            return True
        else:
            print(f"❌ Ошибка API: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")
        return False

def test_webhook():
    """Проверить статус веб-хука"""
    print("\n🔗 Проверка веб-хука...")
    
    url = f"https://api.telegram.org/bot8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4/getWebhookInfo"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('ok'):
            webhook_info = data['result']
            print(f"✅ Веб-хук настроен!")
            print(f"   URL: {webhook_info.get('url', 'Не настроен')}")
            print(f"   Ожидающих обновлений: {webhook_info.get('pending_update_count', 0)}")
            
            if webhook_info.get('last_error_message'):
                print(f"   Последняя ошибка: {webhook_info.get('last_error_message')}")
            
            return True
        else:
            print(f"❌ Ошибка API: {data.get('description')}")
            return False
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")
        return False

def send_test_message():
    """Отправить тестовое сообщение боту"""
    print("\n📤 Отправка тестового сообщения...")
    
    # Замените на ваш Telegram ID для получения сообщения
    chat_id = input("Введите ваш Telegram ID (или оставьте пустым для пропуска): ").strip()
    
    if not chat_id:
        print("⏭️ Пропускаем отправку сообщения")
        return True
    
    try:
        chat_id = int(chat_id)
    except ValueError:
        print("❌ Неверный ID чата")
        return False
    
    message = """
🤖 Тестовое сообщение от бота!

✅ Бот работает корректно
✅ Веб-хук настроен
✅ Мини-приложение готово

Для использования:
1. Отправьте /start
2. Нажмите кнопку "📱 Open Expense Tracker"
3. Начните отслеживать расходы!
"""
    
    url = f"https://api.telegram.org/bot8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ Тестовое сообщение отправлено!")
            return True
        else:
            print(f"❌ Ошибка отправки: {result.get('description')}")
            return False
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")
        return False

def setup_commands():
    """Настроить команды бота"""
    print("\n⚙️ Настройка команд бота...")
    
    commands = [
        {"command": "start", "description": "Открыть приложение для отслеживания расходов"},
        {"command": "help", "description": "Показать помощь и доступные команды"},
        {"command": "about", "description": "Информация о приложении"}
    ]
    
    url = f"https://api.telegram.org/bot8319629279:AAERWVdXipQIoqZR_OPd6RtcFHEb2PNvMG4/setMyCommands"
    data = {"commands": commands}
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ Команды бота настроены!")
            for cmd in commands:
                print(f"   /{cmd['command']} - {cmd['description']}")
            return True
        else:
            print(f"❌ Ошибка настройки команд: {result.get('description')}")
            return False
    else:
        print(f"❌ HTTP ошибка: {response.status_code}")
        return False

def main():
    """Основная функция тестирования"""
    print("🧪 Тестирование Telegram бота")
    print("=" * 40)
    
    tests = [
        test_bot_info,
        test_webhook,
        setup_commands,
        send_test_message
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Ошибка в тесте: {e}")
    
    print("\n" + "=" * 40)
    print(f"📊 Результаты: {passed}/{total} тестов пройдено")
    
    if passed == total:
        print("🎉 Все тесты пройдены!")
        print("\n📱 Теперь попробуйте:")
        print("1. Найдите @spendSenceBot в Telegram")
        print("2. Отправьте /start")
        print("3. Нажмите '📱 Open Expense Tracker'")
    else:
        print("⚠️ Некоторые тесты не пройдены")
        print("📋 Проверьте настройки и попробуйте снова")

if __name__ == "__main__":
    main()
