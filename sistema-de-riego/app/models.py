from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ENUM

from .extensions import db, login_manager

rol_usuario = ENUM(
    "SUPERUSUARIO", "REGADOR",
    name="rol_usuario",
    create_type=False,  
)


class User(UserMixin, db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    fecha_alta = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    rol = db.Column(rol_usuario, nullable=False, default="REGADOR")
    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)

    @property
    def es_superusuario(self):
        return self.rol == "SUPERUSUARIO"


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))