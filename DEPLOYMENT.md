# Deployment Guide

This document covers deployment strategies for the Smart Medical Assistant, ranging from local development to production server deployment, including Docker containerization, security hardening, and monitoring.

---

## Table of Contents

- [Local Deployment](#local-deployment)
- [Server Deployment (Linux)](#server-deployment-linux)
- [Server Deployment (Windows)](#server-deployment-windows)
- [Docker Setup](#docker-setup)
- [Environment Configuration](#environment-configuration)
- [Database Migration](#database-migration)
- [Model Deployment Considerations](#model-deployment-considerations)
- [Security Checklist](#security-checklist)
- [Performance Optimization](#performance-optimization)
- [Monitoring and Logging](#monitoring-and-logging)
- [Backup Strategy](#backup-strategy)

---

## Local Deployment

For local development and testing, the built-in Flask development server is sufficient.

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Start the API
python -m src.api.app
```

The API will be accessible at `http://localhost:5000`.

> **Warning:** The Flask development server is **not suitable for production**. Use Gunicorn or uWSGI for production deployments.

---

## Server Deployment (Linux)

### 1. Prepare the Server

**Recommended OS:** Ubuntu 22.04 LTS or CentOS 8+

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y python3 python3-pip python3-venv git nginx mysql-server

# Create app user
sudo useradd -m -s /bin/bash sma
sudo usermod -aG sudo sma
```

### 2. Clone and Setup Project

```bash
su - sma
git clone https://github.com/your-org/smart-medical-assistant.git ~/smart-medical-assistant
cd ~/smart-medical-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Gunicorn

Create a systemd service file at `/etc/systemd/system/sma-api.service`:

```ini
[Unit]
Description=Smart Medical Assistant API
After=network.target

[Service]
User=sma
Group=www-data
WorkingDirectory=/home/sma/smart-medical-assistant
Environment="PATH=/home/sma/smart-medical-assistant/venv/bin"
Environment="FLASK_ENV=production"
Environment="DB_HOST=localhost"
Environment="DB_NAME=smart_medical_db"
Environment="DB_USER=sma_user"
Environment="DB_PASSWORD=YourSecurePassword123!"
ExecStart=/home/sma/smart-medical-assistant/venv/bin/gunicorn \
  --workers 4 \
  --bind 0.0.0.0:8000 \
  --access-logfile /var/log/sma/access.log \
  --error-logfile /var/log/sma/error.log \
  --timeout 120 \
  src.api.app:app

[Install]
WantedBy=multi-user.target
```

Create log directories and enable:

```bash
sudo mkdir -p /var/log/sma
sudo chown -R sma:www-data /var/log/sma
sudo systemctl daemon-reload
sudo systemctl enable sma-api
sudo systemctl start sma-api
```

### 4. Configure Nginx Reverse Proxy

Create `/etc/nginx/sites-available/sma`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts for ML inference
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;
    }

    location /static {
        alias /home/sma/smart-medical-assistant/static;
        expires 30d;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/sma /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. HTTPS with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
sudo systemctl enable certbot.timer
```

---

## Server Deployment (Windows)

### 1. Install Prerequisites

- Python 3.8+ from [python.org](https://python.org)
- Git for Windows
- MySQL Server for Windows
- IIS (optional, for reverse proxy) or Nginx for Windows

### 2. Setup Project

```powershell
# Open PowerShell as Administrator
git clone https://github.com/your-org/smart-medical-assistant.git
cd smart-medical-assistant
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Run as a Windows Service

Use **NSSM** (Non-Sucking Service Manager) to run Gunicorn as a Windows service:

```powershell
# Download NSSM from https://nssm.cc/download
# Extract nssm.exe to a known location (e.g., C:\nssm\nssm.exe)

nssm install SMA-API
# Application path: C:\...\smart-medical-assistant\venv\Scripts\gunicorn.exe
# Arguments: --workers 4 --bind 0.0.0.0:8000 src.api.app:app
# Working directory: C:\...\smart-medical-assistant

nssm start SMA-API
```

### 4. Configure IIS Reverse Proxy (Optional)

Install IIS URL Rewrite and ARR modules, then create a reverse proxy rule pointing to `http://localhost:8000`.

---

## Docker Setup

A `Dockerfile` and `docker-compose.yml` are provided for easy containerized deployment.

### Dockerfile

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create necessary directories
RUN mkdir -p /app/data/raw /app/data/processed /app/models /app/reports

# Ensure models are present (if not, they must be mounted as volumes)
# RUN python -c "from src.ml.train_models import main; import os; main({'runDir': '/app'})"

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "src.api.app:app"]
```

### docker-compose.yml

```yaml
version: "3.9"

services:
  api:
    build: .
    container_name: sma-api
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - DB_HOST=db
      - DB_PORT=3306
      - DB_NAME=smart_medical_db
      - DB_USER=sma_user
      - DB_PASSWORD=${DB_PASSWORD}
    volumes:
      - ./models:/app/models:ro
      - ./data:/app/data:ro
      - ./reports:/app/reports
    depends_on:
      - db
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: mysql:8.0
    container_name: sma-db
    environment:
      MYSQL_ROOT_PASSWORD: ${DB_ROOT_PASSWORD}
      MYSQL_DATABASE: smart_medical_db
      MYSQL_USER: sma_user
      MYSQL_PASSWORD: ${DB_PASSWORD}
    volumes:
      - mysql_data:/var/lib/mysql
      - ./schema.sql:/docker-entrypoint-initdb.d/schema.sql:ro
    ports:
      - "3306:3306"
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    container_name: sma-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
      - ./ssl:/etc/nginx/ssl:ro
    depends_on:
      - api
    restart: unless-stopped

volumes:
  mysql_data:
```

### Build and Run

```bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f api

# Stop
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

---

## Environment Configuration

For production, all secrets and configuration should be externalized.

### Production `.env` File

```bash
# Flask
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=YourSuperSecretKey-ChangeThisInProduction!

# MySQL
DB_HOST=db
DB_PORT=3306
DB_NAME=smart_medical_db
DB_USER=sma_user
DB_PASSWORD=changeme-strongpassword

# Paths
MODEL_DIR=/app/models
DATA_DIR=/app/data/raw

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/sma/app.log
```

> **Never** commit `.env` or any file containing secrets to version control. The `.gitignore` already excludes `.env` files.

---

## Database Migration

If schema changes are needed over time:

### Manual Migration

```bash
# Backup before migrating
mysqldump -u sma_user -p smart_medical_db > backup_$(date +%F).sql

# Apply new schema
mysql -u sma_user -p smart_medical_db < migrations/001_add_feedback_table.sql
```

### Automated Migrations (Optional)

If using SQLAlchemy with Flask-SQLAlchemy:

```bash
pip install Flask-Migrate

# Initialize migrations
flask db init

# Create migration script
flask db migrate -m "Add user feedback table"

# Apply migration
flask db upgrade
```

---

## Model Deployment Considerations

1. **Model Size:** Serialized models (`best_model.pkl`, `preprocessor.pkl`) can be large. Use Git LFS if storing in Git, or mount them as volumes in Docker.
2. **Cold Start:** Loading models on first request can cause latency. Ensure models are loaded at application startup (already handled in `app.py`).
3. **Model Versioning:** Tag models with version numbers and maintain a model registry:
   ```
   models/
     ├── v1.0.0/
     │   ├── best_model.pkl
     │   └── preprocessor.pkl
     └── v1.1.0/
         ├── best_model.pkl
         └── preprocessor.pkl
   ```
4. **A/B Testing:** Deploy multiple model versions behind a load balancer or API gateway to compare performance.
5. **Rollback:** Keep previous model versions available for immediate rollback if accuracy degrades.

---

## Security Checklist

Before going to production, verify the following:

- [ ] **HTTPS enabled** (Let's Encrypt, commercial SSL, or self-signed for internal use)
- [ ] **Secrets externalized** (no hardcoded passwords, API keys, or DB credentials)
- [ ] **Debug mode disabled** (`FLASK_DEBUG=0`, `FLASK_ENV=production`)
- [ ] **CORS restricted** (only allow trusted frontend domains, not `*`)
- [ ] **Input validation** (validate all incoming JSON, sanitize user text)
- [ ] **Rate limiting** (prevent abuse of the `/api/predict` endpoint)
- [ ] **SQL injection prevention** (use parameterized queries if using raw SQL)
- [ ] **Content Security Policy** (CSP headers for frontend)
- [ ] **Firewall rules** (only expose ports 80/443; block 5000/8000 from public)
- [ ] **Regular dependency updates** (`pip list --outdated`)
- [ ] **Medical disclaimer** prominently displayed on all prediction results

### Rate Limiting Example (Flask-Limiter)

```python
# Add to requirements.txt: Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(
    app,
    key_func=lambda: request.remote_addr,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/predict', methods=['POST'])
@limiter.limit("10 per minute")
def predict_disease():
    ...
```

---

## Performance Optimization

1. **Gunicorn Workers:** Use `2-4 x $num_cores` workers. For I/O-bound ML inference, `4` workers on a 2-core VM is a good starting point.
2. **Model Caching:** Models are already loaded once at startup. Ensure they are not reloaded per request.
3. **Nginx Caching:** Cache static assets and health check responses:
   ```nginx
   location /api/health {
       proxy_cache_valid 200 10s;
       proxy_cache my_cache;
   }
   ```
4. **Database Connection Pooling:** Use `mysql-connector-python` pooling or SQLAlchemy `pool_size=10`.
5. **TF-IDF Sparse Matrices:** Keep features sparse during inference to reduce memory usage.
6. **Model Compression:** For large models, consider quantization (XGBoost) or feature selection to reduce dimensionality.

---

## Monitoring and Logging

### Structured Logging

Use Python's `logging` module with JSON formatting for production:

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('/var/log/sma/app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
```

### Monitoring Tools

| Tool | Purpose |
|------|---------|
| **Prometheus + Grafana** | Metrics dashboard (request latency, error rates, model inference time) |
| **Sentry** | Error tracking and alerting |
| **UptimeRobot / Pingdom** | External uptime monitoring |
| **Nginx Access Logs** | Request-level analytics |

### Key Metrics to Track

- API request rate (requests/minute)
- Average response time (p50, p95, p99)
- Prediction endpoint latency
- Model accuracy over time (with feedback loop)
- Error rate (4xx, 5xx)
- System resource usage (CPU, RAM, disk)

---

## Backup Strategy

### 1. Database Backups

```bash
# Automated daily backup via cron
0 2 * * * mysqldump -u sma_user -p'YourPassword' smart_medical_db > /backups/db_$(date +\%F).sql

# Compress and rotate
find /backups/ -name "db_*.sql" -mtime +30 -delete
```

### 2. Model Artifacts Backups

```bash
# Backup after every retraining
rsync -avz models/ backups/models_$(date +%F)/
```

### 3. Configuration Backups

```bash
# Backup nginx, systemd, and env files
tar czvf backups/config_$(date +%F).tar.gz \
  /etc/nginx/sites-available/sma \
  /etc/systemd/system/sma-api.service \
  /home/sma/smart-medical-assistant/.env
```

### 4. Disaster Recovery Plan

| Scenario | Recovery Steps |
|----------|---------------|
| Database corruption | Restore from latest `.sql` backup |
| Model corruption | Roll back to previous `best_model.pkl` version |
| Server failure | Spin up new VM, restore code + models + DB backup |
| Accidental data deletion | Restore from daily backups; check off-site storage |

### 5. Off-Site Storage

Sync critical backups to cloud storage (AWS S3, Azure Blob, Google Cloud Storage, or Backblaze B2):

```bash
aws s3 sync /backups/ s3://your-backup-bucket/sma/ --storage-class STANDARD_IA
```

---

## Quick Reference

| Action | Command |
|--------|---------|
| Start Linux service | `sudo systemctl start sma-api` |
| Check service status | `sudo systemctl status sma-api` |
| View logs | `sudo journalctl -u sma-api -f` |
| Restart Nginx | `sudo systemctl restart nginx` |
| Docker build | `docker-compose up -d --build` |
| Docker logs | `docker-compose logs -f api` |
| SSL renew | `sudo certbot renew --dry-run` |

---

For questions or issues related to deployment, please open an issue in the project repository or contact the DevOps team.
