from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler 
from webapp import models
from webapp.database import DBHelper
from telegram import ParseMode
from utils import helpers
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

STATE5, STATE6 = range(2)
dbHelper = DBHelper()
print(STATE5)
def confirm(update, context):
    # text = update.message.text
    # query = update.callback_query
    update.message.reply_text("Confirmationdbb Sent to Buyer")
    return ConversationHandler.END
   


# Define the states and their corresponding handlers
states = {
    STATE5: [MessageHandler(Filters.text & ~Filters.command, confirm)],
}
