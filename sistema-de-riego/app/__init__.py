import os

from flask import Flask


def create_app():
    app = Flask(__name__)


    @app.route("/")
    def index():
        return "Funciona"

    from app.regadores import regadores_bp
    app.register_blueprint(regadores_bp)

    return app