from bot.handlers.callback_queries.buyer import start as buyer_start
from bot.handlers.callback_queries.seller import new_order_request as seller_new_order_request

def get_handlers():
    
    callback_queries = [buyer_start, seller_new_order_request]
    handlers = []
    for query in callback_queries:
        handlers += query.get_handlers()
    return handlers