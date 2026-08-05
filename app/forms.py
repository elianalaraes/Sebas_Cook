from flask_wtf import FlaskForm
from wtforms import StringField, TelField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class OrderForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired()])
    telefono = TelField("Teléfono", validators=[DataRequired()])
    notas = StringField("Notas")
    submit = SubmitField("Pedir")


class LoginForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(message="El usuario es obligatorio.")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="La contraseña es obligatoria.")])
    submit = SubmitField('Entrar')