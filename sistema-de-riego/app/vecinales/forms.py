from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class CrearVecinalForm(FlaskForm):
    geofence_id = SelectField(
        "Geocerca de VSAT",
        coerce=int,
        validators=[DataRequired(message="Seleccioná una geocerca de la API")],
    )
    nombre = StringField(
        "Nombre de la vecinal",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=255)],
    )
    km = IntegerField(
        "Kilómetros totales de calles",
        validators=[
            DataRequired(message="Ingresá los kilómetros"),
            NumberRange(min=1, message="Debe ser mayor a 0"),
        ],
    )
    submit = SubmitField("Importar y guardar")


class EditarVecinalForm(FlaskForm):
    nombre = StringField(
        "Nombre de la vecinal",
        validators=[DataRequired(message="El nombre es obligatorio"), Length(max=255)],
    )
    km = IntegerField(
        "Kilómetros totales de calles",
        validators=[
            DataRequired(message="Ingresá los kilómetros"),
            NumberRange(min=1, message="Debe ser mayor a 0"),
        ],
    )
    submit = SubmitField("Guardar cambios")