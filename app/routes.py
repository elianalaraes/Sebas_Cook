from flask import Blueprint, render_template, request, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def home():
    return redirect(url_for('main.landing'))

@main.route('/landing', methods=['GET', 'POST'])
def landing():
    return render_template('landing.html')

@main.route('/ordena', methods=['GET', 'POST'])
def ordena():
    return render_template('ordena.html')

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')


