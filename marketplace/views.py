from flask import Blueprint, redirect, url_for, render_template
from .models import Listing

bp = Blueprint('main', __name__, template_folder="templates")

# https://hackersandslackers.com/the-art-of-building-flask-routes

@bp.route('/', endpoint="home")
def home():
    listing = Listing.query.filter_by(available=True).all()
    genres = Listing.query.with_entities(Listing.genre).distinct()
    return render_template('index.html', listing=listing, genres=genres)