# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CommandHandler,
)
from webapp import models
from utils.decorators import save_message, store_user_data
from webapp.database import DBHelper
from bot.handlers import conversations
from webapp.enums import OrderStatus
import json
from telegram import ParseMode
from telegram import BotCommand

(
    STATE1,
    STATE2,
    STATE3,
    STATE4,
    STATE5,
    STATE6,
    STATE7,
    STATE8,
    STATE9,
    STATE10,
    STATE11,
    STATE12,
) = range(12)
dbHelper = DBHelper()


class HandleQuery:
    def confirm_new_order_request(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id=order_id)
            order.status = OrderStatus.WAITING_SS
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id=order.buyer_id)
            product = dbHelper.get_one(models.Product, id=order.product_id)
            text = (
                f"*Your Order Request is CONFIRMED for the product below*\n\n"
                f"🆔 {product.id}\n"
                f"📦 Product: {product.description}\n\n"
                f"{product.url}\n\n\n"
                f"*Please purchase the product and send the order screenshot*"
            )

            context.user_data["buyer_chat_id"] = buyer.chat_id
            context.bot.sendMessage(
                chat_id=buyer.chat_id, text=text, parse_mode=ParseMode.HTML
            )
            update.callback_query.message.reply_text(
                "Order Confirmation is sent to buyer"
            )
            ConversationHandler.END
        except Exception as e:
            print(str(e))

    def reject_new_order_request(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id=order_id)
            order.status = OrderStatus.REJECTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id=order.buyer_id)
            product = dbHelper.get_one(models.Product, id=order.product_id)
            text = (
                f"*Your Order Request is REJECTED for the product below*\n\n"
                f"🆔 {product.id}\n"
                f"📦 Product: {product.description}\n\n"
                f"{product.url}\n\n\n"
            )

            context.bot.sendMessage(
                chat_id=buyer.chat_id, text=text, parse_mode=ParseMode.HTML
            )
            update.callback_query.message.reply_text("Order Rejection is sent to buyer")
            ConversationHandler.END
        except Exception as e:
            print(str(e))

    def accept_order_screenshot(self, update, context, order_id):
        try:
            #
            order = dbHelper.get_one(models.Order, id=order_id)
            order.status = OrderStatus.SS_ACCEPTED
            dbHelper.update(order)
            #
            buyer = dbHelper.get_one(models.Buyer, id=order.buyer_id)
            product = dbHelper.get_one(models.Product, id=order.product_id).order()
            dbHelper.update(product)

            text = (
                f"*The screenshot is Accepted by the seller*\n\n"
                f"Please submit review after a week\n"
                f"Send us the link and screenshot of review after it is published\n\n"
            )

            context.bot.sendMessage(
                chat_id=buyer.chat_id, text=text, parse_mode=ParseMode.HTML
            )
            update.callback_query.message.reply_text("Confirmation is sent to buyer")
            # ConversationHandler.END
            return STATE6
        except Exception as e:
            print(str(e))

    def decline_order_screenshot(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id=order_id)
            order.status = OrderStatus.SS_REJECTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id=order.buyer_id)
            text = (
                f"*The screenshot is Declined by the seller*\n\n" f"Please try again\n"
            )

            context.bot.sendMessage(
                chat_id=buyer.chat_id, text=text, parse_mode=ParseMode.HTML
            )
            update.callback_query.message.reply_text("The buyer is asked to try again.")
            return STATE7
        except Exception as e:
            print(str(e))

    def confirm_review_screenshot(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id=order_id)
            order.status = OrderStatus.REVIEW_ACCEPTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id=order.buyer_id)
            product = dbHelper.get_one(models.Product, id=order.product_id)
            text = (
                f"*Your Review is CONFIRMED for the order number {order.order_id}*\n\n"
                f"*Please wait for paypal refund in next 5 days*"
            )

            context.user_data["buyer_chat_id"] = buyer.chat_id
            context.bot.sendMessage(
                chat_id=buyer.chat_id, text=text, parse_mode=ParseMode.HTML
            )
            update.callback_query.message.reply_text(
                "Order Confirmation is sent to buyer"
            )
            ConversationHandler.END
        except Exception as e:
            print(str(e))

    def reject_review_screenshot(self, update, context, order_id):
        try:
            order = dbHelper.get_one(models.Order, id=order_id)
            order.status = OrderStatus.REVIEW_REJECTED
            dbHelper.update(order)
            buyer = dbHelper.get_one(models.Buyer, id=order.buyer_id)
            text = (
                f"*The review screenshot is Declined by the seller*\n\n"
                f"Please try again\n"
            )

            context.bot.sendMessage(
                chat_id=buyer.chat_id, text=text, parse_mode=ParseMode.HTML
            )
            update.callback_query.message.reply_text("The buyer is asked to try again.")
            return STATE1

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


menu_commands = []


def get_handlers():
    callbacks = [
        "decline_order_screenshot",
        "confirm_new_order_request",
        "reject_new_order_request",
        "confirm_review_screenshot",
        "reject_review_screenshot",
    ]
    queries = ["accept_order_screenshot"]
    handlers = []

    for callback in callbacks:
        entry_points = [CallbackQueryHandler(callback_function)]
        states = getattr(conversations, callback).states
        handlers.append(ConversationHandler(entry_points, states, fallbacks=[]))
    for query in queries:
        handlers.append(CallbackQueryHandler(callback_function, pattern=f"^{query}"))
    return handlers
