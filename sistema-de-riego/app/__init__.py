from dotenv import load_dotenv

from flask import Flask
from config import Config
from app.models import db
from app.auth.auth import auth_bp

load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Inicializar la base de datos
    db.init_app(app)

    # Registrar ñas rutas de autenticacion
    app.register_blueprint(auth_bp)

    @app.route("/")
    def index():
        return "Funciona"

    return app