from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_user, logout_user, login_required
from sqlalchemy import func
from app import db
from app.models import User
from wtforms.validators import DataRequired
from app.forms import RegistrationForm, LoginForm
bp = Blueprint('auth', __name__)


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
def login():
    form = LoginForm()
    user = None

    if form.validate_on_submit():
        user = User.query.filter(func.lower(User.email) == func.lower(form.email.data)).first()

        if user:
            if user.check_password(form.password.data):
                user.failed_attempts = 0
                user.last_attempt = datetime.now()
                db.session.commit()
                login_user(user, remember=form.remember_me.data)
                return redirect(url_for('main.search'))
            else:
                user.failed_attempts += 1
                user.last_attempt = datetime.now()
                db.session.commit()
                flash('Invalid email or password.', 'danger')
        else:
            flash('Invalid email or password.', 'danger')

    # Show the reCAPTCHA field if the user failed too many login attempts
    if user and user.failed_attempts >= current_app.config['MAX_FAILED_ATTEMPTS']:
        form.recaptcha.validators = [DataRequired()]
    print(current_app.config['RECAPTCHA_PUBLIC_KEY'])

    return render_template('login.html', form=form)
