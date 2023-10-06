from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler, MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

# Conversation states
STATE1, STATE2 = range(2)

def start(update, context):
    update.message.reply_text("Hi! I'm a conversation bot. Please enter your name.")
    return STATE1

# State 1 handler
def state1_handler(update, context):
    name = update.message.text
    context.user_data['name'] = name

    update.message.reply_text("Great, now enter your age.")
    return STATE2

# State 2 handler
def state2_handler(update, context):
    age = update.message.text
    context.user_data['age'] = age

    # Process the collected data or perform any other actions

    # End the conversation
    update.message.reply_text("Thank you for providing your information.")
    return ConversationHandler.END

def cancel(update, context):
    update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END


def get_handlers():
    # Create the updater and dispatcher
    

    # Create the conversation handler
    return [ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            STATE1: [MessageHandler(Filters.text & ~Filters.command, state1_handler)],
            STATE2: [MessageHandler(Filters.text & ~Filters.command, state2_handler)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )]


