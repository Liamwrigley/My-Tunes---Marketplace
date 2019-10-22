from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField,FloatField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Required
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from datetime import datetime

#Used as a price field - replaces ',' with '' to not throw errors and not have commas in the price field
class PriceFloatField(FloatField):
  def process_formdata(self, valuelist):
    if valuelist:
      try:
        self.data = float(valuelist[0].replace(',', ''))
      except ValueError:
        self.data = None
        raise ValueError(self.gettext('Not a valid price value'))

#Used to validate the length of the  phone number then verify that it is an integer
class PhoneFieldField(IntegerField):
  def process_formdata(self, valuelist):
    if valuelist:
      if len(str(valuelist[0])) < 8 or len(str(valuelist[0])) > 10:
        self.data = None
        raise ValueError(self.gettext('Please enter a valid phone number'))
      else:
        try:
          int(valuelist[0])
          self.data = valuelist[0]
        except:
          self.data = None
          raise ValueError(self.gettext('Please enter a valid phone number'))
        
          

#listing creation form
class ListingForm(FlaskForm):

  name = StringField('Song', validators=[InputRequired()])
  artist = StringField('Artist Name', validators=[InputRequired()])
  album = StringField('Album Name', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired(), Length(min=10, max=200)])
  condition = TextAreaField('Item Condition',
             validators=[InputRequired(), Length(min=1, max=50)])
  image = FileField('Image', validators=[
    FileRequired(),
    FileAllowed(['jpg','png'], "Image files only")])
  price = PriceFloatField('Price', validators=[InputRequired()])
  genre = StringField('Genre', validators=[InputRequired()])
  release_year = SelectField('Release Year')
  submit = SubmitField("Create")

  def __init__(self, *args, **kwargs):
    super(ListingForm, self).__init__(*args, **kwargs)
    now = datetime.utcnow()
    self.release_year.choices = [(str(i), i) for i in range(now.year, now.year - 100, -1)]
    self.release_year.validators = [InputRequired()]
#Login form
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 #Register form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone = PhoneFieldField('Phone Number', validators=[InputRequired()])
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")