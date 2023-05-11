import os
from flask import Flask, jsonify
from flask import render_template
from flask import request
from application import config
from application import workers
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_restful import Resource,Api
from application.models import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from weasyprint import HTML
from flask_cors import CORS

from application.models import User, Post, Comment, Follower, Likes


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"],
        timezone = app.config['CELERY_TIMEZONE'],
        beat_schedule = app.config['CELERYBEAT_SCHEDULE'],
    )
    celery.Task = workers.ContextTask
    CORS(app)
    return app,api, celery

app,api,celery = create_app()
        
from application.controllers import *

from application.api import UserAPI
api.add_resource(UserAPI, '/user','/user/<string:username>')

from application.api import PostAPI
api.add_resource(PostAPI, '/post','/post/<string:username>', '/post/<int:post_id>')

from application.api import CommentAPI
api.add_resource(CommentAPI, '/comment','/comment/<int:id>')

from application.api import IndividualPostAPI
api.add_resource(IndividualPostAPI, '/posts/<int:post_id>')

from application.api import TestAPI
api.add_resource(TestAPI, "/test")

from application.api import AllUsersAPI
api.add_resource(AllUsersAPI, "/all")

from application.api import LoginAPI
api.add_resource(LoginAPI, "/login")

from application.api import LogoutAPI
api.add_resource(LogoutAPI, "/logout")

from application.api import FollowAPI
api.add_resource(FollowAPI, "/follow","/follow/<string:username>")

from application.api import FeedAPI
api.add_resource(FeedAPI, "/feed")

from application.api import LikeAPI
api.add_resource(LikeAPI, "/like","/like/<string:username>","/like/<int:post_id>")

from application.api import TrendingPosts
api.add_resource(TrendingPosts, "/trending")


if __name__=='__main__':
    app.run(
        host = '0.0.0.0',
        debug = True,
        port = 8080
    )
    