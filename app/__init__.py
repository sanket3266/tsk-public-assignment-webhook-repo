from flask import Flask
from app.extensions import init_app
from app.webhook.routes import webhook

def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = "mongodb://localhost:27017/database"
    init_app(app)
    app.register_blueprint(webhook)
    return app
