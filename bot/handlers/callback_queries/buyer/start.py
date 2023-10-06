# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler
from webapp import models
from utils.decorators import save_message, store_user_data
from webapp.database import DBHelper
from bot.handlers import conversations

STATE1, STATE2, STATE3, STATE4, STATE5 = range(5)

class HandleQuery:
    @store_user_data
    def order_product(self, update, context):
        query = update.callback_query
        query.edit_message_text(text = "Please enter the product id:")
        # user_exists = DBHelper().get_one(buyer, chat_id=chat_id)
        return STATE1

    def review_product(self, update, context):
        query = update.callback_query
        query.edit_message_text(text = "Choose a product:")
        return STATE1

def get_handlers():
    # return [CallbackQueryHandler(handle_query)]
    callbacks = ["order_product", "review_product"]
    handler_class = HandleQuery()
    handlers=[]

    for callback in callbacks: 
        entry_points = [CallbackQueryHandler(getattr(handler_class, callback), pattern=callback)]
        states = getattr(conversations, callback).states
        handlers.append(ConversationHandler(entry_points, states, fallbacks=[]))

    return handlers
