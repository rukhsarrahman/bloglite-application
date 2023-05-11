from application.workers import celery
import datetime
from celery.schedules import crontab
from application.models import db, User, Comment, Post, Likes, Follower
from application.config import LocalDevelopmentConfig
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from weasyprint import HTML
from flask import current_app as app
import matplotlib.pyplot as plt
import calendar
import os

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(10.0, print_current_time_job.s, name="add every 10")

@celery.task()
def print_current_time_job():
    print("START")
    now = datetime.now()
    print("now in task = ", now)
    dt_string = now.strftime("%d/%m%Y %H:%M:%S")
    print("date and time = ", dt_string)
    print("Complete")
    return dt_string

def send_email(to_address, subject, message, attachment_file=None):
    print("now here")
    msg = MIMEMultipart()
    msg["From"] = app.config["SENDER_ADDRESS"]
    msg["To"] = to_address
    msg["Subject"] = subject

    msg.attach(MIMEText(message, "html"))
    if attachment_file:
        with open(attachment_file, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition", f"attachment; filename = {attachment_file}",
        )
        msg.attach(part)
    s = smtplib.SMTP(host=app.config["SMTP_SERVER_HOST"], port=app.config["SMTP_SERVER_PORT"])
    s.login(app.config["SENDER_ADDRESS"], app.config["SENDER_PASSWORD"])
    s.send_message(msg)
    s.quit()
    print("done")

@celery.task()
def dailyEmail():
    user_query = db.session.query(User).all()
    users = []
    for query in user_query:
        users.append({"name": query.name,"username":query.username, "email":query.email})
    for user in users:
        followings = db.session.query(Follower).filter(Follower.follower == user["username"])
        follow_posts = []
        for f in followings:
            posts_query = db.session.query(Post).filter(Post.username == f.following)
            if posts_query:
                for posts in posts_query: 
                    if posts.date == str(datetime.date.today()):
                        follow_posts.append({"username":posts.username, "title":posts.title, "post_id":posts.post_id})
        posts_query = db.session.query(Post).filter(Post.username == user["username"])
        comments = []
        for post in posts_query:
            comment = db.session.query(Comment).filter(Comment.post_id == post.post_id)
            if comment:
                for c in comment:
                    if c.date == str(datetime.date.today()):
                        comments.append({"body":c.body, "commenter":c.commenter})
        if(follow_posts == [] and comments == []):
            break
        with open("templates/dailyNotifs.html") as file_:
            template = Template(file_.read())
            message = template.render(user=user, posts = follow_posts, comments = comments)
        send_email(user["email"], subject="Daily Summary", message = message)

def format_report(template_file, total_posts,crowns, followers_gained, followings_gained, month, user = {}):
    with open(template_file) as file_:
        template = Template(file_.read())
        return template.render(total_posts = total_posts,crowns = crowns, user=user, month = month, followers_gained = followers_gained, followings_gained = followings_gained)

def create_pdf_report(total_posts, crowns,followers_gained, followings_gained, month, user):
    message=format_report("templates/monthlyReport.html",total_posts = total_posts,crowns = crowns, followers_gained = followers_gained, followings_gained = followings_gained, month = month, user = user)
    html = HTML(string=message, base_url="static")
    file_name = "static/reports/"+str(user["username"]) + ".pdf"
    html.write_pdf(target=file_name, presentational_hints=True)
    with open("templates/report_email.html") as file_:
            template = Template(file_.read())
            body = template.render(user=user)
    send_email(user["email"], subject="Monthly Report", message = body, attachment_file = file_name)
    os.remove("static/reports/"+str(user["username"]) + ".pdf")
    os.remove('static/graphs/'+str(user["username"])+'_follow_history.png')
    os.remove('static/graphs/'+str(user["username"])+'_engagement.png')


@celery.task()
def generate_report_data():
    today = datetime.date.today()
    first = today.replace(day=1)
    last_month = first - datetime.timedelta(days=1)
    last_month = last_month.strftime("%Y-%m")
    for_the_month = str(calendar.month_name[int(last_month[5:])])+" "+last_month[0:4]
    user_query = db.session.query(User).all()
    users = []
    for query in user_query:
        users.append({"profile_photo":query.profile_photo,"name": query.name,"username":query.username, "email":query.email})
    for user in users:
        followings = db.session.query(Follower).filter(Follower.follower == user["username"])
        followers = db.session.query(Follower).filter(Follower.following == user["username"])
        followers_gained = 0
        followings_gained = 0
        x_follower = []
        y_follower = []
        x_following = []
        y_following = []
        for follower in followers:
            if follower.date not in x_follower:
                x_follower.append(follower.date)
                y_follower.append(1)
            else:
                y_follower[x_follower.index(follower.date)]+=1
            if follower.date[0:7] == last_month:
                followers_gained+=1

        for following in followings:
            if following.date not in x_following:
                x_following.append(following.date)
                y_following.append(1)
            else:
                y_following[x_following.index(following.date)]+=1

            if following.date[0:7] == last_month:
                followings_gained+= 1
        followers_gained = followers_gained
        followings_gained = followings_gained
        plt.figure()
        plt.plot(x_follower, y_follower, label = "Followers")
        plt.plot(x_following, y_following, label = "Followings")
        plt.xlabel('Dates') 
        plt.ylabel('Follow Counts') 
        plt.title("Follow Summary")
        plt.legend()
        plt.savefig('static/graphs/'+str(user["username"])+'_follow_history.png')
        plt.close()

        posts_query = db.session.query(Post).filter(Post.username == user["username"])
        posts = []
        maxx_engaged = 0
        maxx_commented = 0
        maxx_liked = 0
        most_engaged = "NIL"
        most_commented = "NIL"
        most_liked = "NIL"
        x_post_date = []
        y_likes = []
        y_comments = []
        if posts_query:
            for post in posts_query: 
                if post.date[0:7] == last_month:
                    posts.append({"title":post.title, "post_id":post.post_id, "likes_num":post.likes_num, "comments_num":post.comments_num})
                    if post.likes_num+post.comments_num > maxx_engaged:
                        maxx_engaged = post.likes_num+post.comments_num
                        most_engaged = post.title
                    if post.likes_num > maxx_liked:
                        maxx_liked = post.likes_num
                        most_liked = post.title
                    if post.comments_num > maxx_commented:
                        maxx_commented = post.comments_num
                        most_commented = post.title
        total_posts = len(posts)
        comment_query = db.session.query(Comment).all()
        like_query = db.session.query(Likes).all()
        for like in like_query:
            if like.date[0:7] == last_month:
                if like.date not in x_post_date:
                    x_post_date.append(like.date)
                    y_likes.append(1)
                    y_comments.append(0)
                else:
                    y_likes[x_post_date.index(like.date)]+=post.likes_num
        for comment in comment_query:
            if comment.date[0:7] == last_month:
                if comment.date not in x_post_date:
                    x_post_date.append(comment.date)
                    y_comments.append(1)
                    y_likes.append(0)
                else:
                    y_comments[x_post_date.index(comment.date)]+=1
        crowns = {"most_engaged":most_engaged,"most_commented":most_commented,"most_liked":most_liked}
        plt.figure()
        plt.plot(x_post_date, y_likes, label = "Likes")
        plt.plot(x_post_date, y_comments, label = "Comments")
        plt.xlabel('Dates') 
        plt.ylabel('Engagement Counts') 
        plt.title("Engagement Summary")
        plt.legend()
        plt.savefig('static/graphs/'+str(user["username"])+'_engagement.png')
        plt.close()
        create_pdf_report(total_posts,crowns,followers_gained, followings_gained, for_the_month,user)
    