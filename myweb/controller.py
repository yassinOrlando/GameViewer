from main import app
import os
from models import *
from flask import render_template, redirect, request, url_for, flash, session, g
from forms import *
from werkzeug.utils import secure_filename
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import exc

#Routes for root pages
@app.route("/")
def index():
    categ = Categories.query.all()
    users = Users.query.all()
    name_page = "Home"
    return render_template("index.html", page = name_page, cats = categ, users = users)

@app.route("/category/<cat_name>")
def category(cat_name):
    categ = Categories.query.all()
    category = cat_name 
    return render_template("category.html", categ_name = category, cats = categ)

@app.route("/review/<review_title>")
def review(review_title):
    title = review_title
    return render_template("read-review.html", title = title)



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
        session['user'] = request.form['email']
        flash('You are logged in!')
        return redirect(url_for('admin'))

    return render_template("login/login.html", form = form)

@app.route("/logout")
def logout():
    session.pop('user', None)
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
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                app.config['UPLOAD_FOLDER'], filename
            ))
            user = Users(req['nickname'], req['email'], generate_password_hash(req['password']), filename)
        
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


#Routes for the admin
@app.route("/admin")
def admin(): 
    return render_template("admin/user.html")

@app.route("/my-posts")
def myPosts(): 
    return render_template("admin/my-posts.html")

@app.route("/new-review")
def newReview(): 
    return render_template("admin/new-review.html")

@app.route("/edit-review/<id>")
def editReview(id):
    r_id = id 
    return render_template("admin/edit-review.html", id = r_id)

app.run(debug=True)