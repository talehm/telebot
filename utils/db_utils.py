from datetime import datetime
from telebot.webapp import models
from telebot.webapp.database import DBHelper
from telegram import Update
import json
from telebot.utils.decorators import message_to_json

dbHelper = DBHelper()

@message_to_json
def save_user(update, message):
    chat_id = message["from"]["id"]
    first_name = message["from"]["first_name"]
    last_name = message["from"]["last_name"]
    username = message["from"]["username"]
    language_code = message["from"]["language_code"]

    user = models.Buyer(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        is_active=True,
        is_blocked=False,
        language_code=language_code
    )

    user_exists = dbHelper.get_one(models.Buyer, chat_id=chat_id)
    if user_exists:
        dbHelper.update(user_exists, first_name=first_name, last_name=last_name,username=username, language_code=language_code)
    else:
        dbHelper.add(user)
