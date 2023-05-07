from flask import Flask, request, Blueprint
from telebot.config import Config
from telebot.bot.bot import setup_updater
from flask_migrate import Migrate
from telebot.webapp.database import db
from telebot.admin import create_admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:admin@localhost/telegram'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
db.init_app(app)
create_admin(app, db)
app.debug = True

migrate = Migrate(app, db)
def create_app():
    app.config.from_object(Config)
    setup_updater()
    with app.app_context():
        db.create_all()

    return app
