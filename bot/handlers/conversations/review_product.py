from telegram.ext import (
    CallbackQueryHandler,
    ConversationHandler,
    MessageHandler,
    Filters,
    CommandHandler,
)
from webapp import models
from webapp.database import DBHelper
from telegram import ParseMode
from utils import helpers, constraints, constants, regexp
import os
from utils.decorators import save_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
from webapp import enums
import re

STATE1, STATE2, STATE3, STATE4, STATE5, STATE6, STATE7 = range(7)
dbHelper = DBHelper()


def ask_for_review(update, context):
    user_reply = update.message.text
    orders = context.user_data["orders"]
    selected_order = [
        order
        for order in orders
        if regexp.review_order_list(order.order_id, user_reply)
    ][0]
    if selected_order is not None:
        context.user_data["selected_order"] = selected_order
        update.message.reply_text("Please send your review screenshot")
    return STATE2


def send_to_seller(update, context, action=None):
    try:
        #
        order = context.user_data["selected_order"]
        product = dbHelper.get_one(models.Product, id=order.product_id)
        seller = dbHelper.get_one(models.Seller, id=product.seller_id)
        buyer = dbHelper.get_one(models.Buyer, chat_id=context.user_data.get("chat_id"))
        keyboard = []
        if action is constants.REVIEW_SCREENSHOT:
            #
            message = (
                f"🔔 <b>Buyer has sent review screenshot for below order.</b> 🔔\n\n"
                f"{order.order_id}\n"
                f"🆔 {product.id}\n"
                f"📦 Product: {product.description}\n\n"
                f"👤 <b>CUSTOMER DETAILS</b>\n\n"
                f"📨 Paypal: {buyer.paypal}\n"
                f"🔗 Amazon Account : {buyer.amazon_url}\n"
            )

            context.bot.sendMessage(
                chat_id=seller.chat_id, text=message, parse_mode=ParseMode.HTML
            )
            context.bot.send_photo(
                chat_id=seller.chat_id,
                photo=open(buyer.amazon_screenshot, "rb"),
                caption="Review Screenshot",
            )
            keyboard = [
                [
                    InlineKeyboardButton(
                        "✅ Confirm",
                        callback_data=json.dumps(
                            {
                                "action": "confirm_review_screenshot",
                                "order_id": order.id,
                            }
                        ),
                    ),
                    InlineKeyboardButton(
                        "❌ Reject",
                        callback_data=json.dumps(
                            {"action": "reject_review_screenshot", "order_id": order.id}
                        ),
                    ),
                ]
            ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.sendMessage(
            chat_id=seller.chat_id,
            text="Please choose an option:",
            reply_markup=reply_markup,
        )

    except Exception as e:
        update.message.reply_text(
            f"Error occured. Message is not delivered to seller:{e}"
        )


def send_order_review_screenshot(update, context):
    order = context.user_data["selected_order"]
    if (
        order.status is enums.OrderStatus.ORDERED
        or order.status is enums.OrderStatus.REVIEW_REJECTED
    ):
        path = helpers.save_photo(update, context, constants.REVIEW_SCREENSHOT)
        if path is not None:
            order.review_ss = path
            context.user_data["review_screenshot"] = path

            send_to_seller(update, context, constants.REVIEW_SCREENSHOT)
            update.message.reply_text(
                "Data is sent to seller. Please stay tuned until confirmation"
            )
            return STATE2
    return ConversationHandler.END
    # update.message.reply_text("Photo is not saved. Please try again")
    # return STATE7


states = {
    STATE1: [
        MessageHandler(Filters.text & ~Filters.command, save_message(ask_for_review))
    ],
    STATE2: [MessageHandler(Filters.photo, save_message(send_order_review_screenshot))],
}
