from app import create_app
from app import db
from app.models import MenuItem, MenuItemVariant

app = create_app()

def seed_database():
    with app.app_context():
        print("Cleaning up old data...")
        db.drop_all()
        db.create_all()

        print("Seeding menu items...")

        # 1. Roles de Canela
        roles = MenuItem(name="Rol de Canela", category="Roles")
        roles.variants = [
            MenuItemVariant(variant_name="Sencillo", price=55.0, remaining=5, status="available"),
            MenuItemVariant(variant_name="Pistache", price=55.0, remaining=10, status="available"),
            MenuItemVariant(variant_name="Nutella", price=55.0, remaining=10, status="available"),
        ]

        # 2. Galletas
        galletas = MenuItem(name="Galleta", category="Galletas")
        galletas.variants = [
            MenuItemVariant(variant_name="Red Velvet", price=15.0, remaining=15, status="sold_out"),
            MenuItemVariant(variant_name="Chispas de Chocolate", price=15.0, remaining=20, status="available"),
        ]

        # 3. Pan de Muerto (Single variant)
        pan_muerto = MenuItem(name="Pan de Muerto", category="Especiales")
        pan_muerto.variants = [
            MenuItemVariant(variant_name="Tradicional", price=50.0, remaining=12, status="temporada")
        ]

        # 4. Cupcake (Single variant)
        cupcake = MenuItem(name="Cupcake de Naranja", category="Cupcakes")
        cupcake.variants = [
            MenuItemVariant(variant_name="Estándar", price=30.0, remaining=10, status="agotado")
        ]

        # Add all to session and commit
        db.session.add_all([roles, galletas, pan_muerto, cupcake])
        db.session.commit()

        print("Successfully seeded the database!")

if __name__ == "__main__":
    seed_database()