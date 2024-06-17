from flask import Flask
from app.extensions import init_app
from app.webhook.routes import webhook

def create_app():
    app = Flask(__name__)

    # Initialize MongoDB
    app.db = init_app(app)

    # Register blueprints
    app.register_blueprint(webhook)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
