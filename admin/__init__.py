from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin
from telebot.webapp import models 
from telebot.admin import views

def create_admin(app, db):
    admin = Admin(app, name='My App Admin', template_mode='bootstrap3')
    admin.add_view(views.ProductView(models.Product, db.session))
    admin.add_view(ModelView(models.Buyer , db.session))
    admin.add_view(ModelView(models.Seller, db.session))
    admin.add_view(ModelView(models.Verification, db.session))
    admin.add_view(ModelView(models.Message, db.session))