from application.workers import celery
from datetime import datetime
from celery.schedules import crontab
from application.models import db
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from jinja2 import Template
from weasyprint import HTML

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