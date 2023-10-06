from flask import Flask, request, Blueprint
import telegram
from webapp import create_app

if __name__ == '__main__':
    app = create_app()
    app.run(port=5000)



