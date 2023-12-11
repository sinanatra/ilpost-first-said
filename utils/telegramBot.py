import os
from telegram import Bot


#os.environ['TELEGRAM_TOKEN']
telegram_bot = Bot(token='os.environ['TELEGRAM_TOKEN']')

async def updateStatus(status, link, title, finalsnippet):
    telegram_channel = '@nuoveparoledelpost'
    telegram_message = f'[{status}]({link})'
    await telegram_bot.send_message(chat_id=telegram_channel, text=telegram_message, disable_web_page_preview=True, parse_mode='MarkdownV2')
