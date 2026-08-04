import json
from . import db
from flask import Blueprint, render_template, request, redirect, url_for, flash
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
        order_items_raw = request.form.get("order_items")

        # Validar si el carrito está vacío o contiene una lista vacía "[]"
        if not order_items_raw or order_items_raw == "[]":
            flash("Debes agregar al menos un producto al pedido.", "danger")
            return render_template("ordena.html", form=form, menu_items=menu_items)

        items = json.loads(order_items_raw)

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

            if variant:
                order_item = OrderItem(
                    order_id=order.id,
                    variant_id=variant.id,
                    quantity=item['count'],
                    price=item['price']
                )

                total += item['price'] * item['count']

                # Descontar inventario
                variant.remaining -= item['count']

                db.session.add(order_item)

        order.total = total
        db.session.commit()

        flash("¡Tu pedido ha sido registrado con éxito!", "success")
        return redirect(url_for('main.ordena'))

    else:
        if request.method == "POST":
            flash("Por favor completa todos los campos obligatorios.", "danger")

    return render_template('ordena.html', menu_items=menu_items, form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')