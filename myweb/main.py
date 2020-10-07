from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
import os


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
#app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=30)


app.config['UPLOAD_FOLDER'] = './static/img'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])

db = SQLAlchemy(app)

from controller import *

if __name__ == '__main__':
    app.run(debug=True)