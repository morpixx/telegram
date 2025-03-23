import asyncio
from pyrogram import Client

# Замініть на ваші дані
api_id = 27174235         # Наприклад, 123456
api_hash = "93682bb767f2240d31252b764b6bfe9a"
session = 'my_session'

client = Client(session, api_id, api_hash)

async def main():
    async for dialog in client.get_dialogs():
        chat = dialog.chat
        # Якщо це група або канал, використовується title,
        # а якщо це приватний чат, використовується ім'я користувача.
        if hasattr(chat, "title") and chat.title:
            name = chat.title
        elif hasattr(chat, "first_name") and chat.first_name:
            name = chat.first_name + (" " + chat.last_name if hasattr(chat, "last_name") and chat.last_name else "")
        else:
            name = "Невідомо"
        print(f"Назва: {name}, ID: {chat.id}")

with client:
    client.loop.run_until_complete(main())
