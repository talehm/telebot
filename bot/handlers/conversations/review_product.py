from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
)
from webapp import models, enums
from webapp.database import DBHelper
from utils import helpers, constants, regexp
from utils.decorators import save_message

STATE1, STATE2 = range(2)
dbHelper = DBHelper()


def ask_for_review(update, context):
    user_reply = update.message.text
    orders = context.user_data.get("orders", [])
    selected_order = next(
        (
            order
            for order in orders
            if regexp.review_order_list(order.order_number, user_reply)
        ),
        None,
    )
    if selected_order:
        context.user_data["selected_order"] = selected_order
        update.message.reply_text("Please send your review screenshot")
        return STATE2
    return None


def send_order_review_screenshot(update, context):
    order = context.user_data.get("selected_order")
    if not order:
        return ConversationHandler.END

    order = dbHelper.get_one(models.Order, id=order.id)
    if order.status in [
        enums.OrderStatus.ORDERED,
        enums.OrderStatus.SS_ACCEPTED,
        enums.OrderStatus.REVIEW_REJECTED,
    ]:
        path = helpers.save_photo(update, context, constants.REVIEW_SCREENSHOT)
        if path:
            order.review_screenshot = path
            context.user_data["review_screenshot"] = path
            dbHelper.update(order)
            helpers.send_to_seller(update, context, constants.REVIEW_SCREENSHOT)
            update.message.reply_text(
                "Data is sent to the seller. Please stay tuned until confirmation"
            )
            return STATE2

    return ConversationHandler.END


states = {
    STATE1: [
        MessageHandler(Filters.text & ~Filters.command, save_message(ask_for_review))
    ],
    STATE2: [MessageHandler(Filters.photo, save_message(send_order_review_screenshot))],
}
