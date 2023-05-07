from telebot.bot.handlers import callback_query_handlers, command_handlers, message_handlers
from telebot.utils.decorators import save_message
from telegram.ext import  CommandHandler, MessageHandler, CallbackQueryHandler

## CUSTOM HANDLERS TO SAVE MESSAGES AUTOMATICALLY


def save_message_decorator_all_handlers(handler):
    if isinstance(handler, CommandHandler):
        return SaveMessageCommandHandler(handler.command, handler.callback)
    elif isinstance(handler, MessageHandler):
        return SaveMessageMessageHandler(handler.filters, handler.callback)
    elif isinstance(handler, CallbackQueryHandler):
        return SaveMessageCallbackQueryHandler(handler.pattern, handler.callback)
    else:
        return handler

class SaveMessageCommandHandler(CommandHandler):
    def __init__(self, command, callback):
        super().__init__(command, save_message(callback))

class SaveMessageMessageHandler(MessageHandler):
    def __init__(self, filters, callback):
        super().__init__(filters, save_message(callback))

class SaveMessageCallbackQueryHandler(CallbackQueryHandler):
    def __init__(self, pattern, callback):
        super().__init__(save_message(callback), pattern)

def add_save_message_decorator(dp):
    # Add the decorator to all MessageHandlers
    for index, value in enumerate(dp.handlers[0]):
            decorated_handler = save_message_decorator_all_handlers(value)
            dp.handlers[0][index]=decorated_handler
           
    
def setup_handlers(dp):
    # get handlers
    handler_types = [message_handlers, command_handlers, callback_query_handlers]

    for handler_type in handler_types:
        for handler in handler_type.get_handlers():
            # add handlers
            dp.add_handler(handler)
    # create custom handler
    add_save_message_decorator(dp)
