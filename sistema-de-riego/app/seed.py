import os
from werkzeug import security
from .extensions import db
from .models import User


def crear_usuario_por_defecto():
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")

    if not email or not password or not os.getenv("ADMIN_ROL") or not os.getenv("ADMIN_ESTADO"):
        raise ValueError("Faltan variables de entorno para crear el administrador.")

    # Si ya existe, no hace nada
    if User.query.filter_by(email=email).first():
        return

    admin = User(
        nombre="Administrador",
        apellido= "Administrador",
        rol = os.getenv("ADMIN_ROL"),
        email=email,
        password_hash=security.generate_password_hash(password),
        estado = os.getenv("ADMIN_ESTADO")
    )
    db.session.add(admin)
    db.session.commit()