from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'Por favor inicia sesión para acceder.'
    login_manager.login_message_category = 'danger'

    from app.models import Admin

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    # Crea las tablas automáticamente al levantar la app si aún no existen en la BD
    with app.app_context():
        from . import models
        from app.models import Admin  # Importamos el modelo Admin

        db.create_all()  # Crea las tablas en PostgreSQL si no existen

        # CREAR ADMINISTRADOR AUTOMÁTICAMENTE SI LA BASE DE DATOS ESTÁ VACÍA
        if not Admin.query.filter_by(username='sebas').first():
            admin = Admin(username='sebas')
            admin.set_password('123')  # Puedes cambiar la contraseña aquí
            db.session.add(admin)
            db.session.commit()
            print("--- Usuario Administrador 'sebas' creado automáticamente ---")

    return app