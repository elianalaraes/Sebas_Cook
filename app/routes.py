from flask import Blueprint, render_template, request, redirect, url_for
from app.models import MenuItem
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
        nombre = form.nombre.data
        email = form.email.data
        notas = form.notas.data

        # Save order...

    return render_template('ordena.html', menu_items=menu_items, form=form)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


