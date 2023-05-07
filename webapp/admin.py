from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from telebot.webapp.database import db
from telebot.webapp import models

admin = Admin(app, name='My App', template_mode='bootstrap3')
admin.add_view(ModelView(models.Product, db.session))