import os 

# Heroku
S3_BUCKET = os.environ['S3_BUCKET']
S3_LOCATION = os.environ['S3_LOCATION']
DATABASE_URL= os.environ['DATABASE_URL']
S3_KEY = os.environ['S3_KEY']
S3_SECRET = os.environ['S3_SECRET']

DEBUG=False
WTF_CSRF_SECRET_KEY = os.environ['WTF_CSRF_SECRET_KEY']