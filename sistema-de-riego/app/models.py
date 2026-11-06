from datetime import datetime, timezone

from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ENUM

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey

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

class Regador(db.Model):
    __tablename__ = "regador"

    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"), primary_key=True, autoincrement=False)
    dni: Mapped[str] = mapped_column(db.String(10), unique=True)
    telefono: Mapped[str | None] = mapped_column(db.String(20))
    carnet_conducir: Mapped[str | None] = mapped_column(db.String(255))
    info_seguro: Mapped[str | None] = mapped_column(db.String(255))

    usuario = db.relationship("User", backref=db.backref("regador", uselist=False))

    def __str__(self):
        return (
            f"Usuario_id:{self.usuario_id},"
            f"Dni:{self.dni},"
            f"Telefono:{self.telefono},"
            f"Carnet_conducir:{self.carnet_conducir},"
            f"Info_seguro:{self.info_seguro}"
        )
