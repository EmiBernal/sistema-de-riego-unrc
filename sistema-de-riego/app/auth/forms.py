import re
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

def _normalizar_email(valor):
    return valor.strip().lower() if valor else valor

class LoginForm(FlaskForm):
    email = EmailField("Correo electronico", validators=[DataRequired(), Email()], filters=[_normalizar_email])
    password = PasswordField("Contraseña", validators=[DataRequired()])
    submit = SubmitField("Ingresar")

class RegisterForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(message="Este campo es requerido")])
    apellido = StringField("Apellido", validators=[DataRequired(message="Este campo es requerido")])
    email = EmailField("Correo electrónico", validators=[DataRequired(), Email(message="Ingresá un email válido", check_deliverability=True), Length(max=254)])
    password = PasswordField("Contraseña", validators=[DataRequired(), Length(min=8, max=64, message="Debe tener entre 8 y 64 caracteres")])
    confirmar = PasswordField("Repetir contraseña", validators=[DataRequired(), EqualTo("password", message="Las contraseñas no coinciden")])
    condiciones = BooleanField(
            "Acepto los términos de uso y el tratamiento de mis datos personales.",
            validators=[DataRequired(message="Debés aceptar los términos para continuar.")],
        )
    submit = SubmitField("Enviar solicitud")

    def validate_email(self, field):
            field.data = field.data.strip().lower()
    
    def validate_password(self, field):
            pwd = field.data
            if not re.search(r"[A-Z]", pwd):
                raise ValidationError("Debe incluir al menos una mayúscula")
            if not re.search(r"[a-z]", pwd):
                raise ValidationError("Debe incluir al menos una minúscula")
            if not re.search(r"\d", pwd):
                raise ValidationError("Debe incluir al menos un número")
            if not re.search(r"[^\w\s]", pwd):
                raise ValidationError("Debe incluir al menos un símbolo (!@#$...)")