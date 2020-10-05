from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Required
from wtforms.fields.html5 import EmailField

class signInForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()], render_kw={"placeholder": "Nickname"})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    img = FileField('Profile image', validators=[Required()] )
    submit = SubmitField('Sign up')