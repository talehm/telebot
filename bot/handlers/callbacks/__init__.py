from bot.handlers.callbacks.buyer import start as buyer_start
from bot.handlers.callbacks.seller import new_order_request as seller_new_order_request

# from bot.handlers.callbacks.seller import review_request


def get_handlers():
    callbacks = [buyer_start, seller_new_order_request]
    handlers = []
    for query in callbacks:
        handlers += query.get_handlers()
    return handlers


def get_menu():
    callbacks = [buyer_start, seller_new_order_request]
    menus = []
    for callback in callbacks:
        menus.extend(callback.menu_commands)
    return menus
