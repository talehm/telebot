# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telebot.webapp import models
from telebot.utils.decorators import save_message
from telebot.webapp.database import DBHelper
@save_message
def order_product(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Please enter the product name:")
    context.user_data['next_step'] = 'validate_product_id'

@save_message
def validate_product_id(update, context):
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

    # del context.user_data['next_step']