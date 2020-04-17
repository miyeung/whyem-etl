import logging
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from whyemetl.location import Position, Rectangle


def get_logger() -> logging.Logger:
    """ Returns a well formatted logger with INFO level streaming out to stdout. """

    fmt = logging.Formatter(
        "[%(asctime)s] [%(filename)s:%(funcName)s:%(lineno)d] [%(levelname)s] - %(message)s"
    )
    logger = logging.getLogger(__name__)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(fmt)

    logger.addHandler(stream_handler)
    loglevel = logging.INFO

    logger.setLevel(loglevel)
    return logger


#
# Global variables
#

log = get_logger()
db = SQLAlchemy()


#
# Utility functions
#


def create_app() -> Flask:
    """ Returns a Flask application with database ORM and blueprint initialized. """

    from . import views

    app = Flask(__name__)
    app.register_blueprint(views.bp)
    db.init_app(app)
    return app


def db_url() -> str:
    """ Returns database URL for Postgres with docker-compose integration. """

    db_host = os.environ["PGHOST"]
    db_name = os.environ["PGDATABASE"]
    db_user = os.environ["PGUSER"]
    db_password = os.environ["PGPASSWORD"]
    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}/{db_name}"


#
# Global geo-continent approximated by Rectangle
#


upperleft = Position(58.950306, -17.455528)  # North-West of UK
bottomright = Position(42.324367, 27.273977)  # South-East of Bulgaria
europe = Rectangle("EUROPE", upperleft, bottomright)

upperleft = Position(71.608584, -168.455893)  # Somewhere in Chukchi Sea
bottomright = Position(23.437493, -52.142073)  # North-east or Porto Rico
america = Rectangle("AMERICA", upperleft, bottomright)

upperleft = Position(71.654537, 37.787070)  # Somewhere in Barents Sea
bottomright = Position(15.050491, 144.707127)  # Somewhere in the Philippine Sea
asia = Rectangle("ASIA", upperleft, bottomright)
