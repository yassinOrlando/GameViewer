from flask_wtf import FlaskForm
from flask import session
from wtforms import StringField, PasswordField, SubmitField, FileField, TextAreaField, SelectField, HiddenField
from wtforms.validators import DataRequired, Email, Required
from wtforms.fields.html5 import EmailField
from models import Categories, Users

class signInForm(FlaskForm):
    nickname = StringField('Nickname', validators=[DataRequired()], render_kw={"placeholder": "Nickname"})
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    img = FileField('Profile image', validators=[Required()] )
    submit = SubmitField('Sign up')

class logInForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField('Log in')

class createReview(FlaskForm):
    cats = Categories.query.all()
    options = []
    for cat in cats:
            options.append(tuple((cat.id, cat.name)))


    title = StringField('Title', validators=[DataRequired()], render_kw={"placeholder": "Title"})
    img = FileField('Review img', validators=[Required()])
    content = TextAreaField('Content', validators=[DataRequired()], render_kw={"placeholder": "Content"})
    category = SelectField(
        u'Category',
        choices = options
    )
    submit = SubmitField('Save', render_kw={"class": "success"})

class updateImg(FlaskForm):
    img = FileField('Review img')