import os
import logging

from flask import Flask, jsonify
from logging.handlers import RotatingFileHandler

from .config import BaseConfig
from .views import index


def create_app(config=None, app_name=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = config.PROJECT
    app = Flask(app_name)

    configure_app(app, config)
    configure_logging(app)
    return app


def configure_app(app, config=None):
    app.config.from_object(config)
    app.add_url_rule("/api", view_func=index, methods=["POST"])


def configure_logging(app):
    app.logger.setLevel(logging.INFO)
    info_log = os.path.join(app.config["LOG_FOLDER"], "info.log")
    info_file_handler = RotatingFileHandler(
        info_log, mode="w", maxBytes=100000, backupCount=10
    )
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
        )
    )
    app.logger.addHandler(info_file_handler)


app = create_app(BaseConfig)


@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"status": 404, "message": "404 Not Found"})


@app.route("/")
def status():
    data = {"status": "OK"}
    return jsonify(data), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=BaseConfig.DEBUG)
