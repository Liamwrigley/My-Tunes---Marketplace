import os
import os.path
import datetime

# uncomment for heroku
import psycopg2


#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CsrfProtect
from .util.filters import datetimeformat, excerpt

if (os.path.exists(os.getcwd() + '/marketplace/configs/local_config.py')):
    from .configs.local_config import DATABASE_URL, DEBUG
else:
    from .configs.live_config import DATABASE_URL, DEBUG

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():

    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=DEBUG
    WTF_CSRF_ENABLED = True
    app.secret_key=os.urandom(32)

    csrf = CsrfProtect()
    csrf.init_app(app)
    #set the app configuration data

    app.config['SQLALCHEMY_DATABASE_URI']=DATABASE_URL

    #initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    #initialize the login manager
    login_manager = LoginManager()

    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    #create a user loader function takes userid and returns User
    #from .models import User, Listing  # importing here to avoid circular references
    from .models import User, Listing
    # from flask_login import current_user

    @login_manager.user_loader
    def load_user(user_id):
        # return User.query.get(id=user_id)
        return User.query.filter_by(id=user_id).first()

    # Error handing - passes through error code and template forms based on code
    @app.errorhandler(Exception)
    def handle_error(e):
        return render_template("error.html", error=e)

    @app.context_processor
    def get_genres():
        genres = Listing.query.with_entities(Listing.genre).filter(Listing.available==True).order_by(Listing.genre.desc()).distinct()
        years = Listing.query.with_entities(Listing.release_year).filter(Listing.available==True).order_by(Listing.release_year.desc()).distinct()
        return dict(nav_genres=genres, nav_years=years)

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from .listings import bp
    app.register_blueprint(bp)

    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['excerpt'] = excerpt

    return app
