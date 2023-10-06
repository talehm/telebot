from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler 
from webapp import models
from webapp.database import DBHelper
from telegram import ParseMode
from utils import helpers
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

STATE5 = 0
dbHelper = DBHelper()

def confirm(update, context):
    # text = update.message.text
    query = update.callback_query
    update.message.reply_text("Rejection Sent to Buyer")
    return 6
    


# Define the states and their corresponding handlers
states = {
    2: [MessageHandler(Filters.text & ~Filters.command, confirm)],    
}
