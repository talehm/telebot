from bot import handlers
from telegram.ext import CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, CommandHandler
from bot.handlers import message_handlers

# Define the states and their corresponding handlers
states = {
    validate_product_id: [MessageHandler(Filters.text & ~Filters.command, validate_product_id)],
    get_paypal_account: [MessageHandler(Filters.text & ~Filters.command, get_paypal_account)]
}

# Generate the states_keys dictionary
states_keys = {state: state.__name__ for state in states}

# Assign the generated values to order_product
order_product.states = states
order_product.states_keys = states_keys