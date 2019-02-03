from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Sign In')

class SignUp(FlaskForm):
    name = StringField('Name')
    secondname = StringField('Second name')
    username = StringField('Username*', validators = [DataRequired()])
    password = PasswordField('Password*', validators = [DataRequired()])
    passwordRet = PasswordField("Retype password*", validators = [DataRequired()])
    submit = SubmitField('Sign Up')

class ProblemsetID(FlaskForm):
    selectfile = FileField('Select File')
    submit = SubmitField('Submit')
