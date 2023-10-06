from webapp import app
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request, Blueprint
from webapp.routes import app_routes

app, updater = app.create_app()
app.register_blueprint(app_routes)

if __name__ == '__main__':
    app.run()