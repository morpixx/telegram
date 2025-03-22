import asyncio
from telethon import TelegramClient

# Замініть на ваші дані
api_id = 27174235         # Наприклад, 123456
api_hash = "93682bb767f2240d31252b764b6bfe9a"
session = 'my_session'

client = TelegramClient(session, api_id, api_hash)

async def main():
    # Отримуємо всі діалоги
    dialogs = await client.get_dialogs()
    for dialog in dialogs:
        print(f"Назва: {dialog.name}, ID: {dialog.id}")

with client:
    client.loop.run_until_complete(main())
