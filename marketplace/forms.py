from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField,FloatField, SelectField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Required, Optional
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from datetime import datetime
import re

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
        
#Used to sanitise username field
class UsernameField(StringField):
  def process_formdata(self, valuelist):
    if valuelist:
      if (valuelist[0].isalnum()):
        if len(str(valuelist[0])) < 4 or len(str(valuelist[0])) > 12:
          self.data = None
          raise ValueError(self.gettext('Please enter a username between 4 and 12 characters'))
        else:
          self.data = valuelist[0]
      else:
        self.data = None
        raise ValueError(self.gettext('Please enter an alphanumberic username'))

#Used to sanitise string fields
class SanitizedString(StringField):
  def process_formdata(self, valuelist):
    if valuelist:
      #All inputs should have a max validator on it
      if (self.validators[1].max != None):
        max = self.validators[1].max
        #Check that input value is less than max
        if (len(str(valuelist[0])) > int(max)):
          self.data = None
          #Displays error message with dynamic input field name and max value
          raise ValueError(self.gettext(self.label.text+" must be less than "+str(max)+" characters"))
        else :
          keepcharacters = (' ','-','_','!')
          checkValid = ""
          if (checkValid.join(c for c in valuelist[0] if c.isalnum() or c in keepcharacters).rstrip() == ""):
            self.data = None
            raise ValueError(self.gettext('Please enter a valid input. Accepts: " ", "_", "-", "!" as special characters'))
          else:
            self.data = valuelist[0]

#Used to sanitise textarea fields
class SanitizedTextArea(TextAreaField):
  def process_formdata(self, valuelist):
    if valuelist:
      #All inputs should have a max validator on it
      if (self.validators[1].max != None):
        max = self.validators[1].max
        #Check that input value is less than max
        if (len(str(valuelist[0])) > int(max)):
          self.data = None
          #Displays error message with dynamic input field name and max value
          raise ValueError(self.gettext(self.label.text+" must be less than "+str(max)+" characters"))
        else :
          keepcharacters = (' ','-','_','!')
          checkValid = ""
          if (checkValid.join(c for c in valuelist[0] if c.isalnum() or c in keepcharacters).rstrip() == ""):
            self.data = None
            raise ValueError(self.gettext('Please enter a valid input. Accepts: " ", "_", "-", "!" as special characters'))
          else:
            self.data = valuelist[0]

#listing creation form
class ListingForm(FlaskForm):
  name = SanitizedString('Song', validators=[InputRequired(), Length(max=50)])
  artist = SanitizedString('Artist Name', validators=[InputRequired(), Length(max=50)])
  album = SanitizedString('Album Name', validators=[InputRequired(), Length(max=50)])
  description = SanitizedTextArea('Description', 
            validators=[InputRequired(), Length(max=200)])
  condition = SanitizedTextArea('Item Condition',
             validators=[InputRequired(), Length(max=50)])
  image = FileField('Image', validators=[
    FileRequired(),
    FileAllowed(['jpg','png'], "Image files only")])
  price = PriceFloatField('Price', validators=[InputRequired()])
  genre = SanitizedString('Genre', validators=[InputRequired(), Length(max=50)])
  release_year = SelectField('Release Year')
  submit = SubmitField("Create")

  def __init__(self, *args, **kwargs):
    super(ListingForm, self).__init__(*args, **kwargs)
    now = datetime.utcnow()
    self.release_year.choices = [(str(i), i) for i in range(now.year, now.year - 100, -1)]
    self.release_year.validators = [InputRequired()]


#Edit form
# Needed to make a new form for editing as images were required in listing 
# creation and Optional validator was not working as intended.
class EditForm(FlaskForm):
  name = SanitizedString('Song', validators=[InputRequired(), Length(max=50)])
  artist = SanitizedString('Artist Name', validators=[InputRequired(), Length(max=50)])
  album = SanitizedString('Album Name', validators=[InputRequired(), Length(max=50)])
  description = SanitizedTextArea('Description', 
            validators=[InputRequired(), Length(max=200)])
  condition = SanitizedTextArea('Item Condition',
             validators=[InputRequired(), Length(max=50)])
  image = FileField('Image - leaving blank will keep current image', validators=[
    Optional(),
    FileAllowed(['jpg','png'], "Image files only")])
  price = PriceFloatField('Price', validators=[InputRequired()])
  genre = SanitizedString('Genre', validators=[InputRequired(), Length(max=50)])
  release_year = SelectField('Release Year')
  submit = SubmitField("Update")

  def __init__(self, *args, **kwargs):
    super(EditForm, self).__init__(*args, **kwargs)
    now = datetime.utcnow()
    self.release_year.choices = [(str(i), i) for i in range(now.year, now.year - 100, -1)]

#Login form
class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[InputRequired('Enter user name')])
    password = PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 #Register form
class RegisterForm(FlaskForm):
    user_name = UsernameField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    phone = PhoneFieldField('Phone Number', validators=[InputRequired()])
    #linking two fields - password should be equal to data entered in confirm
    password = PasswordField("Password", validators=[InputRequired(), Length(min=4, max=50),
                  EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")