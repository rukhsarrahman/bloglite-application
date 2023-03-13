from flask import Flask, request, render_template, jsonify
from flask import current_app as app
from application.models import User, Post
from application import tasks


@app.route("/home", methods = ['GET', 'POST'])
def home():
    posts = Post.query.all()
    return render_template("home.html", posts = posts)

@app.route("/", methods = ['GET', 'POST'])
def upload_image():
    return render_template("upload_image.html")

@app.route("/posts/<username>",methods = ['GET','POST'])
def posts_by_username(username):
    posts = Post.query.filter_by(username=username)
    return render_template("post_by_username.html", posts = posts)

@app.route("/hello/<username>", methods = ['GET', 'POST'])
def hello(username):
    job = tasks.just_say_hello.delay(username)
    result = job.wait()
    return result, 200

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')