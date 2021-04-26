from flask import Flask
from flask_cors import CORS
import random

from flaskr.models import setup_db
from flaskr.routes import create_routes
from flaskr.errors import create_error_handlers


QUESTIONS_PER_PAGE = 10


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__)

    if config is not None:
        app.config.from_object(config)

    setup_db(app)

    CORS(app)

    create_routes(app)

    create_error_handlers(app)

    return app

