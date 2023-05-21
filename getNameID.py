# name and chat ID

import asyncio
from telethon import TelegramClient

# Replace the values below with your own Telegram API credentials
api_id = "ENTER API_ID"
api_hash = 'ENTER API_HAS'
phone_number = 'ENTER YOUR PHONE NUMBER'

async def get_dialogs():
    # Create a new TelegramClient instance
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter the code: '))

    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        print(f'{dialog.title} (ID: {dialog.id})')

    await client.disconnect()

asyncio.run(get_dialogs())
