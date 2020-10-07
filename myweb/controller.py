from main import app
import os
from models import *
from flask import render_template, redirect, request, url_for, jsonify, flash, session, g, make_response
from forms import *
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc
from json import JSONEncoder
from datetime import datetime

#Routes for root pages
@app.route("/")
def index():
    categ = Categories.query.all()
    if session.get('user') != None :
        user = Users.query.filter_by(id = session['user']).first()
    else:
        user = {"id": "0"}
    name_page = "Home"
    reviews = Reviews.query.all()

    return render_template("index.html", page = name_page, cats = categ, user = user, reviews = reviews)

@app.route("/category/<cat_name>")
def category(cat_name):
    if session.get('user') != None :
        user = Users.query.filter_by(id = session['user']).first()
    else:
        user = {"id": "0"}

    get_cat = Categories.query.filter_by(name = cat_name ).first()
    reviews = Reviews.query.filter_by(id_cat = get_cat.id )
    categ = Categories.query.all()
    category = cat_name 
    return render_template("category.html", categ_name = category, cats = categ, user = user, reviews = reviews)

@app.route("/review/<review_title>/<id>")
def review(review_title, id):
    review = Reviews.query.filter_by(id = id).first()
    categ = Categories.query.all()
    if session.get('user') != None :
        user = Users.query.filter_by(id = session['user']).first()
    else:
        user = {"id": "0"}

    return render_template("read-review.html", cats = categ, review = review, user = user)


#----------------------------------------------------------------------
#Routes for login

@app.route("/login")
def login():
    form = logInForm()
    return render_template("login/login.html", form = form)

@app.route("/user-log", methods=['GET', 'POST'])
def logUser():
    form = logInForm()
    if request.method == "POST":
        req = request.form
        user = Users.query.filter_by(email = req['email']).first()

        try:
            if check_password_hash(user.password, req['password']):
                session['user'] = user.id
                flash('You are logged in!')
                return redirect(url_for('admin', id = user.id ))

            else:
                flash('Password error!')
        except exc.NonType:
            flash('Email error!')
        

    return render_template("login/login.html", form = form)

@app.route("/logout")
def logout():
    session.pop('user', None)
    flash('You logged out!')
    return redirect(url_for('login'))

@app.route("/signin")
def signIn():
    form = signInForm()
    return render_template("login/signin.html", form = form)

@app.route("/add-user", methods=('GET', 'POST'))
def addUser():
    form = signInForm()
    if request.method == "POST":
        req = request.form
        user = set()
        
        if form.validate_on_submit():
            f = form.img.data
            filename = str(secure_filename(f.filename))
            f.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))
            user = Users(req['nickname'], req['email'], generate_password_hash(req['password']), 'static/img/'+filename)
        
        try:
            db.session.add(user)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            flash('This email is already used')
            return render_template("login/signin.html", form = form)

        flash('Account created successfully! Now log in')
        return redirect(url_for("login"))
    return render_template("login/signin.html", form = form)


#----------------------------------------------------------------------
#Routes for the admin

@app.route("/admin/<id>")
def admin(id):
    user = Users.query.filter_by(id = id).first()
    return render_template("admin/user.html", user = user)

@app.route("/admin/my-posts/<id>")
def myPosts(id): 
    user = Users.query.filter_by(id = id).first()
    reviews = Reviews.query.filter_by(id_user = user.id)
    return render_template("admin/my-posts.html", user = user, reviews = reviews)

@app.route("/admin/new-review/<user_id>")
def newReview(user_id):
    user =  Users.query.filter_by(id = user_id).first()
    cats = Categories.query.all()
    form = createReview()
    return render_template("admin/new-review.html", user = user, cats = cats, form =  form)


@app.route("/post-review", methods=('GET', 'POST'))
def postReview():
    user = Users.query.filter_by(id = session['user']).first()
    form = signInForm()
    if request.method == "POST":
        req = request.form
        review = set()
        """if form.validate_on_submit():
            f = form.img.data
            filename = str(secure_filename(f.filename))
            f.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))
            review = Reviews(request.form.get('id_user'), request.form.get('category'), req['title'], 'static/img/'+filename, req['content'])

            db.session.add(review)
            db.session.commit()

            flash('Review posted')
        else:"""
        f = form.img.data
        filename = str(secure_filename(f.filename))
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        review = Reviews(request.form.get('id_user'), request.form.get('category'), req['title'], 'static/img/'+filename, req['content'], datetime.today().strftime('%Y-%m-%d'))

        db.session.add(review)
        db.session.commit()

        flash('Review posted')
    else:
        flash('Fatal error')
    return redirect(url_for('myPosts', id = user.id))

@app.route("/delete-review/<id>")
def deleteReview(id):
    review = Reviews.query.filter_by(id = id).first()
    db.session.delete(review)
    db.session.commit()
    flash('Post deleted')
    return redirect(url_for('myPosts', id = review.id_user))

@app.route("/edit-review/<id>")
def editReview(id):
    r_id = id 
    return render_template("admin/edit-review.html", id = r_id)

app.run(debug=True)