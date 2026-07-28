from . import db


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