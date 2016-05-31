# project/user/forms.py


from flask_wtf import Form
from wtforms import fields, validators, TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from project.models import User


class LoginForm(Form):
    username = TextField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

class SignupForm(Form):
  username = TextField('username',  validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])
  confirm = PasswordField('Repeat password', validators=[
            DataRequired(),
            EqualTo('password', message='Passwords must match.')
        ])
  submit = SubmitField("Create account")

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
 
  def validate(self):
    if not Form.validate(self):
      return False
     
    user = User.query.filter_by(username = self.username.data.lower()).first()
    if user:
      self.username.errors.append("That username is already taken")
      return False
    return True

class ChangePasswordForm(Form):
  username = TextField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

  new = PasswordField('new_password', validators=[DataRequired()])
  confirm = PasswordField('Repeat password', validators=[
            DataRequired(),
            EqualTo('new', message='Passwords must match.')
        ])
  submit = SubmitField('Change Password')
