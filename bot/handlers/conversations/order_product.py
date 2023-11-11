from telegram.ext import (
    ConversationHandler,
    MessageHandler,
    Filters,
)
from webapp import models
from webapp.database import DBHelper
from telegram import ParseMode
from utils import helpers, constraints, constants
from utils.decorators import save_message
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json, re
from webapp import enums

STATE1, STATE2, STATE3, STATE4, STATE5, STATE6, STATE7, STATE8 = range(8)
dbHelper = DBHelper()


def is_buyer_data_expired(context):
    chat_id = context.user_data.get("chat_id")
    buyer = dbHelper.get_one(models.Buyer, chat_id=chat_id)
    return helpers.is_older_than(
        buyer.updated_at, weeks=constraints.BUYER_DATA_EXPIRATION
    )


def has_buyer_profile_screenshot(context):
    chat_id = context.user_data.get("chat_id")
    buyer = dbHelper.get_one(models.Buyer, chat_id=chat_id)
    return buyer.amazon_screenshot is not None and buyer.amazon_screenshot != ""


def save_buyer_info(update, context, column, text=None):
    try:
        chat_id = context.user_data.get("chat_id")
        if not chat_id:
            update.message.reply_text(
                "Chat ID not found. Please start the conversation again."
            )
            return

        buyer = dbHelper.get_one(models.Buyer, chat_id=chat_id)
        if not buyer:
            update.message.reply_text(
                "Buyer not found. Please start the conversation again."
            )
            return

        if not text:
            text = update.message.text
            # update.message.reply_text("Text value not provided. Please enter a valid value.")
            # return

        setattr(buyer, column, text)
        dbHelper.update(buyer)
        return True

    except Exception as e:
        print(f"Error updating buyer information: {e}")
        return False


def validate_product_id(update, context):
    text = update.message.text
    if not text.isdigit():
        update.message.reply_text(
            "Please choose a valid product name (should contain at least one number)"
        )
        return
    else:
        product = dbHelper.get_one(models.Product, id=text)
        if not product:
            update.message.reply_text("This product ID does not exist")
        else:
            context.user_data["chosen_product"] = product
            photo_url = product.image_url
            product_info = (
                f"✅*Product is Available*✅\n\n"
                f"*Chosen Product*: {product.description}\n"
                f"{'✅ *FULL REFUND*' if product.properties['refund']['isFullRefund'] == True else '✅ *Refund: ' + str(product.properties['refund']['amount'])+'*'}\n"
                f"{'✅ *Paypal Fee Included*' if product.properties['paypal']['isPaypalFeeIncluded'] == True else 'Paypal Fee Not Included'}\n"
                f"💰 *Price: {product.price}* 💰\n\n"
                f"{product.url}\n\n\n"
            )
            # photo_file = BytesIO(requests.get(photo_url).content)
            isExpired = is_buyer_data_expired(context)
            has_amazon_ss = has_buyer_profile_screenshot(context)
            buyer = dbHelper.get_one(
                models.Buyer, chat_id=context.user_data.get("chat_id")
            )
            order = dbHelper.get_one(
                models.Order, product_id=product.id, buyer_id=buyer.id
            )
            if order is not None:
                update.message.reply_text(
                    f"You have already proceeded with this order. Status: {order.status}"
                )
                return ConversationHandler.END
            if (
                product.count <= 0
                or product.status == enums.ProductStatus.DISCONTINUED
                or product.status == enums.ProductStatus.SOLD_OUT
            ):
                update.message.reply_text(
                    f"This product is not available anymore. Status: {product.status}"
                )
                return ConversationHandler.END
            if isExpired:
                update.message.reply_text(
                    "*Next Step: Please send your paypal account.*"
                )
                context.user_data["next_step"] = "get_paypal_account"
                return STATE2
            elif has_amazon_ss is False:
                update.message.reply_text(
                    "*Next Step: Please send your screenshot of amazon profile.*"
                )
                context.user_data["next_step"] = "get_amazon_account_screenshot"
                return STATE4
            else:
                update.message.reply_photo(photo=photo_url, caption=product_info)
                update.message.reply_text("*Your order request is sent to the agent*")
                helpers.send_to_seller(update, context, constants.NEW_ORDER_REQUEST)
                return STATE6


