from flask import Flask, request, Blueprint
from config import Config
from bot import setup_updater
from flask_migrate import Migrate
from webapp.database import db
from admin import create_admin
from telegram.ext import Updater
from bot.handlers import init
import telegram
from webapp.routes import app_routes

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:admin@localhost/telegram"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)
create_admin(app, db)
app.debug = True
migrate = Migrate(app, db)
my_routes = Blueprint("my_routes", __name__)
updater = setup_updater()


@my_routes.route("/webhook", methods=["POST"])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), updater.bot)
    updater.dispatcher.process_update(update)
    return "OK"


def create_app():
    app.config.from_object(Config)
    init(updater.dispatcher)
    with app.app_context():
        db.init_app(app)
        app.register_blueprint(my_routes)
        app.register_blueprint(app_routes)
        db.create_all()

    return app
