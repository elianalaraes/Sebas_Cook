from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db

class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Genera el hash seguro de la contraseña."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verifica si la contraseña coincide con el hash."""
        return check_password_hash(self.password_hash, password)

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), nullable=True)  # e.g., 'Roles', 'Galletas', 'Cupcakes'

    # Relationship to variants (e.g. Rol de Canela -> [Sencillo, Pistache, Nutella])
    variants = db.relationship('MenuItemVariant', backref='item', lazy=True, cascade="all, delete-orphan")

    def __repr__(self):
        return f'<MenuItem {self.name}>'


class MenuItemVariant(db.Model):
    __tablename__ = 'menu_item_variants'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False)

    # Variant specific info
    variant_name = db.Column(db.String(100), nullable=False)  # e.g., 'Sencillo', 'Pistache', 'Chispas'
    price = db.Column(db.Float, nullable=False)
    remaining = db.Column(db.Integer, default=0, nullable=False)
    status = db.Column(db.String(20), default='available', nullable=False)  # 'available', 'sold_out', etc.

    def __repr__(self):
        return f'<MenuItemVariant {self.variant_name} - ${self.price}>'


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)

    nombre = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    notas = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(30), nullable=False, default='pendiente')

    total = db.Column(db.Float, nullable=False, default=0)

    status = db.Column(
        db.String(20),
        default='pending'
    )  # pending, completed, cancelled

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp()
    )

    # productos del pedido
    items = db.relationship(
        'OrderItem',
        backref='order',
        cascade="all, delete-orphan",
        lazy=True
    )


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)

    order_id = db.Column(
        db.Integer,
        db.ForeignKey('orders.id'),
        nullable=False
    )

    variant_id = db.Column(
        db.Integer,
        db.ForeignKey('menu_item_variants.id'),
        nullable=False
    )

    quantity = db.Column(
        db.Integer,
        nullable=False
    )

    # guardamos el precio de ese momento
    # por si después cambia el precio del menú
    price = db.Column(
        db.Float,
        nullable=False
    )

    variant = db.relationship(
        'MenuItemVariant'
    )


    def subtotal(self):
        return self.quantity * self.price