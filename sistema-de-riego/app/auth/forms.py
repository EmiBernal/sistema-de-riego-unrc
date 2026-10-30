from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    recordarme = BooleanField("Recordarme")
    submit = SubmitField("Ingresar")

class RegisterForm(FlaskForm):
    nombre = StringField("nombre", validators=[DataRequired()])
    apellido = StringField("apellido", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired(), Email(), Length(max=254)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8, max=128)])
    confirmar = PasswordField("Repetir contraseña", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Crear cuenta")