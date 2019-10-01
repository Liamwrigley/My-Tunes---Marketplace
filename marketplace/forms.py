
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

#listing creation form
class ListingForm(FlaskForm):
  name = StringField('Song', validators=[InputRequired()])
  description = TextAreaField('Description', 
            validators=[InputRequired(), Length(min=10, max=200)])
  image = StringField('Cover Image', validators=[InputRequired()])
  price = StringField('Price', validators=[InputRequired()])
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