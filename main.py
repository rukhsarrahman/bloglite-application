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


def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    api = Api(app)
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    CORS(app)
    return app,api, celery

app,api,celery = create_app()

def send_email(to_address, subject, message):
    msg = MIMEMultipart()
    msg["From"] = app.config["SENDER_ADDRESS"]
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))
    s = smtplib.SMTP(host=app.config["SMTP_SERVER_HOST"], port=app.config["SMTP_SERVER_PORT"])
    s.login(app.config["SENDER_ADDRESS"], app.config["SENDER_PASSWORD"])
    s.send_message(msg)
    s.quit()
    return True

def main():
    new_users = [{"name": "Poppy", "email": "poppy@gmail.com"}]
    for user in new_users:
        with open("templates/welcome.html") as file_:
            template =Template(file_.read())
            message = template.render(data = user)
        send_email(user["email"], subject="Welcome email", message=message)

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


if __name__=='__main__':
    #main()
    app.run(
        host = '0.0.0.0',
        debug = True,
        port = 8080
    )
    