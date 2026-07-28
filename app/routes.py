from flask import Blueprint, render_template, request, redirect, url_for
from app.models import MenuItem

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
    return render_template('ordena.html', menu_items=menu_items)

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


