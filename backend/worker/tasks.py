from celery import Celery
import requests
from OpenSSL import SSL
import whois
from datetime import datetime
from models.target import TargetModel
from utils.notifications import send_alert
import os
from dotenv import load_dotenv

load_dotenv()

app = Celery('tasks', broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0'))

@app.task
def check_url(target_id):
    target = TargetModel.get_by_id(target_id)
    if not target:
        return
    try:
        response = requests.get(target.url, timeout=5)
        target.status = str(response.status_code)
        target.latency = response.elapsed.total_seconds() * 1000
        target.last_checked = datetime.utcnow()
        target.save()
    except requests.RequestException as e:
        target.status = 'DOWN'
        target.save()
        send_alert.delay(f'Downtime detected for {target.url}: {str(e)}')

@app.task
def check_ssl_domain(target_id):
    target = TargetModel.get_by_id(target_id)
    if not target:
        return
    try:
        w = whois.whois(target.url)
        expiry = w.expiration_date
        if isinstance(expiry, list):
            expiry = expiry[0]
        days_left = (expiry - datetime.utcnow()).days if expiry else 0
        if days_left <= 14:
            send_alert.delay(f'Domain {target.url} expires in {days_left} days')
    except Exception as e:
        send_alert.delay(f'Error checking SSL/domain for {target.url}: {str(e)}')