# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, ConversationHandler, CommandHandler
from webapp import models, enums
from utils.decorators import save_message, store_user_data
from webapp.database import DBHelper
from bot.handlers import conversations
from telegram import BotCommand, ReplyKeyboardMarkup
from utils import regexp

STATE1, STATE2, STATE3, STATE4, STATE5 = range(5)

dbHelper = DBHelper()


class HandleQuery:
    @store_user_data
    def order_product(self, update, context):
        query = update.callback_query
        print("SDfdsfdsf")
        update.message.reply_text(text="Please enter the product id:")
        # user_exists = DBHelper().get_one(buyer, chat_id=chat_id)
        return STATE1

    @store_user_data
    def review_product(self, update, context):
        query = update.callback_query
        user = dbHelper.get_one(
            model=models.Buyer, chat_id=context.user_data["chat_id"]
        )
        orders = dbHelper.get_many(
            model=models.Order,
            buyer_id=user.id,
            status=[enums.OrderStatus.SS_ACCEPTED, enums.OrderStatus.REVIEW_REJECTED],
        )
        if orders is None:
            update.message.reply_text(text="You have no active orders.")
            return ConversationHandler.END

        options = []  # Your list of options
        context.user_data["orders"] = orders
        for order in orders:
            product = dbHelper.get_one(model=models.Product, id=order.product_id)
            options.append(
                regexp.review_order_list(order.order_id, product.name, regexp=False)
            )  # f"Order id: {order.order_id} \n Product: {product.name}")
        reply_markup = ReplyKeyboardMarkup(
            [[option] for option in options], one_time_keyboard=True
        )
        update.message.reply_text(
            "Please choose one of the following order", reply_markup=reply_markup
        )

        return STATE1


menu_commands = [
    BotCommand("order_product", "Order"),
    BotCommand("review_product", "Review"),
]


def get_handlers():
    # return [CallbackQueryHandler(handle_query)]
    callbacks = ["order_product", "review_product"]
    handler_class = HandleQuery()
    handlers = []

    for callback in callbacks:
        entry_points = [CommandHandler(callback, getattr(handler_class, callback))]
        states = getattr(conversations, callback).states
        handlers.append(ConversationHandler(entry_points, states, fallbacks=[]))

    return handlers
