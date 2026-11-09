from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import current_user, login_required, login_user, logout_user
from ..extensions import db, limiter
from ..models import User
from .forms import LoginForm, RegisterForm
from werkzeug import security
from app.models import User
from sqlalchemy import exc

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        user = User(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            password_hash=security.generate_password_hash(form.password.data),
        )
        db.session.add(user)
        try:
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            form.email.errors.append("Email ya está registrado")
            return render_template("auth/register.html", form=form), 400  
        
        flash("Solicitud enviada. Un administrador la revisará.", "success")  
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)
         
@auth_bp.route("/login", methods=["GET","POST"])
@limiter.limit("5 per minute", methods=["POST"])
def login():
    form = LoginForm()

    ## Controlamos que los campos vengan
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        ## Busca el primer email registrado en la bases de datos.
        user = User.query.filter_by(email=email).first()


        # Si el usuario no existe o las contraseña
        if not user or not security.check_password_hash(user.password_hash, password):
            return "Email o contraseña incorrecta. Intente nuevamente.", 401

        # si el usuario tiene como estado pendiente o rechazado
        if user.estado in ("PENDIENTE", "RECHAZADO"):
            flash("Su cuenta aún no está disponible.", "warning")
            return render_template("login.html", form=form), 403
        
        session.permanent = True
        login_user(user, remember=False)
        return "Ok", 200
    return "Datos incompletos", 400

@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return "Ok", 200

@auth_bp.route("/me")
@login_required
def me():
    return {"email": current_user.email}