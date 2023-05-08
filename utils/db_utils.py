from datetime import datetime
from telebot.webapp import models
from telebot.webapp import types
from telebot.webapp.database import DBHelper
from telegram import Update
from telebot.webapp.enums import ServiceType
import json
from telebot.utils.decorators import message_to_json

dbHelper = DBHelper()

@message_to_json
def save_user(update, message):
    chat_id = message["from"]["id"]
    first_name = message["from"]["first_name"]
    last_name = message["from"]["last_name"]
    username = message["from"]["username"]
    language_code = message["from"]["language_code"]

    user = models.Buyer(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        is_active=True,
        is_blocked=False,
        language_code=language_code
    )
    test_product = models.Product(
        name='test',
        description = 'test',
        status = 'AVAILABLE',
        price = 5.00,
        seller_id = 1,
        url = 'https://unsplash.com/photos/e616t35Vbeg',
        image_url = 'https://unsplash.com/photos/e616t35Vbeg',
        properties = types.ProductProperties(
            refund = types.ProductPropertiesRefund(isFullRefund = True, amount = 5),
            paypal = types.ProductPropertiesPaypal(isPaypalFeeIncluded=True, amount = 5),
            service_type = ServiceType.REVIEW.value
        )
    ) 
    dbHelper.add(test_product)
    user_exists = dbHelper.get_one(models.Buyer, chat_id=chat_id)
    if user_exists:
        dbHelper.update(user_exists, first_name=first_name, last_name=last_name,username=username, language_code=language_code)
    else:
        dbHelper.add(user)