def get_paypal_account(update, context):
    text = update.message.text
    if not helpers.is_valid_email(text):
        update.message.reply_text("Email format is not correct. Please try again")
    else:
        isSaved = save_buyer_info(update, context, "paypal")
        if isSaved:
            context.user_data["paypal"] = text
            update.message.reply_text("Please send amazon account link")
            return STATE3
        else:
            update.message.reply_text("Error occured. Please send again.")
            return


def get_amazon_account_link(update, context):
    text = update.message.text
    if not helpers.is_valid_url(text):
        update.message.reply_text("URL format is not correct. Please try again")
    else:
        isSaved = save_buyer_info(update, context, "amazon_url")
        if isSaved:
            context.user_data["amazon_url"] = text
            update.message.reply_text("Please send screenshot of amazon public profile")
            return STATE4
        update.message.reply_text("Error occured. Please send again.")
        return


def get_amazon_account_screenshot(update, context):
    path = helpers.save_photo(update, context, constants.ACCOUNT_SCREENSHOT)
    if path:
        isSaved = save_buyer_info(update, context, "amazon_screenshot", path)
        if isSaved:
            context.user_data["amazon_screenshot"] = path
            helpers.send_to_seller(update, context, constants.NEW_ORDER_REQUEST)
            update.message.reply_text(
                "Data is sent to seller. Please stay tuned until confirmation"
            )
            return ConversationHandler.END
    update.message.reply_text("Photo is not saved. Please try again")
    return


def send_order_number_to_seller(update, context):
    print(context.user_data)
    order_number = update.message.text
    print(order_number)
    if order_number is not None and helpers.validate_order_number(order_number):
        order = dbHelper.get_one(models.Order, id=context.user_data["order_id"])
        order.order_number = order_number
        dbHelper.update(order)
        update.message.reply_text("Please Send order screenshot")
        return STATE7
    else:
        update.message.reply_text(
            "Validation error. Please try again. Ex: 123-1234567-1234567"
        )
        return STATE6


def send_order_screenshot_to_seller(update, context):
    order = dbHelper.get_one(models.Order, id=context.user_data["order_id"])
    if (
        order.status is enums.OrderStatus.SS_REJECTED
        or order.status is enums.OrderStatus.WAITING_SS
    ):
        path = helpers.save_photo(update, context, constants.ORDER_SCREENSHOT)
        if path:
            # isSaved = save_buyer_info(update, context, "amazon_order_screenshot", path)
            order.order_screenshot = path
            dbHelper.update(order)
            #
            context.user_data["amazon_order_screenshot"] = path
            helpers.send_to_seller(update, context, constants.ORDER_SCREENSHOT)
            update.message.reply_text(
                "Screenshot is sent to seller. Please stay tuned until confirmation"
            )
            return STATE7
    else:
        return STATE8
    update.message.reply_text("Photo is not saved. Please try again")
    return False

# Define the states and their corresponding handlers
states = {
    STATE1: [
        MessageHandler(
            Filters.text & ~Filters.command, save_message(validate_product_id)
        )
    ],
    STATE2: [
        MessageHandler(
            Filters.text & ~Filters.command, save_message(get_paypal_account)
        )
    ],
    STATE3: [
        MessageHandler(
            Filters.text & ~Filters.command, save_message(get_amazon_account_link)
        )
    ],
    STATE4: [
        MessageHandler(Filters.photo, save_message(get_amazon_account_screenshot))
    ],
    STATE6: [
        MessageHandler(
            Filters.text & ~Filters.command, save_message(send_order_number_to_seller)
        )
    ],
    STATE7: [
        MessageHandler(Filters.photo, save_message(send_order_screenshot_to_seller))
    ],
}
