# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telebot.webapp import models
from telebot.webapp.database import DBHelper


def validate_product_id(update, context):
    text = update.message.text
    if not text.isdigit():
        update.message.reply_text("Please a valid product name (should contain at least one number)")
        return
    else:
        dbHelper = DBHelper()
        product = dbHelper.get_one(models.Product, id=text)
        if not product: 
            update.message.reply_text("This product ID does not exist")
        else:
            update.message.reply_text(product.description)

def validate_product_id_id(update, context):
    text = update.message.text
    if not text.isdigit():
        update.message.reply_text("Please a valid product name (should contain at least one number)")
        return
    else:
        dbHelper=DBHelper()
        product = dbHelper.get_one(models.Product, id=text)
        if not product: 
            update.message.reply_text("This product ID does not exist")
        else:
            update.message.reply_text(product.description)
def get_handlers():
    return [
        MessageHandler(Filters.text & ~Filters.command, validate_product_id_id),
        MessageHandler(Filters.text & ~Filters.command, validate_product_id)
    ]
