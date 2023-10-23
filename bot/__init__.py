from telegram.ext import Updater
from bot import handlers, reminders, scheduler
def setup_updater():
    # bot_token = app.config.get('1334466133:AAFozKa4qBUBKQkVIoC-5P6DG5NJ8cC2Y1o')
    updater = Updater('1334466133:AAGpj2HZ7kyxaBRzl4JtnRElVcaedvCdF18',use_context=True)
    WEBHOOK_URL = 'https://2ece-79-211-172-183.ngrok-free.app/webhook'
    updater.bot.setWebhook(url=WEBHOOK_URL)
    # updater.start_polling()
    # job_queue = updater.job_queue

    return updater

def init(dp):
    handlers.init(dp)
    reminders.init(dp)
