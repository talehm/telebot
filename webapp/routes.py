from flask import request, Blueprint

# from telebot import Update, Bot
app_routes = Blueprint("app_routes", __name__)


@app_routes.route("/", methods=["GET"])
def home():
    return "Hello, World!"


@app_routes.route("/", methods=["POST"])
def test():
    return "Hello, World!"
