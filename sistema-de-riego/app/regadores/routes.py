from functools import wraps

from flask_login import login_required, current_user
from sqlalchemy import exc
from werkzeug import security

from ..extensions import db
from ..models import Regador, User
from . import regadores_bp
from .forms import RegadorForm, EditarRegadorForm


def _datos_basicos(regador):
    return {
        "id": regador.usuario_id,
        "nombre": regador.usuario.nombre,
        "apellido": regador.usuario.apellido,
        "dni": regador.dni,
    }

def _datos_completos(regador):
    datos = _datos_basicos(regador)
    datos["telefono"] = regador.telefono
    datos["carnet_conducir"] = regador.carnet_conducir
    datos["info_seguro"] = regador.info_seguro
    return datos

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

    return _datos_completos(regador)

@regadores_bp.route("/crear-regador", methods=["POST"])
@login_required
@admin_required
def crear_regador():
    form = RegadorForm()

    if not form.validate_on_submit():
        return form.errors, 400

    usuario = User(
        nombre=form.nombre.data,
        apellido=form.apellido.data,
        email=form.email.data,
        password_hash=security.generate_password_hash(form.password.data),
        rol="USUARIO",
        estado="APROBADO",
    )
    regador = Regador(
        usuario=usuario,
        dni=form.dni.data,
        telefono=form.telefono.data,
        carnet_conducir=form.carnet_conducir.data,
        info_seguro=form.info_seguro.data,
    )
    db.session.add(regador)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return "Ya existe un usuario con ese email o DNI", 409

    return _datos_basicos(regador), 201

@regadores_bp.route("/editar-regador/<int:usuario_id>", methods=["POST"])
@login_required
@admin_required
def editar_regador(usuario_id):
    regador = db.get_or_404(Regador, usuario_id, description="Regador no encontrado")

    form = EditarRegadorForm()

    if not form.validate_on_submit():
        return form.errors, 400

    campos_por_objeto = (
        (regador.usuario, ("nombre", "apellido")),
        (regador, ("dni", "telefono", "carnet_conducir", "info_seguro")),
    )
    for objeto, campos in campos_por_objeto:
        for campo in campos:
            nuevo_valor = getattr(form, campo).data
            if nuevo_valor:
                setattr(objeto, campo, nuevo_valor)

    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return "Ya existe un regador con ese DNI", 409

    return _datos_completos(regador)

@regadores_bp.route("/eliminar-regador/<int:usuario_id>", methods=["POST"])
@login_required
@admin_required
def eliminar_regador(usuario_id):
    regador = db.get_or_404(Regador, usuario_id, description="Regador no encontrado")

    db.session.delete(regador)
    db.session.delete(regador.usuario)
    try:
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        return "No se puede eliminar: el regador tiene registros asociados", 409

    return "", 204
