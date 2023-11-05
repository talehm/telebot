from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# from webapp import models, updater
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

# from bot.callbacks import order_product, validate_product_id
from utils import db_utils
from webapp.database import DBHelper
from utils.decorators import save_message
from telegram import BotCommand

db_helper = DBHelper()

STATE1, STATE2, STATE3, STATE4, STATE5 = range(5)


def start(update, context):
    """Handler function for the /start command"""
    # context.user_data["db_helper"] = db_helper

    keyboard = [
        [
            InlineKeyboardButton(
                "\U0001F4EB Order Product", callback_data="order_product"
            ),
            InlineKeyboardButton(
                "\U0001F31F Review Product", callback_data="review_product"
            ),
        ],
        [
            InlineKeyboardButton(
                "\U0001F50D Check Order Status", callback_data="check_order_status"
            ),
            InlineKeyboardButton("\U0001F44E Complaints", callback_data="complaints"),
        ],
        [
            InlineKeyboardButton(
                "\U0001F30F Choose Language", callback_data="choose_language"
            ),
            InlineKeyboardButton(
                "\U000026D4 Cancel Order", callback_data="cancel_order"
            ),
        ],
        [
            InlineKeyboardButton("\U000026A0 Rules", callback_data="rules"),
            InlineKeyboardButton("\U0001F4E3 Help", callback_data="help"),
        ],
    ]
    inline_button = InlineKeyboardButton("Inline Button", callback_data="order_product")

    # menu_commands = BotCommand[{"command": "start", "description": "Show Menu"}]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Please choose an option from menu")
    db_utils.save_user(update)


menu_commands = [BotCommand("start", "Show Menu")]


def get_handlers():
    return [
        CommandHandler("start", start),
    ]
