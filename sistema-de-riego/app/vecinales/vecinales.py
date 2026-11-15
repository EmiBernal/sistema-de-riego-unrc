import json
from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import exc

from ..extensions import db
from ..models import Vecinal
from .forms import CrearVecinalForm, EditarVecinalForm
from .vsat_service import (
    VSATError,
    obtener_geocerca_por_id,
    obtener_geocercas_vsat,
    vertices_a_postgis,
)

vecinales_bp = Blueprint("vecinales", __name__, url_prefix="/vecinales")


@vecinales_bp.route("/")
@login_required
def index():
    vecinales = Vecinal.query.order_by(Vecinal.nombre.asc()).all()
    return render_template("vecinales/index.html", vecinales=vecinales)


@vecinales_bp.route("/nueva", methods=["GET", "POST"])
@login_required
def crear():
    form = CrearVecinalForm()
    geocercas = []

    try:
        geocercas = obtener_geocercas_vsat()
        form.geofence_id.choices = [
            (g["id"], f"{g['name']} (ID: {g['id']})") for g in geocercas
        ]
    except VSATError as err:
        form.geofence_id.choices = []
        flash(str(err), "error")

    if form.validate_on_submit():
        try:
            geocerca = obtener_geocerca_por_id(form.geofence_id.data)
            poligono = vertices_a_postgis(geocerca)

            nueva = Vecinal(
                nombre=form.nombre.data.strip(),
                km=form.km.data,
                polinomio=poligono,
            )
            db.session.add(nueva)
            db.session.commit()
            flash("Vecinal agregada correctamente.", "success")
            return redirect(url_for("vecinales.index"))
        except VSATError as err:
            flash(str(err), "error")
        except exc.SQLAlchemyError:
            db.session.rollback()
            flash("Error al guardar la vecinal en la base de datos.", "error")

    nombres_vsat = {g["id"]: g["name"] for g in geocercas}
    return render_template("vecinales/crear.html", form=form, nombres_vsat=nombres_vsat)


@vecinales_bp.route("/<int:vecinal_id>")
@login_required
def detalle(vecinal_id):
    vecinal = db.get_or_404(Vecinal, vecinal_id)
    poligono = to_shape(vecinal.polinomio)
    geojson = json.dumps(mapping(poligono))
    vertices = list(poligono.exterior.coords)

    return render_template(
        "vecinales/detalle.html",
        vecinal=vecinal,
        geojson=geojson,
        vertices=vertices,
    )


@vecinales_bp.route("/<int:vecinal_id>/editar", methods=["GET", "POST"])
@login_required
def editar(vecinal_id):
    vecinal = db.get_or_404(Vecinal, vecinal_id)
    form = EditarVecinalForm(obj=vecinal)

    if form.validate_on_submit():
        vecinal.nombre = form.nombre.data.strip()
        vecinal.km = form.km.data
        try:
            db.session.commit()
            flash("Vecinal actualizada correctamente.", "success")
            return redirect(url_for("vecinales.index"))
        except exc.SQLAlchemyError:
            db.session.rollback()
            flash("Error al actualizar la vecinal.", "error")

    return render_template("vecinales/editar.html", form=form, vecinal=vecinal)


@vecinales_bp.route("/<int:vecinal_id>/eliminar", methods=["POST"])
@login_required
def eliminar(vecinal_id):
    vecinal = db.get_or_404(Vecinal, vecinal_id)
    try:
        db.session.delete(vecinal)
        db.session.commit()
        flash("Vecinal eliminada correctamente.", "success")
    except exc.IntegrityError:
        db.session.rollback()
        flash("No se puede eliminar la vecinal porque tiene registros asociados.", "error")

    return redirect(url_for("vecinales.index"))