from main import app
import os
from models import *
from flask import render_template, redirect, request, url_for, jsonify, flash, session, g, make_response
from forms import *
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc, desc
from json import JSONEncoder
from datetime import datetime
from functools import wraps


#-------------------------------------
#middleware
def isAuth(f):
    @wraps(f)
    def wrap(*args, **kwargs):        # if user is not logged in, redirect to login page
        if session.get('user') != None:
            pass
        else:
            return redirect(url_for('index'))     # finally call f. f() now haves access to g.user
        return f(*args, **kwargs)
   
    return wrap

def isVisitor(f):
    @wraps(f)
    def wrap(*args, **kwargs):        # if user is not logged in, redirect to login page      
        if session.get('user') != None :
            return redirect(url_for('index'))     # finally call f. f() now haves access to g.user
        else:
            pass
        return f(*args, **kwargs)
   
    return wrap

def userAuth(id):
    link_id = Users.query.filter_by(id = id).first()
    actual_user = Users.query.filter_by(id = session['user']).first()
    print(actual_user.id)
    print(session.get('user'))
    if link_id.id == actual_user.id:
        print('You passed')
        return True
    else:
        print('no no no, you are not going there :)')
        session.pop('user', None)
        return False


#-------------------------------------
#Routes for root pages
@app.route("/")
def index():
    categ = Categories.query.all()
    if session.get('user') != None :
        user = Users.query.filter_by(id = session['user']).first()
    else:
        user = {"id": "0"}
    
    reviews = Reviews.query.order_by(desc('id'))
    return render_template("index.html", cats = categ, user = user, reviews = reviews)

@app.route("/category/<cat_name>")
def category(cat_name):
    if session.get('user') != None :
        user = Users.query.filter_by(id = session['user']).first()
    else:
        user = {"id": "0"}

    get_cat = Categories.query.filter_by(name = cat_name ).first()
    reviews = Reviews.query.filter_by(id_cat = get_cat.id ).order_by(desc('id'))
    categ = Categories.query.all()
    category = cat_name 
    return render_template("category.html", categ_name = category, cats = categ, user = user, reviews = reviews)

@app.route("/review/<review_title>/<id>")
def review(review_title, id):
    review = Reviews.query.filter_by(id = id).first()
    rev_author = Users.query.filter_by(id = review.id_user).first()
    rev_cat = Categories.query.filter_by(id = review.id_cat).first()
    cats = Categories.query.all()
    if session.get('user') != None :
        user = Users.query.filter_by(id = session['user']).first()
    else:
        user = {"id": "0"}

    return render_template("read-review.html", cats = cats, review = review, user = user, rev_author = rev_author, rev_cat = rev_cat.name)


#----------------------------------------------------------------------
#Routes for login

@app.route("/login")
@isVisitor
def login():
    form = logInForm()
    return render_template("login/login.html", form = form)

@app.route("/user-log", methods=['GET', 'POST'])
@isVisitor
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
@isAuth
def logout():
    session.pop('user', None)
    flash('You logged out!')
    return redirect(url_for('login'))

@app.route("/signin")
@isVisitor
def signIn():
    form = signInForm()
    return render_template("login/signin.html", form = form)

@app.route("/add-user", methods=('GET', 'POST'))
@isVisitor
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
            user = Users(req['nickname'], req['email'], generate_password_hash(req['password']), 'img/'+filename)
        
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
@isAuth
def admin(id):
    if userAuth(id) == False:
        return redirect(url_for('index'))

    user = Users.query.filter_by(id = id).first()
    return render_template("admin/user.html", user = user)

@app.route("/admin/my-posts/<id>")
@isAuth
def myPosts(id): 
    if userAuth(id) == False:
        return redirect(url_for('index'))
    user = Users.query.filter_by(id = id).first()
    reviews = Reviews.query.filter_by(id_user = user.id).order_by(desc('id'))
    return render_template("admin/my-posts.html", user = user, reviews = reviews)

@app.route("/admin/new-review/<user_id>")
@isAuth
def newReview(user_id):
    if userAuth(user_id) == False:
        return redirect(url_for('index'))
    user =  Users.query.filter_by(id = user_id).first()
    cats = Categories.query.all()
    form = createReview()
    return render_template("admin/new-review.html", user = user, cats = cats, form =  form)


@app.route("/post-review", methods=('GET', 'POST'))
@isAuth
def postReview():
    user = Users.query.filter_by(id = session['user']).first()
    form = signInForm()
    if request.method == "POST":
        req = request.form
        review = set()
        #if form.validate_on_submit():
         #   f = form.img.data
          #  filename = str(secure_filename(f.filename))
            #f.save(os.path.join(
            #    app.config['UPLOAD_FOLDER'], filename
            #))
            #review = Reviews(request.form.get('id_user'), request.form.get('category'), req['title'], 'static/img/'+filename, req['content'])

            #db.session.add(review)
            #db.session.commit()

            #flash('Review posted')
        #else:"""
        f = form.img.data
        filename = str(secure_filename(f.filename))
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        review = Reviews(request.form.get('id_user'), request.form.get('category'), req['title'], 'img/'+filename, req['content'], datetime.today().strftime('%Y-%m-%d'))

        db.session.add(review)
        db.session.commit()

        flash('Review posted')
    else:
        flash('Fatal error')
    return redirect(url_for('myPosts', id = user.id))

@app.route("/delete-review/<id>")
@isAuth
def deleteReview(id):
    review = Reviews.query.filter_by(id = id).first()
    db.session.delete(review)
    db.session.commit()
    flash('Post deleted')
    return redirect(url_for('myPosts', id = review.id_user))

@app.route("/edit-review/<id>")
@isAuth
def editReview(id):
    user = Users.query.filter_by(id = session['user']).first()
    review = Reviews.query.filter_by(id = id).first()
    if userAuth(review.id_user) == False:
        return redirect(url_for('index'))
    cats = Categories.query.all()
    return render_template("admin/edit-review.html", review = review, user = user, cats = cats)

@app.route("/update-review", methods=('GET', 'POST'))
@isAuth
def updateReview():
    user = Users.query.filter_by(id = session['user']).first()
    form = updateImg()
    if request.method == "POST":
        f = form.img.data
        filename = str(secure_filename(f.filename))
        f.save(os.path.join(
            app.config['UPLOAD_FOLDER'], filename
        ))
        review = Reviews.query.filter_by(id = request.form.get('id')).first()
        review.id_cat = request.form.get('category')
        db.session.commit()
        review.title = request.form.get('title')
        db.session.commit()
        review.img = 'img/'+filename
        review.content = request.form.get('content')
        db.session.commit()

        flash('Review updated')
    else:
        flash('Fatal error')
    return redirect(url_for('myPosts', id = user.id))



app.run(debug=True)