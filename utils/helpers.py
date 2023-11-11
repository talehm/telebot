from validate_email_address import validate_email
from urllib.parse import urlparse
import validators
import os, re, json
import uuid
from datetime import datetime, timedelta
from webapp import models, enums
from webapp.database import DBHelper
from utils import helpers, constraints, constants
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode

dbHelper = DBHelper()


def is_valid_email(email):
    return validate_email(email)


def is_valid_url(text):
    # Check if the text starts with a valid URL scheme
    if validators.url(text):
        # Parse the URL using urlparse
        parsed_url = urlparse(text)
        # Check if the scheme and netloc are present
        if parsed_url.scheme and parsed_url.netloc == "www.amazon.de":
            return True
    return False


def validate_order_number(text):
    pattern = r"^\d{3}-\d{7}-\d{7}$"
    if re.match(pattern, text):
        return True
    else:
        return False


def unique_id():
    # Generate a UUID4 (random) ID
    unique_id = uuid.uuid4()

    # Convert the UUID to a string
    unique_id_str = str(unique_id)

    return unique_id_str


def is_older_than(date, weeks=0, days=0, hours=0):
    current_date = datetime.now()
    date_format = "%Y-%m-%d %H:%M:%S"
    # date = datetime.strptime(date, date_format)
    past_date = current_date - timedelta(weeks=weeks, days=days, hours=hours)

    if date < past_date:
        return True
    else:
        return False


def save_photo(update, context, source):
    try:
        #
        if source is constants.ORDER_SCREENSHOT:
            source = "orders"
        elif source is constants.ACCOUNT_SCREENSHOT:
            source = "accounts"
        #
        SAVE_DIR = f"{constraints.IMAGE_DIR}\{source}"

        photo = update.message.photo[-1]
        # Get the file ID and file path
        file_id = photo.file_id
        file = context.bot.get_file(file_id)

        # Create the save directory if it doesn't exist
        os.makedirs(SAVE_DIR, exist_ok=True)
        # Save the photo with a unique name
        save_path = os.path.join(SAVE_DIR, f"{file_id}.jpg")
        file.download(save_path)
        return save_path
    except Exception as e:
        print(f"Error saving photo: {e}")
        return False


def send_to_seller(update, context, action=None, **kwargs):
    try:
        seller = None
        buyer = dbHelper.get_one(models.Buyer, chat_id=context.user_data.get("chat_id"))
        keyboard = []

        if action == constants.REVIEW_SCREENSHOT:
            order = context.user_data.get("selected_order")
            if not order:
                return
            product = dbHelper.get_one(models.Product, id=order.product_id)
            seller = dbHelper.get_one(models.Seller, id=product.seller_id)

            message = (
                f"🔔 <b>Buyer has sent review screenshot for below order.</b> 🔔\n\n"
                f"{order.order_number}\n"
                f"🆔 {product.id}\n"
                f"📦 Product: {product.description}\n\n"
                f"👤 <b>CUSTOMER DETAILS</b>\n\n"
                f"📨 Paypal: {buyer.paypal}\n"
                f"🔗 Amazon Account : {buyer.amazon_url}\n"
            )

            context.bot.send_message(
                chat_id=seller.chat_id, text=message, parse_mode=ParseMode.HTML
            )
            context.bot.send_photo(
                chat_id=seller.chat_id,
                photo=open(context.user_data["review_screenshot"], "rb"),
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

        elif action in [constants.NEW_ORDER_REQUEST, constants.ORDER_SCREENSHOT]:
            product = context.user_data["chosen_product"]
            seller = dbHelper.get_one(models.Seller, id=product.seller_id)

            if action == constants.NEW_ORDER_REQUEST:
                order_model = models.Order(
                    product_id=product.id,
                    buyer_id=buyer.id,
                    status=enums.OrderStatus.WAITING_CONFIRMATION,
                )
                order = dbHelper.add(order_model)
                context.user_data["order_id"] = order.id

                message = (
                    f"🔔 <b>New Order Request Received.</b> 🔔\n\n"
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
                    caption="Amazon Account Screenshot",
                )

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "✅ Confirm",
                            callback_data=json.dumps(
                                {
                                    "action": "confirm_new_order_request",
                                    "order_id": order.id,
                                }
                            ),
                        ),
                        InlineKeyboardButton(
                            "❌ Reject",
                            callback_data=json.dumps(
                                {
                                    "action": "reject_new_order_request",
                                    "order_id": order.id,
                                }
                            ),
                        ),
                    ]
                ]

            elif action == constants.ORDER_SCREENSHOT:
                order = dbHelper.get_one(models.Order, id=context.user_data["order_id"])
                message = f"🔔 *Order number: {re.escape(order.order_number)} \n Screenshot for Order id {order.id}* 🔔"

                context.bot.send_photo(
                    chat_id=seller.chat_id,
                    photo=open(context.user_data["amazon_order_screenshot"], "rb"),
                    caption=message,
                    parse_mode=ParseMode.MARKDOWN_V2,
                )

                order.status = enums.OrderStatus.SS_SENT
                dbHelper.update(order)

                keyboard = [
                    [
                        InlineKeyboardButton(
                            "✅ Confirm",
                            callback_data=json.dumps(
                                {
                                    "action": "accept_order_screenshot",
                                    "order_id": order.id,
                                }
                            ),
                        ),
                        InlineKeyboardButton(
                            "❌ Reject",
                            callback_data=json.dumps(
                                {
                                    "action": "decline_order_screenshot",
                                    "order_id": order.id,
                                }
                            ),
                        ),
                    ]
                ]

        if seller:
            reply_markup = InlineKeyboardMarkup(keyboard)
            context.bot.sendMessage(
                chat_id=seller.chat_id,
                text="Please choose an option:",
                reply_markup=reply_markup,
            )

    except Exception as e:
        update.message.reply_text(
            f"Error occurred. Message is not delivered to the seller: {e}"
        )
