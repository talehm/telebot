from telegram.ext import CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telebot.webapp import models 
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
# from telebot.bot.callbacks import order_product, validate_product_id
from telebot.utils import db_utils 
from telebot.utils.decorators import save_message

def start(update, context):
    """Handler function for the /start command"""
    # user_id = update.message.from_user.id
    # username = update.message.from_user.username
    # user = User(user_id=user_id, username=username)
    # db.session.add(user)
    # db.session.commit()
    # update.message.reply_text('Hi there! I have added you to the database.')
    keyboard = [
        [
            InlineKeyboardButton("\U0001F4EB Order Product", callback_data='order_product'),
            InlineKeyboardButton("\U0001F31F Review Product", callback_data='review_product'),
        ],
        [
            InlineKeyboardButton("\U0001F50D Check Order Status", callback_data='check_order_status'),
            InlineKeyboardButton("\U0001F44E Complaints", callback_data='complaints'),
        ],
        [
            InlineKeyboardButton("\U0001F30F Choose Language", callback_data='choose_language'),
            InlineKeyboardButton("\U000026D4 Cancel Order", callback_data='cancel_order'),
        ],
        [
            InlineKeyboardButton("\U000026A0 Rules", callback_data='rules'),
            InlineKeyboardButton("\U0001F4E3 Help", callback_data='help'),
        ],
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)
    db_utils.save_user(update)

def get_handlers():
    return [
        CommandHandler('start', start)
    ]

