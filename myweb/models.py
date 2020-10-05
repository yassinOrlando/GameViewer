from main import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.Text(50))
    email = db.Column(db.Text(50))
    password = db.Column(db.Text(50))
    img = db.Column(db.Text(50))

    def __init__(self, nickname, email, password, img):
        self.nickname = nickname 
        self.email = email
        self.password = password
        self.img = img

class Categories(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text(50))

    def __init__(self, **kwargs):
        super(Categories, self).__init__(**kwargs)


"""
class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    id_cat = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=False)
    title = db.Column(db.Text(50))
    img = db.Column(db.Text(50))
    content = db.Column(db.Text(50))
    """