from bot.handlers.commands import start, review_reminder


def get_handlers():
    callback_queries = [start, review_reminder]
    handlers = []
    for query in callback_queries:
        handlers += query.get_handlers()
    return handlers
