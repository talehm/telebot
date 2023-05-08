# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telebot.webapp import models
from telebot.webapp.database import DBHelper


def validate_product_id(update, context):
    text = update.message.text
    if not text.isdigit():
        update.message.reply_text("Please a valid product name (should contain at least one number)")
        return
    else:
        dbHelper = DBHelper()
        product = dbHelper.get_one(models.Product, id=text)
        if not product: 
            update.message.reply_text("This product ID does not exist")
        else:
            photo_url = product.image_url
            product_info = f"Product Name: {product.name}\n" \
               f"Price: {product.price}\n" \
               f"Description: {product.description}\n" \
               f"Properties: {product.properties}\n\n"\
               f"Link: {product.url}"
            # photo_file = BytesIO(requests.get(photo_url).content)
            update.message.reply_photo(photo=photo_url, caption=product_info)


def get_handlers():
    return [
        MessageHandler(Filters.text & ~Filters.command, validate_product_id)
    ]
