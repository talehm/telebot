import json
from datetime import datetime
from functools import wraps
from telegram import Update
from telebot.webapp import models
from telebot.webapp.database import DBHelper
#  convert to JSON
def message_to_json(func):
    def wrapper(update: Update, *args, **kwargs):
        message = update.message
        if not message:
            message=update.callback_query.message
        message_dict = message.to_dict()
        message_json = json.loads(json.dumps(message_dict))
        return func(update, message_json, *args, **kwargs)
    return wrapper


# save messages of users automatically
def save_message(func):
    @wraps(func)
    @message_to_json
    def wrapper(update, message, context):
        print("message_saved")
        chat_id = message["chat"]["id"]
        message_id = message["message_id"]
        text = message["text"]
        created_at = datetime.now()
        dbHelper = DBHelper()

        # Save message to database
        message_model = models.Message(
            message_id=message_id,
            chat_id=chat_id,
            text=text,
            created_at=created_at
        )
        dbHelper.add(message_model)

        # Call the original function
        return func(update, context)
    return wrapper

