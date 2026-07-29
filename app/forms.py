from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    telefono = TelField("Teléfono", validators=[DataRequired()])
    notas = StringField("Notas")
    submit = SubmitField("Pedir")