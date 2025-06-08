# 🖥️ Mini-Netumo: Uptime & Domain Monitoring System

This project is a **capstone project** for CS 421 at the University of Dodoma. Inspired by Netumo, this app monitors websites and domains to ensure uptime, SSL validity, and domain expiry.

It includes:
- Uptime checks (every 5 minutes)
- SSL certificate and domain expiry notifications
- Alert delivery via email and Slack
- A responsive front-end dashboard
- CI/CD and containerized deployment on AWS

---

## 📦 Technologies Used

| Layer       | Tech Stack                        |
|-------------|-----------------------------------|
| Backend     | Python, Flask, Celery, Redis      |
| Frontend    | React (Vite), Chart.js            |
| Database    | MySQL                             |
| Queue       | Redis                             |
| Deployment  | Docker, Docker Compose, NGINX     |
| CI/CD       | GitHub Actions, EC2 (AWS Free Tier)|
| Alerts      | Mailtrap, Slack Webhook           |

---



1. Clone the repo:
2. Create a .env file
3. Run Docker
4. Create DB tables
with example of code 
docker exec -it meni-netumo-backend-1 bash
python
>>> from app import create_app, db
>>> app = create_app()
>>> app.app_context().push()
>>> db.create_all()
>>> exit()
