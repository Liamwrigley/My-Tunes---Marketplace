import os, re, boto3, botocore
from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from .models import Listing,User,Bid,Sale
from .forms import ListingForm, EditForm
from . import db
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import app

#create a blueprint
bp = Blueprint('listing', __name__, url_prefix='/listing')

if (os.path.exists(os.getcwd() + '/marketplace/configs/local_config.py')):
  from .configs.local_config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION
else:
  from .configs.live_config import S3_KEY, S3_SECRET, S3_BUCKET, S3_LOCATION

s3 = boto3.client(
  "s3",
  aws_access_key_id=S3_KEY,
  aws_secret_access_key=S3_SECRET
)

@bp.route('/file_upload')
def upload_file(file, bucket_name, acl="public-read"):
  try:
    s3.upload_fileobj(
      file,
      bucket_name,
      file.filename,
      ExtraArgs={
        "ACL": acl,
        "ContentType": file.content_type
      }
    )
  except Exception as e:
    print("Something happened: ", e)
    return e

  return "{}{}".format(S3_LOCATION, file.filename)


#-------------------------------------------------------------------

#-----/results-----
@bp.route('/results')
def results():
  # Open query session to chain filters together based on what arguments are in the form
  # Initially sort by available and at the end sort it by name ascending
  query = db.session.query(Listing)
  query = query.filter(Listing.available==True)
  for q in request.args:
    if (q == 'genre' and request.args.get('genre') != ''):
      query = query.filter(Listing.genre==request.args.get('genre'))
    if (q == 'year' and request.args.get('year') != ''):
      query = query.filter(Listing.release_year==request.args.get('year'))
    if (q == 'search' and request.args.get('search') != ''):
      query = query.filter(Listing.name.ilike("%" + request.args.get('search') + "%"))
    listing = query.order_by(Listing.name.asc()).all()
  return render_template('listings/results.html', listing=listing)
#-----/results-----END

#-----/show/id-----
# Shows a single listing
@bp.route('/<int:id>')
def show(id):
  listing = Listing.query.filter_by(id=id).first()
  return render_template('listings/show.html', listing=listing)
#-----/show/id-----END

#-----/my_listings-----
# Shows all listings belonging to current user
@bp.route('/my_listings')
@login_required
def my_listings():
  if (request.args.get('search')):
    search = request.args.get('search')
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.available==True, Listing.name.like("%" + search + "%")).order_by(Listing.name.asc()).all()
  else:
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.available==True).order_by(Listing.name.asc()).all()
  return render_template('listings/currently-listed.html', listing=listing)
#-----/my_listings-----END

#-----/my_previous-----
# Shows all sold listings belonging to current user
@bp.route('/my_previous')
@login_required
def my_previous():
  if (request.args.get('search')):
    search = request.args.get('search')
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.name.like("%" + search + "%")).order_by(Listing.name.asc()).all()
  else:
    listing = Listing.query.filter(Listing.owner_id==current_user.id, Listing.available==False).order_by(Listing.name.asc()).all()
  return render_template('listings/previous-listed.html', listing=listing)
#-----/my_listings-----END

#-----/bid-----
# Endpoint to bid on an item
# Adds bid details to bid DB
@bp.route('/bid/<int:id>', methods = ['GET', 'POST'])
@login_required
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
# Endpoint for listing creation
# Adds listing details to DB and saves image to local dir
@bp.route('/create', methods = ['GET', 'POST'])
@login_required
def create():
  listing_form = ListingForm()
  if listing_form.validate_on_submit():
    # on successful validation add data

    if request.method == 'POST':
      f = listing_form.image.data
      output = upload_file(f, S3_BUCKET)

    listing = Listing(name=listing_form.name.data,
                artist=listing_form.artist.data,
                album=listing_form.album.data,
                description=listing_form.description.data,
                condition=listing_form.condition.data,
                image=(output), # image path from img upload function
                price=listing_form.price.data,
                genre=listing_form.genre.data,
                release_year=listing_form.release_year.data,
                owner_id=current_user.id)
      
    # push to db
    db.session.add(listing)
    db.session.commit()

    flash('Successfully created new listing', 'success')

    #redirect to created listing
    return redirect(url_for('listing.show', id=listing.id))

  return render_template('listings/create.html', form=listing_form, heading='Create Listing')
#-----/create-----END

#-----/edit/id-----
# Shows page to edit single listing
@bp.route('/edit/<int:id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
  listing = Listing.query.filter_by(id=id).first()

  #check if current user is poster of listing
  if (current_user.id == listing.owner_id):
    #check if listing is avail - stops from entering page from URL
    if (listing.available):
      # Pre populate existing data with form init
      edit_form = EditForm(
        release_year=int(listing.release_year),
        name=listing.name,
        artist=listing.artist,
        album=listing.album,
        description=listing.description,
        condition=listing.condition,
        price=listing.price,
        genre=listing.genre
        )

      if edit_form.validate_on_submit():
        listing.name=edit_form.name.data
        listing.artist=edit_form.artist.data
        listing.album=edit_form.album.data
        listing.description=edit_form.description.data
        listing.condition=edit_form.condition.data
        # listing.image=listing.image # image path from img upload function
        listing.price=edit_form.price.data
        listing.genre=edit_form.genre.data
        # if image is unchanged as cannot add default value
        if (edit_form.image.data is None):
          listing.image=listing.image
        else:
          listing.image=upload_file(edit_form.image.data, S3_BUCKET)
        listing.release_year=edit_form.release_year.data
        listing.owner_id=current_user.id

        # update db
        db.session.commit()

        flash('Successfully edited listing', 'success')

        #redirect to created listing
        return redirect(url_for('listing.show', id=id))
    else:
      return redirect(url_for('listing.show', id=id))
  else:
    return redirect(url_for('listing.show', id=id))

  return render_template('listings/create.html', form=edit_form, heading='Edit Listing')
#-----/edit/id-----END

#-----/delete/id-----
# Endpoint to delete a listing
# Will delete a listing from the DB
@bp.route('/delete/<int:id>', methods = ['GET', 'POST'])
@login_required
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
# Endpoint to select a buyer for a listing
# Takes listing ID and user ID as params
# Sets listing to unavailable and adds details to sales DB
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