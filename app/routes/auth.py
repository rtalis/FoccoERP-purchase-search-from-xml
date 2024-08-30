from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from app import db
from app.models import User
from wtforms.validators import DataRequired
from app.forms import RegistrationForm, LoginForm
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


bp = Blueprint('auth', __name__)
limiter = Limiter(key_func=get_remote_address)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
@limiter.limit("5 per 5 seconds")
def login():
    form = LoginForm()
    user = None

    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first()

        if user:
            if user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('main.search'))
            else:
 
                flash('Invalid email or password.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')

    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))
