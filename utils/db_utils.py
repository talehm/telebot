from datetime import datetime
from webapp import models
from webapp import types
from webapp.database import DBHelper
from telegram import Update
from webapp.enums import ServiceType
import json
from utils.decorators import message_to_json

dbHelper = DBHelper()


@message_to_json
def save_user(update, message):
    if "from" in message and message["from"] is not None:
        from_info = message["from"]
        chat_id = from_info.get("id")
        first_name = from_info.get("first_name")
        last_name = from_info.get("last_name")
        username = from_info.get("username")
        language_code = from_info.get("language_code")
    else:
        # Handle the case when 'from' key is missing or its value is None
        # For example, you can set default values or raise an error
        # Default values example:
        chat_id = None
        first_name = None
        last_name = None
        username = None
        language_code = None

    print("MERYEM", last_name)
    user = models.Buyer(
        chat_id=chat_id,
        first_name=first_name,
        last_name=last_name,
        username=username,
        is_active=True,
        is_blocked=False,
        language_code=language_code,
        paypal=None,
        amazon_screenshot=None,
        amazon_url=None,
    )
    # test_product = models.Product(
    #     name='test',
    #     description = 'test',
    #     status = 'AVAILABLE',
    #     price = 5.00,
    #     seller_id = 1,
    #     url = 'https://unsplash.com/photos/e616t35Vbeg',
    #     image_url = 'https://unsplash.com/photos/e616t35Vbeg',
    #     properties = types.ProductProperties(
    #         refund = types.ProductPropertiesRefund(isFullRefund = True, amount = 5),
    #         paypal = types.ProductPropertiesPaypal(isPaypalFeeIncluded=True, amount = 5),
    #         service_type = ServiceType.REVIEW.value
    #     )
    # )
    # dbHelper.add(test_product)
    user_exists = dbHelper.get_one(models.Buyer, chat_id=chat_id)
    if user_exists:
        dbHelper.update(
            user_exists,
            first_name=first_name,
            last_name=last_name,
            username=username,
            language_code=language_code,
        )
    else:
        dbHelper.add(user)
