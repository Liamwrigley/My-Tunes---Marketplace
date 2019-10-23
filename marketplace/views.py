from flask import Blueprint, redirect, url_for, render_template
from .models import Listing

bp = Blueprint('main', __name__, template_folder="templates")

# https://hackersandslackers.com/the-art-of-building-flask-routes

@bp.route('/', endpoint="home")
def home():
    listing = Listing.query.filter(Listing.available==True).order_by(Listing.name.asc()).all()
    return render_template('index.html', listing=listing)
