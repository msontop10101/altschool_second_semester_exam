from . import db
from flask_login import UserMixin
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    first_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    posts = db.relationship('Post')