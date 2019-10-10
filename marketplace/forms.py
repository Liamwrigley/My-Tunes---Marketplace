
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField,FloatField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

#Used as a price field - replaces ',' with '' to not throw errors and not have commas in the price field
class PriceFloatField(FloatField):
  def process_formdata(self, valuelist):
    if valuelist:
      try:
        self.data = float(valuelist[0].replace(',', ''))
      except ValueError:
        self.data = None
        raise ValueError(self.gettext('Not a valid price value'))

#listing creation form
class ListingForm(FlaskForm):
  name = StringField('Song', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired(), Length(min=10, max=200)])
  image = FileField('Image', validators=[
    FileRequired(),
    FileAllowed(['jpg','png'], "Image files only")])
  price = PriceFloatField('Price', validators=[InputRequired()])
  genre = StringField('Genre', validators=[InputRequired()])
  submit = SubmitField("Create")

#Login form
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 #Register form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
    
    #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                  EqualTo('confirm', message="Passwords do not match")])
    confirm = PasswordField("Confirm Password")
    #submit button
    submit = SubmitField("Register")