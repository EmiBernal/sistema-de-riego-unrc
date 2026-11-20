from functools import wraps
from flask import render_template, redirect, url_for, flash

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
    datos["activo"] = regador.activo
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
    regadores = Regador.query.filter_by(activo=True).all()
    return render_template("regadores/index.html", regadores=regadores)


@regadores_bp.route("/buscar-regador/<int:usuario_id>")
@login_required
@admin_required
def buscar_regador(usuario_id):
    regador = db.get_or_404(Regador, usuario_id, description="Regador no encontrado")

    return _datos_completos(regador)

@regadores_bp.route("/crear-regador", methods=["GET", "POST"])
@login_required
@admin_required
def crear_regador():
    form = RegadorForm()

    if form.validate_on_submit():
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
            flash("Ya existe un usuario con ese email o DNI.", "error")
        else:
            flash("Regador creado correctamente.", "success")
            return redirect(url_for("regadores.lista_regadores"))

    return render_template("regadores/crear.html", form=form)

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

    regador.activo = False
    db.session.commit()

    return "", 204

@regadores_bp.route("/activar-regador/<int:usuario_id>", methods=["POST"])
@login_required
@admin_required
def activar_regador(usuario_id):
    regador = db.get_or_404(Regador, usuario_id, description="Regador no encontrado")

    regador.activo = True 
    db.session.commit()

    return "", 204

