from flask import Blueprint, redirect, url_for, render_template

bp = Blueprint('main', __name__, template_folder="templates")

# https://hackersandslackers.com/the-art-of-building-flask-routes

@bp.route('/')
def home():
  # adding index.html - need to make into a template
    return render_template('index.html')

@bp.route('/login')
def login():
    return '<h1>LOGIN<h1>'

@bp.route('/logout')
def logout():
    return redirect('/login')