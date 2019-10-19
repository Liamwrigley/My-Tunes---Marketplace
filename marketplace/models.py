from . import db
from datetime import datetime
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    #comments = db.relationship('Comment', backref='user')

    def __repr__(self): #string print method
        return "<ID: {}, Name: {}, EmailID: {}, pwhash: {}>".format(self.id, self.name, self.emailid, self.password_hash)


class Listing(db.Model):
    __tablename__ = 'listings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    artist = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    price = db.Column(db.String(10))
    genre = db.Column(db.String(25))
    created_at = db.Column(db.DateTime, default=datetime.now())
    available = db.Column(db.Boolean, default=True, nullable=False)

    # Creates relation between User and Listing
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = db.relationship('User', foreign_keys=[owner_id])

    bids = db.relationship('Bid', backref='listings')

    # ... Create the Comments db.relationship
	  # relation to call destination.comments and comment.destination
    #comments = db.relationship('Comment', backref='destination')

    def __repr__(self): #string print method
        return "<ID: {}, Name: {}, Artist: {}, Description: {}, img: {}, price: {}, genre: {}, create date: {}>".format(self.id, self.name, self.artist, self.description, self.image, self.price, self.genre, self.created_at)


class Bid(db.Model):
    __tablename__ = 'bids'
    id = db.Column(db.Integer, primary_key=True)
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




# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     text = db.Column(db.String(400))
#     created_at = db.Column(db.DateTime, default=datetime.now())
#     #add the foreign keys
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
#     destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'))


#     def __repr__(self):
#         return "<Comment: {}>".format(self.text)
