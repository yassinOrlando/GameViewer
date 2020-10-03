from flask import Flask, render_template

app = Flask(__name__)

#Routes for root pages
@app.route("/")
def index():
    name_page = "Home"
    return render_template("index.html", page = name_page)

@app.route("/category/<cat_name>")
def category(cat_name):
    category = cat_name 
    return render_template("category.html", categ_name = category)

@app.route("/review/<review_title>")
def review(review_title):
    title = review_title
    return render_template("read-review.html", title = title)



#Routes for login
@app.route("/login")
def login():
    return render_template("login/login.html")

@app.route("/signin")
def signIn():
    return render_template("login/signin.html")



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