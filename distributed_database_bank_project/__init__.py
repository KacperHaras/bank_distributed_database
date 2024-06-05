from flask import Flask
from .database import db, init_db
from .main import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    init_db(app)


    app.register_blueprint(main_blueprint)

    return app