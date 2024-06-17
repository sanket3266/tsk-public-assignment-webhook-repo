from flask_pymongo import PyMongo

client = PyMongo()

def init_app(app):
    client.init_app(app)
