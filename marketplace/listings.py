import os
from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from .models import Listing,User,Bid,Sale
from .forms import ListingForm
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import app

#create a blueprint
bp = Blueprint('listing', __name__, url_prefix='/listing')


#-------------------------------------------------------------------

# TEMPORARY ENDPOINT FOR QUOI
#-----/results-----
@bp.route('/results')
def results():
  # This works from the search bar from home page
  if 'search' in request.args:
    search = request.args.get('search')
    listing = Listing.query.filter(Listing.available==True, Listing.name.ilike("%" + search + "%")).all()

  # This works from the nav bar dropdown
  if 'genre' in request.args:
    genreQuery = request.args.get('genre')
    listing = Listing.query.filter(Listing.available==True, Listing.genre==genreQuery).all()

  return render_template('listings/results.html', listing=listing)
#-----/resutls-----END

#-----/show/id-----
#create a page that will show the details for the destination
@bp.route('/<int:id>')
def show(id):
  listing = Listing.query.filter_by(id=id).first()
  return render_template('listings/show.html', listing=listing)
#-----/show/id-----END

#-----/my_listings-----
#Shows all listings belonging to current user
@bp.route('/my_listings')
@login_required   #decorator between the route and view function
def my_listings():
  if (request.args.get('search')):
    search = request.args.get('search')
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.available==True, Listing.name.like("%" + search + "%")).all()
  else:
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.available==True).all()
  return render_template('listings/currently-listed.html', listing=listing)
#-----/my_listings-----END

#-----/my_previous-----
#Shows all listings belonging to current user
@bp.route('/my_previous')
@login_required   #decorator between the route and view function
def my_previous():
  if (request.args.get('search')):
    search = request.args.get('search')
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.name.like("%" + search + "%")).all()
  else:
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.available==False).all()
  return render_template('listings/previous-listed.html', listing=listing)
#-----/my_listings-----END

#-----/bid-----
@bp.route('/bid/<int:id>', methods = ['GET', 'POST'])
@login_required   #decorator between the route and view function
def makebid(id):
  listing = Listing.query.filter_by(id=id).first()
  already_bid = Bid.query.filter_by(bidder_id=current_user.id, listing_id=id).first()
  if (listing.owner_id != current_user.id):
    if (listing != None and already_bid == None):
      bid = Bid(bidder_id=current_user.id, listing_id=id)

      db.session.add(bid)
      db.session.commit()

      flash('Bid Successful!', 'success')

      return redirect(url_for('listing.show', id=id))
    else:
      flash('Bid already exists!', 'danger')
      return redirect(url_for('listing.show', id=id))
  else:
    flash('This is your listing!', 'danger')
    return redirect(url_for('listing.show', id=id))


#-----/create-----
@bp.route('/create', methods = ['GET', 'POST'])
@login_required   #decorator between the route and view function
def create():
  listing_form = ListingForm()
  if listing_form.validate_on_submit():
    # on successful validation add data
    listing = Listing(name=listing_form.name.data,
                artist=listing_form.artist.data,
                album=listing_form.album.data,
                description=listing_form.description.data,
                condition=listing_form.condition.data,
                # image=('/tmp/' + listing_form.image.data.filename),
                image=('/static/listing_images/' + listing_form.image.data.filename),
                price=listing_form.price.data,
                genre=listing_form.genre.data,
                release_year=listing_form.release_year.data,
                owner_id=current_user.id)

    if request.method == 'POST':
      f = listing_form.image.data
      # f.save(os.path.join('/tmp/', secure_filename(f.filename)))
      f.save(os.path.join('marketplace\\static\\listing_images', secure_filename(f.filename)))

    # push to db
    db.session.add(listing)
    db.session.commit()

    flash('Successfully created new listing', 'success')

    #redirect to created listing
    return redirect(url_for('listing.show', id=listing.id))

  return render_template('listings/create.html', form=listing_form, heading='Create Listing')
#-----/create-----END

#-----/edit/id-----
@bp.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required   #decorator between the route and view function
def edit(id):
  listing = Listing.query.filter_by(id=id).first()

  #check if current user is poster of listing
  if (current_user.id == listing.owner_id):
    #check if listing is avail - stops from entering URL when btn disabled
    if (listing.available):
      listing_form = ListingForm()
      if listing_form.validate_on_submit():
        listing.name=listing_form.name.data
        listing.artist=listing_form.artist.data
        listing.description=listing_form.description.data
        listing.image=('/static/listing_images/' + listing_form.image.data.filename)
        listing.price=listing_form.price.data
        listing.genre=listing_form.genre.data
        listing.owner_id=current_user.id

        if request.method == 'POST':
          f = listing_form.image.data
          f.save(os.path.join('marketplace\\static\\listing_images', secure_filename(f.filename)))

        # update db
        db.session.commit()

        flash('Successfully edited listing', 'success')

        #redirect to created listing
        return redirect(url_for('listing.show', id=id))
    else:
      return redirect(url_for('listing.show', id=id))
  else:
    return redirect(url_for('listing.show', id=id))

  return render_template('listings/create.html', form=listing_form, heading='Edit Listing')
#-----/edit/id-----END

#-----/delete/id-----
@bp.route('/delete/<int:id>', methods = ['GET', 'POST'])
@login_required   #decorator between the route and view function
def delete(id):
  listing = Listing.query.filter_by(id=id).first()
  print(listing)
  #check if current user is poster of listing
  if (current_user.id == listing.owner_id):
    # Delete listing from db
    db.session.delete(listing)
    db.session.commit()

    flash('Successfully removed listing', 'success')

    #redirect to personal listings
    return redirect(url_for('listing.my_listings'))
  else:
    flash('Could not remove listings', 'danger')
    return redirect(url_for('listing.my_listings'))

  listing = Listing.query.filter_by(owner_id=current_user.id).all()
  return render_template('listings/currently-listed.html', listing=listing)
#-----/delete/id-----END

#-----/sell/listing_id-user_id-----
@bp.route('/sell/<int:listingid>-<int:userid>', methods = ['GET', 'POST'])
@login_required   #decorator between the route and view function
def sell(listingid, userid):
  listing = Listing.query.filter_by(id=listingid).first()
  #check if current user is poster of listing
  if (current_user.id == listing.owner_id):
    # Make listing unavailable as it is now sold
    listing.available=False

    #create sale entry
    sale = Sale(buyer_id=userid,listing_id=listingid)
    db.session.add(sale)
    db.session.commit()

    flash('Successfully sold listing', 'success')

    #redirect to personal listings
    return redirect(url_for('listing.my_listings'))
  else:
    flash('Error during sell operation', 'danger')
    return redirect(url_for('listing.my_listings'))

  listing = Listing.query.filter_by(owner_id=current_user.id).all()
  return render_template('listings/currently-listed.html', listing=listing)
#-----/sell/id-----END