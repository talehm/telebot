from bot.handlers import commands, callbacks
from utils.decorators import save_message
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

## CUSTOM HANDLERS TO SAVE MESSAGES AUTOMATICALLY


def get_custom_handler(handler):
    if isinstance(handler, CommandHandler):
        return CustomCommandHandler(handler.command, handler.callback)
    elif isinstance(handler, MessageHandler):
        return CustomMessageHandler(handler.filters, handler.callback)
    elif isinstance(handler, CallbackQueryHandler):
        return CustomCallbackQueryHandler(handler.pattern, handler.callback)
    elif isinstance(handler, ConversationHandler):
        return CustomConversationHandler(
            handler.entry_points, handler.states, handler.fallbacks
        )
    else:
        return handler


class CustomCommandHandler(CommandHandler):
    def __init__(self, command, callback):
        super().__init__(command, save_message(callback))


class CustomMessageHandler(MessageHandler):
    def __init__(self, filters, callback):
        super().__init__(filters, save_message(callback))


class CustomCallbackQueryHandler(CallbackQueryHandler):
    def __init__(self, pattern, callback):
        super().__init__(save_message(callback), pattern)


class CustomConversationHandler(ConversationHandler):
    def __init__(self, entry_points, states, fallbacks):
        super().__init__(entry_points, states, fallbacks)


def add_save_message_decorator(dp):
    # Add the decorator to all MessageHandlers
    for index, value in enumerate(dp.handlers[0]):
        decorated_handler = get_custom_handler(value)
        dp.handlers[0][index] = decorated_handler


def init(updater):
    # get handlers
    handler_types = [commands, callbacks]
    dp = updater.dispatcher
    menu_commands = []
    for handler_type in handler_types:
        for handler in handler_type.get_handlers():
            dp.add_handler(handler)
        menu_commands.extend(handler_type.get_menu())
    # updater.set)
    updater.bot.set_my_commands(menu_commands)
    add_save_message_decorator(dp)
