from celery import Celery
import os
from slack_sdk.webhook import WebhookClient
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Celery('notifications', broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))

@app.task
def send_alert(message):
    try:
        # Email via Mailtrap
        msg = MIMEText(message)
        msg['Subject'] = 'Mini-Netumo Alert'
        msg['From'] = 'no-reply@mininetumo.com'
        msg['To'] = 'alerts@yourdomain.com'
        with smtplib.SMTP('smtp.mailtrap.io', 2525) as server:
            server.login(os.getenv('MAILTRAP_USERNAME'), os.getenv('MAILTRAP_PASSWORD'))
            server.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as e:
        print(f"Email notification failed: {str(e)}")
    try:
        # Slack webhook
        webhook = WebhookClient(os.getenv('SLACK_WEBHOOK_URL', 'your-slack-webhook'))
        webhook.send(text=message)
    except Exception as e:
        print(f"Slack notification failed: {str(e)}")