from application.database import db
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, unique = True)
    name = db.Column(db.String)
    email = db.Column(db.String, unique = True)
    password = db.Column(db.String(255))
    bio = db.Column(db.String, default = 'No description')
    profile_photo = db.Column(db.String, default = 'default_user.jpeg')
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    likes = db.Column(db.Integer)
    comments = db.Column(db.Integer)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))
    post_photo = db.Column(db.String, default = 'default_bg.jpeg')
    comments = db.relationship('Comment', backref='post')

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    body = db.Column(db.String)
    commenter = db.Column(db.Integer, db.ForeignKey('user.username'))