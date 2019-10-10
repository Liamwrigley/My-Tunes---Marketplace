import os
from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from .models import Listing,User #add Comment back later
from .forms import ListingForm #add comment form later
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import app

#create a blueprint
bp = Blueprint('listing', __name__, url_prefix='/listing')

#create a page that will show the details fo the destination
@bp.route('/<int:id>')
def show(id):
  listing = Listing.query.filter_by(id=id).first()
  # cform = CommentForm()
  return render_template('listings/show.html', listing=listing) #, form=cfor


@bp.route('/create', methods = ['GET', 'POST'])
@login_required   #decorator between the route and view function
def create():
  listing_form = ListingForm()
  if listing_form.validate_on_submit():
    # on successful validation add data
    listing = Listing(name=listing_form.name.data,
                description=listing_form.description.data,
                image=('/listing_images/' + listing_form.image.data.filename),
                price=listing_form.price.data,
                genre=listing_form.genre.data,
                owner_id=current_user.id)

    if request.method == 'POST':
      f = listing_form.image.data
      f.save(os.path.join('marketplace\\listing_images', secure_filename(f.filename)))

    # push to db
    db.session.add(listing)
    db.session.commit()

    flash('Successfully created new listing', 'success')
    return redirect(url_for('main.home')) #probably change this to route somewhere else

  return render_template('listings/create.html', form=listing_form, heading='Create Listing')

# @bp.route('/<destination>/comment', methods = ['GET', 'POST'])
# @login_required
# def comment(destination):
#     form = CommentForm()
#     #get the destination object associated to the page and the comment
#     destination_obj = Destination.query.filter_by(id=destination).first()
#     if form.validate_on_submit():
#       #read the comment from the form
#       comment = Comment(text=form.text.data,
#                         destination=destination_obj, user=current_user)
#       #here the back-referencing works - comment.destination is set
#       # and the link is created
#       db.session.add(comment)
#       db.session.commit()

#       #flashing a message which needs to be handled by the html
#       flash('Your comment has been added', 'success')
#     # using redirect sends a GET request to destination.show
#     return redirect(url_for('destination.show', id=destination))
