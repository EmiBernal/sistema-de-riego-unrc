from urllib import request

from flask import Blueprint, render_template, redirect, url_for, flash
from ..extensions import db, limiter
from ..models import User
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash
from app.models import User
from sqlalchemy.exc import IntegrityError

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

#@bp.route("/login", methods=["GET", "POST"])
#@limiter.limit("5 per day", methods=["POST"])
#def login():

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            nombre = form.nombre.data,
            apellido = form.apellido.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data)
        )
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            form.email.errors.append("Ese email ya esta registado")
            #return render_template("auth/register.html", form=form), 409
            return "Formulario inválido", 400
        flash("Cuenta creada. Ya podes iniciar sesion.")
        return redirect(url_for("index"))
    print(form.errors)
    return "Formulario inválido", 400
    
    #return render_template("auth/register.html", form=form)
        
