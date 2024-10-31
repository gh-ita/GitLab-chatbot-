from flask import Flask 
from embedchain import App

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    app.embedchain_app = App()

    from .routes import main 
    app.register_blueprint(main)

    return app

