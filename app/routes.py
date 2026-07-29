import json
from . import db
from flask import Blueprint, render_template, request, redirect, url_for
from app.models import MenuItem, OrderItem, Order, MenuItemVariant
from app.forms import OrderForm

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.landing'))

@main.route('/landing', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

@main.route('/ordena', methods=['GET', 'POST'])
def ordena():
    menu_items = MenuItem.query.all()
    form = OrderForm()

    if form.validate_on_submit():
        items = json.loads(
            request.form.get('order_items')
        )

        order = Order(
            nombre=form.nombre.data,
            telefono=form.telefono.data,
            notas=form.notas.data,
            total=0
        )

        db.session.add(order)
        db.session.flush()

        total = 0

        for item in items:
            variant = MenuItemVariant.query.filter_by(
                variant_name=item['variantName']
            ).first()

            order_item = OrderItem(
                order_id=order.id,
                variant_id=variant.id,
                quantity=item['count'],
                price=item['price']
            )

            total += item['price'] * item['count']

            # descontar inventario
            variant.remaining -= item['count']

            db.session.add(order_item)

        order.total = total

        db.session.commit() # esto se debería cambiar de aquí a models

    return render_template('ordena.html', menu_items=menu_items, form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


