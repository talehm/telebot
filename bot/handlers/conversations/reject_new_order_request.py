from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler 
from webapp import models
from webapp.database import DBHelper
from telegram import ParseMode
from utils import helpers
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

STATE5 = 1
dbHelper = DBHelper()

def confirm(update, context):
    # text = update.message.text
    query = update.callback_query
    query.edit_message_text("Rejection Sent to Buyer")
    return ConversationHandler.END
    


# Define the states and their corresponding handlers
states = {
    3: [MessageHandler(Filters.text & ~Filters.command, confirm)],    
}
