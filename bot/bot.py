from telegram.ext import Updater
from telebot.bot.handlers import setup_handlers

def setup_updater():
    # bot_token = app.config.get('1334466133:AAFozKa4qBUBKQkVIoC-5P6DG5NJ8cC2Y1o')
    updater = Updater('1334466133:AAFozKa4qBUBKQkVIoC-5P6DG5NJ8cC2Y1o')
    WEBHOOK_URL = 'https://711d-79-211-172-249.ngrok-free.app/webhook'
    updater.bot.setWebhook(url=WEBHOOK_URL)
    setup_handlers(updater.dispatcher)
    # updater.start_polling()

    return updater
