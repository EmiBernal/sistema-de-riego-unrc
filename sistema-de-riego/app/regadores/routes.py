from functools import wraps

from flask_login import login_required, current_user

from ..extensions import db
from ..models import Regador
from . import regadores_bp


def _datos_basicos(regador):
    return {
        "id": regador.usuario_id,
        "nombre": regador.usuario.nombre,
        "apellido": regador.usuario.apellido,
        "dni": regador.dni,
    }

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.es_administrador:
            return "Acceso restringido", 403
        return func(*args, **kwargs)
    return wrapper

@regadores_bp.route("/")
@login_required
@admin_required
def lista_regadores():

    regadores = Regador.query.all()
    lista = []
    for regador in regadores:
        lista.append(_datos_basicos(regador))
    
    return lista


@regadores_bp.route("/buscar-regador/<int:usuario_id>")
@login_required
@admin_required
def buscar_regador(usuario_id):
    regador = db.get_or_404(Regador, usuario_id, description="Regador no encontrado")

    datos = _datos_basicos(regador)
    datos["telefono"] = regador.telefono
    datos["carnet_conducir"] = regador.carnet_conducir
    datos["info_seguro"] = regador.info_seguro
    return datos
