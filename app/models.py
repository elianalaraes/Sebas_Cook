from . import db

class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='available', nullable=False)
    remaining = db.Column(db.Integer, default=0, nullable=False)

    def __repr__(self):
        return f'<MenuItem {self.name}>'