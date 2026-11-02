# Deployment Guide — TaskFlow Pro Capstone

---

## Overview

This guide covers deploying the TaskFlow Pro application to production.

---

## Prerequisites

- Python 3.10+
- Git
- Access to a cloud provider (Railway, Render, Heroku, or VPS)

---

## Local Setup

```bash
# 1. Clone repository
git clone https://github.com/yourusername/taskflow-pro.git
cd taskflow-pro

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\Activate.ps1  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env with your values

# 5. Initialize database
python -c "from src.main import init_database; init_database()"

# 6. Run development server
uvicorn src.main:app --reload --port 8000

# 7. Access API docs
# http://localhost:8000/docs
```

---

## Environment Variables (.env)

```bash
# Required
SECRET_KEY=your-very-secret-key-here-make-it-long-and-random

# Optional
DATABASE_URL=taskflow.db
ACCESS_TOKEN_EXPIRE=60
DEBUG=false
```

Generate a secure secret key:
```python
import secrets
print(secrets.token_hex(32))
```

---

## Deploying to Railway

[Railway](https://railway.app) is the easiest free deployment option.

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Create project
railway new

# 4. Set environment variables
railway variables set SECRET_KEY=your-secret-key

# 5. Deploy
railway up

# 6. Get your URL
railway status
```

---

## Deploying to Render

1. Push code to GitHub
2. Go to [render.com](https://render.com)
3. New → Web Service
4. Connect your GitHub repo
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `uvicorn src.main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables in the dashboard
8. Deploy

---

## Deploying to VPS (Linux)

```bash
# On your server:

# Install Python
sudo apt update
sudo apt install python3.10 python3-pip python3-venv nginx -y

# Clone and setup
git clone https://github.com/yourusername/taskflow-pro.git
cd taskflow-pro
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create systemd service
sudo nano /etc/systemd/system/taskflow.service
```

```ini
[Unit]
Description=TaskFlow Pro
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/taskflow-pro
Environment="PATH=/home/ubuntu/taskflow-pro/venv/bin"
ExecStart=/home/ubuntu/taskflow-pro/venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable taskflow
sudo systemctl start taskflow
```

---

## Production Checklist

Before going live:

- [ ] SECRET_KEY is a long random string (not the default)
- [ ] DEBUG is set to false
- [ ] Database file is in a persistent location
- [ ] HTTPS is configured (SSL certificate)
- [ ] Logging is writing to a file
- [ ] API keys are environment variables (not hardcoded)
- [ ] Error pages don't expose stack traces
- [ ] Rate limiting is configured
- [ ] Backups are scheduled

---

## Testing the Deployment

```bash
# Health check
curl https://yourapp.com/health

# Create user
curl -X POST https://yourapp.com/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'

# Login
curl -X POST https://yourapp.com/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# API docs
# https://yourapp.com/docs
```

---

## Monitoring

For a production application, add:

1. **Logging** — already configured in `src/main.py`
2. **Uptime monitoring** — [UptimeRobot](https://uptimerobot.com) (free)
3. **Error tracking** — [Sentry](https://sentry.io) (free tier)

---

*Congratulations on completing the Python Mastery Academy Capstone! 🏆*
