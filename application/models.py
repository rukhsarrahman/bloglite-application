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
    followers = db.Column(db.Integer, default = 0)
    profile_photo = db.Column(db.String, default = 'default_user.jpeg')
    posts = db.relationship('Post', backref='user')
    comments = db.relationship('Comment', backref='user')
    like = db.relationship('Likes', backref='user')

class Post(db.Model):
    __tablename__ = 'post'
    post_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    title = db.Column(db.String)
    description = db.Column(db.String)
    likes_num = db.Column(db.Integer, default=0)
    comments_num = db.Column(db.Integer, default = 0)
    username = db.Column(db.Integer, db.ForeignKey('user.username'))
    post_photo = db.Column(db.String, default = 'default_bg.jpeg')
    date = db.Column(db.String)
    comments = db.relationship('Comment', backref='post')
    like = db.relationship('Likes', backref='post')

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    body = db.Column(db.String)
    date = db.Column(db.String)
    commenter = db.Column(db.Integer, db.ForeignKey('user.username'))

class Follower(db.Model):
    __tablename__= 'follower'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    following = db.Column(db.String)
    follower = db.Column(db.String)
    date = db.Column(db.String)

class Likes(db.Model):
    __tablename__= "likes"
    id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'))
    username = db.Column(db.Integer, db.ForeignKey('user.username'))
    date = db.Column(db.String)
