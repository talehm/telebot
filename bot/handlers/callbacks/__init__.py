
from bot.handlers.callbacks.buyer import start as buyer_start
from bot.handlers.callbacks.seller import new_order_request as seller_new_order_request

def get_handlers():
    callback_queries = [
        buyer_start,
        seller_new_order_request]
    handlers = []
    for query in callback_queries:
        handlers += query.get_handlers()
    return handlers

