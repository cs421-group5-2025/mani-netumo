# 🖥️ Mini-Netumo: Uptime & Domain Monitoring System

This project is a **capstone project** for CS 421 at the University of Dodoma. Inspired by Netumo, this app monitors websites and domains to ensure uptime, SSL validity, and domain expiry.

It includes:
- Uptime checks (every 5 minutes)
- SSL certificate and domain expiry notifications
- Alert delivery via email and Slack
- A responsive front-end dashboard
- CI/CD and containerized deployment on AWS

---
This system is deployed on an **Amazon EC2 Free Tier instance** using Docker Compose.

- **Public IP**: http://13.62.0.111
- **Port 80/443**: NGINX load balancer
- **Backend API**: http://13.62.0.111/api/

ou can access the docs via:
> http://13.62.0.111/api/docs

API endpoints:
- `POST /targets`
- `GET /targets`
- `GET /status/{id}`
- `GET /alerts`

Authentication: **JWT Token** (passed via Authorization header)

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


Getting Started
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


```md
## 📊 Features

- Add and manage monitored targets
- Track latency and HTTP status logs
- View 24h uptime stats in graphs
- Daily SSL and domain expiry checks
- Alert on consecutive downtime or expiry threshold
- JWT-secured API
- CI/CD via GitHub Actions and Docker Hub

---

meni-netumo/
├── backend/
│ ├── app/ # Flask app
│ ├── Dockerfile
│ └── requirements.txt
├── frontend/ # React app
├── nginx/ # NGINX load balancer config
├── .github/workflows/ # GitHub Actions
├── docker-compose.yml
|__ screenshots
├── .env
└── README.md

## 👥 Contributors

| GitHub Username | Role                         |
|------------------|------------------------------|
| Luckyferuzi      | Owner, Deployment, Docs      |
| Fazilfizzo       | Frontend, Architecture       |
| Issa885          | Backend API, Swagger Docs    |
| KABIPE           | Monitoring + Celery Worker   |
| sherlock-07      | CI/CD, Demo, Logs & Alerts   |