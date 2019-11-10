import os 

S3_BUCKET = 'iab207'
S3_LOCATION = 'http://{}.s3.amazonaws.com/'.format(S3_BUCKET)

# Heroku
DATABASE_URL= os.environ['DATABASE_URL']
S3_KEY = os.environ['S3_KEY']
S3_SECRET = os.environ['S3_SECRET']