from dotenv import load_dotenv

from flask import Flask
from config import Config
from app.auth.auth import auth_bp
from app.main.routes import main_bp
from .extensions import  db, login_manager
from .seed import crear_usuario_por_defecto


load_dotenv()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    #Inicializar la base de datos
    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


    # Registrar las rutas de autenticacion
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()                # crea las tablas si no existen
        crear_usuario_por_defecto()    # crea el usuario si no existe

    return app