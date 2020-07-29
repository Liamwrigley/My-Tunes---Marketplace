from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    phone = db.Column(db.Integer(), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)
    authenticated = db.Column(db.Boolean, index=True, default=False, nullable=False)

    def __repr__(self): #string print method
        return "<ID: {}, Name: {}, EmailID: {}, pwhash: {}>".format(self.id, self.name, self.emailid, self.password_hash)

    def is_active(self):
        """True as all users are active"""
        return True

    def get_id(self):
        """Return the user_ID tp satisfy Flask-Login's requirements"""
        return self.id

    def is_authenticated(self):
        """Return True if the user is authenticated"""
        return self.authenticated

    def is_anonymous(self):
        """Return False as anon users are not supported"""
        return False


class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, index=True, primary_key=True)
    name = db.Column(db.String(80), index=True)
    artist = db.Column(db.String(80), index=True)
    album = db.Column(db.String(80), index=True)
    description = db.Column(db.String(200), index=True)
    condition = db.Column(db.String(50), index=True)
    image = db.Column(db.String(400), index=True)
    price = db.Column(db.String(10), index=True)
    genre = db.Column(db.String(25), index=True)
    release_year = db.Column(db.Integer(), index=True)
    created_at = db.Column(db.DateTime, index=True, default=datetime.now())
    available = db.Column(db.Boolean, index=True, default=True, nullable=False)

    # Creates relation between User and Listing
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', foreign_keys=[owner_id])

    bids = db.relationship('Bid', backref='listings')
    sales = db.relationship('Sale', backref='listings')

    def __repr__(self): #string print method
        return "<ID: {}, Name: {}, Artist: {}, Description: {}, img: {}, price: {}, genre: {}, create date: {}>".format(self.id, self.name, self.artist, self.description, self.image, self.price, self.genre, self.created_at)


class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, index=True, primary_key=True)
    bid_time = db.Column(db.DateTime, default=datetime.now())

    #foreign keys
    bidder_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    # # Creates relation between User and Bid
    bidder = db.relationship('User', foreign_keys=[bidder_id])

    # # Creates relation between Listing and Bid
    listing = db.relationship('Listing', foreign_keys=[listing_id])

    def __repr__(self): #string print method
        return "<ID: {}, bidder_id: {}, listing_id: {}, bid_time: {}\nbidderRELATION: {}\nlistingRELATION: {}>".format(self.id, self.bidder_id, self.listing_id, self.bid_time, self.bidder, self.listing)


class Sale(db.Model):
    __tablename__ = 'sales'
    id = db.Column(db.Integer, index=True, primary_key=True)
    sale_date = db.Column(db.DateTime, default=datetime.now())

    #foreign keys
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    listing_id = db.Column(db.Integer, db.ForeignKey('listings.id'))

    # # Creates relation between User and Sale
    buyer = db.relationship('User', foreign_keys=[buyer_id])

    # # Creates relation between Listing and Sale
    listing = db.relationship('Listing', foreign_keys=[listing_id])

    def __repr__(self): #string print method
        return "<ID: {}, buyer_id: {}, listing_id: {}, sale_date: {}\nbuyerRELATION: {}\nlistingRELATION: {}>".format(self.id, self.buyer_id, self.listing_id, self.sale_date, self.buyer, self.listing)
