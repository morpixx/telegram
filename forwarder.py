import asyncio
import json
import re
from pyrogram import Client

async def forward_posts(client, config):
    """
    Функція для пересилання постів за даними з конфігурації як копій (без імені відправника).
    """
    cycle_delay = config.get("cycle_delay", 3600)
    chat_delay = config.get("chat_delay", 5)
    source_posts = config["source_posts"]
    target_chats = config["target_chats"]

    while True:
        for post_url in source_posts:
            # Парсинг URL для отримання username каналу та ID повідомлення.
            # Приклад URL: https://t.me/channel_username/12345
            match = re.search(r't\.me/([^/]+)/(\d+)', post_url)
            if not match:
                print(f"Невірний формат URL: {post_url}")
                continue

            channel_username, message_id = match.group(1), int(match.group(2))

            try:
                # Отримання сутності каналу
                channel = await client.get_chat(channel_username)
            except Exception as e:
                print(f"Помилка при завантаженні поста {post_url}: {e}")
                continue

            # Пересилання поста до кожного цільового чату
            for target in target_chats:
                try:
                    # Отримання сутності цільового чату
                    target_chat = await client.get_chat(target)
                    
                    # Спроба приєднатися до чату (якщо чат публічний, має username)
                    try:
                        if target_chat.username:
                            await client.join_chat(target_chat.username)
                    except Exception:
                        # Якщо не вдалося приєднатися, продовжуємо, оскільки клієнт може вже бути учасником
                        pass

                    # Використовуємо copy_message для пересилання як копії (без імені відправника)
                    await client.copy_message(
                        chat_id=target_chat.id,    # Куди пересилати
                        from_chat_id=channel.id,     # Звідки пересилати
                        message_id=message_id        # ID повідомлення
                    )
                    print(f"Пост {message_id} переслано до {target}")
                except Exception as e:
                    print(f"Помилка при пересиланні поста {message_id} до {target}: {e}")
                await asyncio.sleep(chat_delay)
        print(f"Цикл завершено. Чекаємо {cycle_delay} секунд до наступного циклу...")
        await asyncio.sleep(cycle_delay)

async def main():
    # Завантаження конфігурації
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)

    # Створення клієнта Pyrogram. Ім'я сесії передається як перший позиційний аргумент.
    app = Client(
        config.get("session", "session"),
        api_id=config["api_id"],
        api_hash=config["api_hash"]
    )

    async with app:
        print("Підключення до Telegram успішне!")
        await forward_posts(app, config)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Скрипт зупинено користувачем.")
