from flask_wtf import FlaskForm
from wtforms import EmailField, PasswordField, StringField
from wtforms.validators import DataRequired, Email, Length, Optional, Regexp

from ..auth.forms import _normalizar_email

class RegadorForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    apellido = StringField("Apellido", validators=[DataRequired()])
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email(message="Ingresá un email válido", check_deliverability=True), Length(max=254)], filters=[_normalizar_email])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8, max=64, message="Debe tener entre 8 y 64 caracteres")])
    dni = StringField("DNI", validators=[DataRequired(), Length(max=10), Regexp(r"^\d+$", message="El DNI solo puede tener números")])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=20)])
    carnet_conducir = StringField("Carnet de conducir", validators=[Optional(), Length(max=10), Regexp(r"^\d+$", message="El carnet de conducir solo puede tener números")])
    info_seguro = StringField("Información del seguro", validators=[Optional(), Length(max=255)])

class EditarRegadorForm(FlaskForm):
    nombre = StringField("Nombre", validators=[Optional()])
    apellido = StringField("Apellido", validators=[Optional()])
    dni = StringField("DNI", validators=[Optional(), Length(max=10), Regexp(r"^\d+$", message="El DNI solo puede tener números")])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=20)])
    carnet_conducir = StringField("Carnet de conducir", validators=[Optional(), Length(max=10), Regexp(r"^\d+$", message="El carnet de conducir solo puede tener números")])
    info_seguro = StringField("Información del seguro", validators=[Optional(), Length(max=255)])
