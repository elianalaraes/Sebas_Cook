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
    login_message = 'Por favor inicia sesión para acceder.'
    login_message_category = 'danger'

    from app.models import Admin, MenuItem, MenuItemVariant

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        from . import models
        from app.models import Admin, MenuItem, MenuItemVariant

        # 1. Elimina todas las tablas de PostgreSQL (para limpiar la estructura vieja)
        db.reflect()
        db.drop_all()

        # 2. Crea las tablas desde cero según tu models.py actual (sin status en MenuItem)
        db.create_all()

        print("--- Poblando catálogo de productos en la base de datos ---")

        # 3. Crear productos
        roles = MenuItem(name="Rol de Canela", category="Roles")
        roles.variants = [
            MenuItemVariant(variant_name="Sencillo", price=55.0, remaining=5, status="available"),
            MenuItemVariant(variant_name="Pistache", price=55.0, remaining=10, status="available"),
            MenuItemVariant(variant_name="Nutella", price=55.0, remaining=10, status="available"),
        ]

        galletas = MenuItem(name="Galleta", category="Galletas")
        galletas.variants = [
            MenuItemVariant(variant_name="Red Velvet", price=15.0, remaining=0, status="sold_out"),
            MenuItemVariant(variant_name="Chispas de Chocolate", price=15.0, remaining=20, status="available"),
        ]

        pan_muerto = MenuItem(name="Pan de Muerto", category="Especiales")
        pan_muerto.variants = [
            MenuItemVariant(variant_name="Tradicional", price=50.0, remaining=12, status="available")
        ]

        cupcake = MenuItem(name="Cupcake de Naranja", category="Cupcakes")
        cupcake.variants = [
            MenuItemVariant(variant_name="Estándar", price=30.0, remaining=0, status="sold_out")
        ]

        db.session.add_all([roles, galletas, pan_muerto, cupcake])

        # 4. Crear Administrador
        admin = Admin(username="sebas")
        admin.set_password("123")
        db.session.add(admin)

        # 5. Guardar cambios
        db.session.commit()
        print("--- ¡Base de datos reconstruida y poblada con éxito! ---")

    return app