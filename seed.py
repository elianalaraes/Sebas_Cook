from app import create_app
from app import db
from app.models import MenuItem, MenuItemVariant, Admin

app = create_app()

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

    from app.models import Admin, MenuItem, MenuItemVariant

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from . import models
        db.create_all()

        # SEED AUTOMÁTICO: Solo se ejecuta la primera vez si no hay productos ni admin
        if not Admin.query.filter_by(username='sebas').first():
            print("--- Poblando la base de datos por primera vez ---")

            # 1. Roles de Canela
            roles = MenuItem(name="Rol de Canela", category="Roles", status="disponible")
            roles.variants = [
                MenuItemVariant(variant_name="Sencillo", price=55.0, remaining=5, status="disponible"),
                MenuItemVariant(variant_name="Pistache", price=55.0, remaining=10, status="disponible"),
                MenuItemVariant(variant_name="Nutella", price=55.0, remaining=10, status="disponible"),
            ]

            # 2. Galletas
            galletas = MenuItem(name="Galleta", category="Galletas", status="disponible")
            galletas.variants = [
                MenuItemVariant(variant_name="Red Velvet", price=15.0, remaining=0, status="sold_out"),
                MenuItemVariant(variant_name="Chispas de Chocolate", price=15.0, remaining=20, status="disponible"),
            ]

            # 3. Pan de Muerto
            pan_muerto = MenuItem(name="Pan de Muerto", category="Especiales", status="seasonal")
            pan_muerto.variants = [
                MenuItemVariant(variant_name="Tradicional", price=50.0, remaining=12, status="seasonal")
            ]

            # 4. Cupcake
            cupcake = MenuItem(name="Cupcake de Naranja", category="Cupcakes", status="sold_out")
            cupcake.variants = [
                MenuItemVariant(variant_name="Estándar", price=30.0, remaining=0, status="sold_out")
            ]

            # Guardar menú
            db.session.add_all([roles, galletas, pan_muerto, cupcake])

            # Guardar Administrador
            admin = Admin(username="sebas")
            admin.set_password("123")
            db.session.add(admin)

            db.session.commit()
            print("--- Base de datos inicializada con éxito ---")

    return app