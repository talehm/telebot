from telebot.webapp import app
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, Blueprint
from telebot.webapp.routes import my_routes

app = app.create_app()
app.register_blueprint(my_routes)

if __name__ == '__main__':
    app.run()