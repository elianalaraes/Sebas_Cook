import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import Admin, Order, MenuItem, MenuItemVariant, OrderItem
from app.forms import LoginForm, OrderForm, PasswordField
from . import db

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


@main.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        admin = Admin.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            login_user(admin)
            flash("¡Bienvenido al Panel de Control!", "success")

            next_page = request.args.get('next')
            return redirect(next_page or url_for('main.dashboard'))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template('login.html', form=form)


@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("Has cerrado sesión correctamente.", "info")
    return redirect(url_for('main.login'))


# --- DASHBOARD & GESTIÓN DE PEDIDOS ---

@main.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # Obtener el filtro activo desde el query param (?status=...)
    status_filter = request.args.get('status', 'todos')

    query = Order.query
    if status_filter != 'todos':
        query = query.filter_by(status=status_filter)

    orders = query.order_by(Order.created_at.desc()).all()

    # Contadores para las métricas rápidas del dashboard
    stats = {
        'todos': Order.query.count(),
        'pendiente': Order.query.filter_by(status='pendiente').count(),
        'aceptado': Order.query.filter_by(status='aceptado').count(),
        'en_proceso': Order.query.filter_by(status='en_proceso').count(),
        'en_delivery': Order.query.filter_by(status='en_delivery').count(),
        'completado': Order.query.filter_by(status='completado').count(),
    }

    return render_template('dashboard.html', orders=orders, stats=stats, current_status=status_filter)


@main.route('/admin/order/<int:order_id>/update-status', methods=['POST'])
@login_required
def update_order_status(order_id):
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')

    valid_statuses = ['pendiente', 'aceptado', 'en_proceso', 'en_delivery', 'completado']
    if new_status in valid_statuses:
        order.status = new_status
        db.session.commit()
        flash(f"Estado del pedido #{order.id} actualizado a '{new_status.replace('_', ' ').capitalize()}'.", "success")
    else:
        flash("Estado inválido.", "danger")

    return redirect(request.referrer or url_for('main.dashboard'))

@main.route('/admin/order/<int:order_id>/delete', methods=['POST'])
@login_required
def delete_order(order_id):
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    flash(f"El pedido #{order_id} ha sido eliminado permanentemente.", "info")
    return redirect(url_for('main.dashboard'))