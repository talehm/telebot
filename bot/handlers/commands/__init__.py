from bot.handlers.commands import start, review_reminder


def get_handlers():
    callbacks = [start, review_reminder]
    handlers = []
    for callback in callbacks:
        handlers += callback.get_handlers()
    return handlers


def get_menu():
    callbacks = [start, review_reminder]
    menus = []
    for callback in callbacks:
        menus.extend(callback.menu_commands)
    return menus
