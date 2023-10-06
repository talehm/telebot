# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler
from webapp import models
from utils.decorators import save_message, store_user_data
from webapp.database import DBHelper
from bot.handlers import conversations
from webapp.enums import OrderStatus
import json
from telegram import ParseMode

STATE5, STATE6, STATE7,STATE8,STATE9,STATE10,STATE11,STATE12, = range(8)
dbHelper = DBHelper()

class HandleQuery:
    def confirm_new_order_request(self, update, context, order_id):
        # user_exists = DBHelper().get_one(buyer, chat_id=chat_id)
        # print(update)
        try:
            order = dbHelper.get_one(models.Order, id = order_id)
            order.status = OrderStatus.WAITING_SS
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id = order.buyer_id)
            product = dbHelper.get_one(models.Product, id = order.product_id)
            text = f"*Your Order Request is CONFIRMED for the product below*\n\n"\
            f"🆔 {product.id}\n"\
            f"📦 Product: {product.description}\n\n"\
            f"{product.url}\n\n\n"\
            f"*Please purchase the product and send the order screenshot*"

            context.user_data['buyer_chat_id'] = buyer.chat_id
            context.bot.sendMessage(chat_id = buyer.chat_id, text = text, parse_mode = ParseMode.HTML)
            update.callback_query.message.reply_text("Order Confirmation is sent to buyer")
            print(STATE5)
            # return STATE5
            ConversationHandler.END
        except Exception as e:
            print(str(e))

    def reject_new_order_request(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id = order_id)
            order.status = OrderStatus.REJECTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id = order.buyer_id)
            product = dbHelper.get_one(models.Product, id = order.product_id)
            text = f"*Your Order Request is REJECTED for the product below*\n\n"\
            f"🆔 {product.id}\n"\
            f"📦 Product: {product.description}\n\n"\
            f"{product.url}\n\n\n"
            
            context.bot.sendMessage(chat_id = buyer.chat_id, text = text, parse_mode = ParseMode.HTML)
            update.callback_query.message.reply_text("Order Rejection is sent to buyer")
            ConversationHandler.END
        except Exception as e:
            print(str(e))

    def accept_order_screenshot(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id = order_id)
            order.status = OrderStatus.REJECTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id = order.buyer_id)
            product = dbHelper.get_one(models.Product, id = order.product_id)
            text = f"*The screenshot is Accepted by the seller*\n\n"\
            f"Please submit review after a week\n"\
            f"Send us the link and screenshot of review after it is published\n\n"
            
            context.bot.sendMessage(chat_id = buyer.chat_id, text = text, parse_mode = ParseMode.HTML)
            update.callback_query.message.reply_text("Confirmation is sent to buyer")
            # ConversationHandler.END
            return STATE6
        except Exception as e:
            print(str(e))

    def decline_order_screenshot(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id = order_id)
            order.status = OrderStatus.SS_REJECTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id = order.buyer_id)
            text = f"*The screenshot is Declined by the seller*\n\n"\
            f"Please try again\n"
            
            context.bot.sendMessage(chat_id = buyer.chat_id, text = text, parse_mode = ParseMode.HTML)
            update.callback_query.message.reply_text("The buyer is asked to try again.")
            print(update)
            # if "decline" in update.callback_query.data["action"]:
            # # ConversationHandler.END 
            #     print(STATE5)
            return STATE7
            # else:
            #     return ConversationHandler.END
        except Exception as e:
            print(str(e))

def callback_function(update, context):
    query = update.callback_query
    callback_data = query.data
    try:
        data = json.loads(callback_data)
    except Exception as e:
        data = query.data
    handler_class = HandleQuery()
    return getattr(handler_class, data["action"])(update, context, data["order_id"])


    # Rest of your code

def get_handlers():
    callbacks = ["decline_order_screenshot","confirm_new_order_request","reject_new_order_request" ]
    queries = ["accept_order_screenshot"]
    handlers = []

    for callback in callbacks: 
        entry_points = [CallbackQueryHandler(callback_function)]
        states = getattr(conversations, callback).states
        handlers.append(ConversationHandler(entry_points, states, fallbacks=[]))
    for query in queries:
        handlers.append(CallbackQueryHandler(callback_function, pattern=f"^{query}"))
    return handlers
