from webapp.database import DBHelper
from utils import helpers, constraints, constants
from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CommandHandler,
)
from datetime import timedelta, datetime
from telegram.ext import Updater, CallbackContext
from bot.scheduler import scheduler
import logging
from apscheduler.jobstores.base import JobLookupError
from apscheduler.triggers.cron import CronTrigger
from webapp import models
from flask import current_app, g

trigger = CronTrigger(second="*/10")
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
from flask import current_app, g

# dbHelper = DBHelper()
# app = current_app._get_current_object()


def send_notification(chat_id, context):
    try:
        dbHelper = DBHelper()
        buyer = dbHelper.get_one(models.Buyer, chat_id=chat_id)
        # if buyer:
        #     one_day_ago = timedelta(days=1)
        #     orders = dbHelper.get_many(
        #         models.Order, buyer_id=buyer.id, older_than=one_day_ago
        #     )
        #     message_text = ""
        #     for order in orders:
        #         message_text += f"""Submit review for order id: {order.id}\n\n"""
        #     context.bot.send_message(chat_id=chat_id, text=message_text)
        #     return None
        # context.bot.send_message(chat_id=chat_id, text="Buyer not found.")
    except Exception as e:
        # Roll back the transaction if an error occurs
        # dbHelper.session.rollback()
        logging.error(f"Errordd: {e}")


def start(update, context):
    chat_id = update.message.chat_id
    try:
        scheduler.add_job(
            send_notification,
            args=[chat_id, context],
            trigger=trigger,
            id=str(chat_id),
        )
        context.bot.send_message(chat_id, "Notification has been set successfully.")
    except JobLookupError:
        context.bot.send_message(chat_id, "Notification has already been set.")


def stop(update, context):
    chat_id = update.message.chat_id
    try:
        scheduler.remove_job(str(chat_id))
        context.bot.send_message(chat_id, "Notification has been stopped successfully.")
    except JobLookupError:
        context.bot.send_message(chat_id, "No active notification to stop.")


menu_commands = []


def get_handlers():
    return [
        CommandHandler("setreminder", start, pass_job_queue=True, pass_args=True),
        CommandHandler("stopreminder", stop, pass_job_queue=True, pass_args=True),
    ]
