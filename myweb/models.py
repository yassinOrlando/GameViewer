from myweb.main import db

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


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    id_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    id_cat = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    title = db.Column(db.Text(50))
    img = db.Column(db.Text(50))
    content = db.Column(db.Text(50))
    created_at = db.Column(db.Text(50))

    def __init__(self, id_user, id_cat, title, img, content, created_at):
        self.id_user = id_user
        self.id_cat = id_cat
        self.title = title
        self.img = img
        self.content = content
        self.created_at = created_at