# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler
from telebot.webapp import models
from telebot.utils.decorators import save_message
from telebot.webapp.database import DBHelper

def order_product(update, context):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Please enter the product name:")
    context.user_data['next_step'] = 'validate_product_id'



def get_handlers():
    return [
        CallbackQueryHandler(order_product, pattern='^order_product$')
    ]