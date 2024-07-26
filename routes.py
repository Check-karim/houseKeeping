from flask import Blueprint, render_template, request, flash, session, redirect, url_for
from models.models import User, Housekeeper, Admin

main = Blueprint('main', __name__)  # routename= main

@main.route('/', methods=['GET'])
def home():
    return render_template("index.html")

@main.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    user_type = request.form.get('user_type')

    if password != confirm_password:
        flash('Passwords do not match!')
        return redirect(url_for('main.home'))

    if user_type == 'user':
        new_user = User(email=email, password=password)
    else:
        new_housekeeper = Housekeeper(email=email, password=password)

    try:
        if user_type == 'user':
            new_user.save()
        else:
            new_housekeeper.save()
        flash('Registration successful! Please log in.')
    except:
        flash('Email already exists!')
        return redirect(url_for('main.home'))

    return redirect(url_for('main.home'))

@main.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    user_type = request.form.get('user_type')

    if user_type == 'user':
        user = User.query.filter_by(email=email).first()
    elif user_type == 'housekeeper':
        user = Housekeeper.query.filter_by(email=email).first()
    elif user_type == 'admin':
        user = Admin.query.filter_by(email=email).first()

    if user and user.password == password:
        session['user_id'] = user.id
        session['user_type'] = user_type
        if user_type == 'user':
            return redirect(url_for('main.user_dashboard'))
        elif user_type == 'housekeeper':
            return redirect(url_for('main.housekeeper_dashboard'))
        elif user_type == 'admin':
            return redirect(url_for('main.admin_dashboard'))
    else:
        flash('Login failed! Check your credentials and try again.')
        return redirect(url_for('main.home'))

@main.route('/user_dashboard', methods=['GET'])
def user_dashboard():
    if 'user_id' in session and session.get('user_type') == 'user':
        return render_template("user_dashboard.html")
    else:
        return redirect(url_for('main.home'))

@main.route('/housekeeper_dashboard', methods=['GET'])
def housekeeper_dashboard():
    if 'user_id' in session and session.get('user_type') == 'housekeeper':
        return render_template("housekeeper_dashboard.html")
    else:
        return redirect(url_for('main.home'))

@main.route('/admin_dashboard', methods=['GET'])
def admin_dashboard():
    if 'user_id' in session and session.get('user_type') == 'admin':
        return render_template("admin_dashboard.html")
    else:
        return redirect(url_for('main.home'))

@main.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('main.home'))
