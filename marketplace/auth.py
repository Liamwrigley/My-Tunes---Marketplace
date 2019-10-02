from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from werkzeug.security import generate_password_hash,check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required,logout_user
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    error=None
    if (login_form.validate_on_submit() == True):
        #get username and password from DB
        user_name = login_form.user_name.data
        pw = login_form.password.data
        user_check = User.query.filter_by(name=user_name).first()

        #if username or password is wrong, should give a vague answer as to which one
        if user_check is None:
            error="Incorrect username or password"

        #check hashed pw against db pw
        #password should be hashed in the DB so we never store a plaintext PW
        elif not check_password_hash(user_check.password_hash, pw):
            error="Incorrect username or password"
        if error is None:
            login_user(user_check)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html')

@bp.route('/register', methods=['GET','POST'])
def register():
    register = registerForm()
    if (register.validate_on_submit() == True):
        user_name = register.user_name.data
        pw = register.pw.data
        email = register.email.data

        #check if username already exists within DB
        user_check = User.query.filter_by(name=user_name).first()
        email_check = User.query.filter_by(emailid=email).first()

        #if user_check returns a user - redirect to register
        if user_check:
            flash('This user already exists, please use a different username or login')
            return redirect(url_for('auth.register'))

        #if email_check returns a user - redirect to register
        if email_check:
            flash('This email is already in use, please use a different email or login')
            return redirect(url_for('auth.register'))

        #if user_check does not return a user - insert data into DB
        pw_hash = generate_password_hash(pw)
        new_user = User(name=user_name, password_hash=pw_hash, emailid=email)
        db.session.add(new_user)
        db.session.commit()
        #once commited to DB - redirect to login
        return redirect(url_for('auth.login'))
    else:
        return render_template('user.html', form=register, heading='Register')





@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
