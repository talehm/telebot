# from telebot import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, MessageHandler, Filters,CallbackQueryHandler,ConversationHandler
from webapp import models
from webapp.database import DBHelper
from telegram import ParseMode
from utils import helpers

dbHelper = DBHelper()
PRODUCT_ID, EMAIL_ADDRESS, ACCOUNT_LINK = range(3)

# class HandleQuery:
    
    # product_info = f" ❇️ * {product.name}*\n\n" \
    #                f"{product.description}\n\n" \
    #                f"{'✅ *FULL REFUND*' if product.properties['refund']['isFullRefund'] == True else '✅ *Refund: ' + str(product.properties['refund']['amount'])+'*'}\n\n" \
    #                f"{'✅ *Paypal Fee Included*' if product.properties['paypal']['isPaypalFeeIncluded'] == True else 'Paypal Fee Not Included'}\n\n" \
    #                f"💰 *Price: {product.price}* 💰\n\n" \
    #                f"{product.url}\n\n\n"\
    #                f"Next Step: Please send paypal account."

def get_paypal_account(update, context):
            text = update.message.text
            if not helpers.verify_email_address(text):
                update.message.reply_text("Email format is not correct. Please try again") 
            else:
                update.message.reply_text("Please send amazon account")

def validate_product_id(update, context):
            text = update.message.text
            if not text.isdigit():
                update.message.reply_text("Please choose a valid product name (should contain at least one number)")
                return
            else:
                product = dbHelper.get_one(models.Product, id=text)
                if not product: 
                    update.message.reply_text("This product ID does not exist")
                else:
                    photo_url = product.image_url
                    product_info = f"✅*Product is Available*✅\n\n" \
                    f"*Chosen Product*: {product.description}\n" \
                    f"{'✅ *FULL REFUND*' if product.properties['refund']['isFullRefund'] == True else '✅ *Refund: ' + str(product.properties['refund']['amount'])+'*'}\n" \
                    f"{'✅ *Paypal Fee Included*' if product.properties['paypal']['isPaypalFeeIncluded'] == True else 'Paypal Fee Not Included'}\n" \
                    f"💰 *Price: {product.price}* 💰\n\n" \
                    f"{product.url}\n\n\n"\
                    f"*Next Step: Please send your paypal account.*\n"\
                    # photo_file = BytesIO(requests.get(photo_url).content)
                    update.message.reply_photo(photo=photo_url, caption=product_info, parse_mode=ParseMode.HTML)
                    context.user_data['next_step'] = 'get_paypal_account'




def get_handlers():
    return [
        MessageHandler(Filters.text & ~Filters.command, validate_product_id),
        MessageHandler(Filters.text & ~Filters.command, get_paypal_account),
        # ConversationHandler(
        #         entry_points=[MessageHandler(Filters.text & ~Filters.command, validate_product_id)],
        #         states={
        #             PRODUCT_ID: [MessageHandler(Filters.text, validate_product_id)],
        #             EMAIL_ADDRESS: [MessageHandler(Filters.text, get_paypal_account)],
        #         },
        #         fallbacks=[]
        #     )
    ]
