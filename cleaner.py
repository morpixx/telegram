import asyncio
from pyrogram import Client, filters

# Ініціалізація клієнта з використанням існуючої сесії
# Переконайтеся, що файл сесії (наприклад, my_session.session) знаходиться в тій же директорії, що й скрипт,
# або вкажіть повний шлях до нього.
app = Client("my_session")

@app.on_message(filters.command("clean_all") & filters.me & filters.group)
async def clean_system_messages(client: Client, message):
    """
    Видаляє системні повідомлення в групі за командою /clean_all.
    """
    chat_id = message.chat.id
    deleted_count = 0
    messages_to_delete = []

    await message.reply_text("Починаю пошук та видалення системних повідомлень...")

    try:
        # Ітерація по історії чату
        async for msg in client.get_chat_history(chat_id):
            # Перевірка, чи є повідомлення системним (перевіряємо, чи атрибут .service не є None)
            if msg.service is not None:
                messages_to_delete.append(msg.id)
                # Видаляємо повідомлення партіями по 100 (Pyrogram робить це автоматично при передачі списку ID)
                if len(messages_to_delete) >= 100:
                    await client.delete_messages(chat_id, messages_to_delete)
                    deleted_count += len(messages_to_delete)
                    print(f"Видалено {deleted_count} системних повідомлень...")
                    messages_to_delete = []

        # Видалення залишків повідомлень, якщо їх менше 100
        if messages_to_delete:
            await client.delete_messages(chat_id, messages_to_delete)
            deleted_count += len(messages_to_delete)

        await message.reply_text(f"Завершено. Видалено всього {deleted_count} системних повідомлень.")

    except Exception as e:
        await message.reply_text(f"Виникла помилка: {e}")
        print(f"Помилка: {e}")

# Запуск клієнта
print("Клієнт запущено. Очікую команду /clean_all...")
app.run()