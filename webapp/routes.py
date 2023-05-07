from flask import  request, Blueprint
from telebot.webapp.models import db
from telebot.bot.handlers import setup_handlers
from telebot.bot.bot import setup_updater
import telegram
# from telebot import Update, Bot
my_routes = Blueprint('my_routes', __name__)

@my_routes.route('/', methods=['GET'])
def home():
    return 'Hello, World!'

@my_routes.route('/webhook', methods=['POST'])
def bot():
    updater = setup_updater()
    update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
    # Handle the update here
    updater.dispatcher.process_update(update)
    return 'OK'
