# Deployment Guide

## 🌐 Deploying Music Analyzer to the Cloud

This guide shows how to deploy the Music Analyzer application to various cloud platforms.

## Table of Contents
- [Local Network Deployment](#local-network)
- [Streamlit Cloud (Free)](#streamlit-cloud)
- [Heroku](#heroku)
- [Docker](#docker)
- [AWS EC2](#aws-ec2)
- [Google Cloud Run](#google-cloud-run)

---

## Local Network

Deploy on your local network for team access.

```bash
# Start with custom host and port
streamlit run app.py --server.port 8080 --server.address 0.0.0.0

# Access from other devices on same network
# http://YOUR_LOCAL_IP:8080
```

**Find your local IP:**
- macOS/Linux: `ifconfig | grep inet`
- Windows: `ipconfig`

---

## Streamlit Cloud

**Easiest option - Free tier available!**

### Prerequisites
- GitHub account
- Your code in a GitHub repository

### Steps

1. **Prepare your repository:**
```bash
# Ensure these files exist:
# - app.py
# - requirements.txt
# - src/ (with all modules)
# - outputs/ and temp/ directories

# Commit and push to GitHub
git add .
git commit -m "Prepare for deployment"
git push origin main
```

2. **Create `packages.txt`** (for system dependencies):
```text
ffmpeg
```

3. **Visit Streamlit Cloud:**
   - Go to https://share.streamlit.io
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

4. **Configure secrets** (if needed):
   - Settings → Secrets
   - Add any API keys or configurations

**Note:** Free tier has limitations:
- 1GB RAM
- 1 CPU
- May timeout on large files

---

## Heroku

Deploy to Heroku for more resources.

### Prerequisites
- Heroku account
- Heroku CLI installed

### Files to Create

**1. `Procfile`:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**2. `runtime.txt`:**
```
python-3.9.16
```

**3. `Aptfile`:**
```
ffmpeg
```

### Deploy Steps

```bash
# Login to Heroku
heroku login

# Create app
heroku create your-music-analyzer

# Add buildpacks
heroku buildpacks:add --index 1 heroku-community/apt
heroku buildpacks:add --index 2 heroku/python

# Deploy
git add .
git commit -m "Deploy to Heroku"
git push heroku main

# Open app
heroku open
```

**Scale up for better performance:**
```bash
heroku ps:scale web=1
heroku config:set MAX_WORKERS=2
```

---

## Docker

Containerize the application for any platform.

### Dockerfile

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Create directories
RUN mkdir -p temp outputs

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  music-analyzer:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./outputs:/app/outputs
      - ./temp:/app/temp
    environment:
      - STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
    restart: unless-stopped
```

### Build and Run

```bash
# Build image
docker build -t music-analyzer .

# Run container
docker run -p 8501:8501 -v $(pwd)/outputs:/app/outputs music-analyzer

# Or use docker-compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## AWS EC2

Deploy to AWS EC2 for full control.

### Launch Instance

1. **Create EC2 Instance:**
   - AMI: Ubuntu 20.04 LTS
   - Type: t2.medium (or larger)
   - Storage: 20GB+
   - Security Group: Allow ports 22 (SSH) and 8501 (Streamlit)

2. **Connect to instance:**
```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install dependencies:**
```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Python and FFmpeg
sudo apt-get install -y python3-pip python3-venv ffmpeg

# Clone your repository
git clone https://github.com/yourusername/music-analyzer.git
cd music-analyzer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

4. **Run with systemd:**

Create `/etc/systemd/system/music-analyzer.service`:
```ini
[Unit]
Description=Music Analyzer Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/music-analyzer
Environment="PATH=/home/ubuntu/music-analyzer/venv/bin"
ExecStart=/home/ubuntu/music-analyzer/venv/bin/streamlit run app.py --server.port=8501 --server.address=0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable music-analyzer
sudo systemctl start music-analyzer
sudo systemctl status music-analyzer
```

5. **Set up Nginx (optional, for HTTPS):**
```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx

# Configure Nginx
sudo nano /etc/nginx/sites-available/music-analyzer
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

Enable and restart:
```bash
sudo ln -s /etc/nginx/sites-available/music-analyzer /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

---

## Google Cloud Run

Deploy serverless on Google Cloud.

### Prerequisites
- Google Cloud account
- gcloud CLI installed

### Dockerfile for Cloud Run

```dockerfile
FROM python:3.9-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p temp outputs

ENV PORT=8080
EXPOSE 8080

CMD streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.headless=true
```

### Deploy

```bash
# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/music-analyzer
gcloud run deploy music-analyzer \
    --image gcr.io/YOUR_PROJECT_ID/music-analyzer \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --timeout 900

# Get URL
gcloud run services describe music-analyzer --region us-central1 --format 'value(status.url)'
```

---

## Performance Optimization

### For Production

**1. Configure Streamlit:**

`.streamlit/config.toml`:
```toml
[server]
maxUploadSize = 200
maxMessageSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

**2. Environment Variables:**
```bash
# Limit memory usage
export TF_FORCE_GPU_ALLOW_GROWTH=true
export OMP_NUM_THREADS=2

# Streamlit optimization
export STREAMLIT_SERVER_MAX_UPLOAD_SIZE=200
```

**3. Use Redis for Caching:**
```python
# In app.py
import streamlit as st

@st.cache_data(ttl=3600)
def cached_analysis(audio_hash):
    # Your analysis code
    pass
```

---

## Monitoring

### Setup Logging

Add to `app.py`:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Monitor with Prometheus (Optional)

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'music-analyzer'
    static_configs:
      - targets: ['localhost:8501']
```

---

## Security Considerations

1. **Use HTTPS** in production
2. **Set rate limiting** to prevent abuse
3. **Validate inputs** thoroughly
4. **Use secrets management** for API keys
5. **Regular updates** of dependencies

---

## Cost Estimates

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Streamlit Cloud | 1GB RAM | N/A | Testing, demos |
| Heroku | 550 hours/month | $7+/month | Small projects |
| AWS EC2 | 750 hours/month (1 year) | $10+/month | Full control |
| Google Cloud Run | 2M requests/month | Pay per use | Serverless |
| Docker (self-hosted) | N/A | Server costs | Maximum control |

---

## Troubleshooting Deployment

**Port already in use:**
```bash
lsof -i :8501
kill -9 PID
```

**Out of memory:**
- Increase instance size
- Use swap file
- Limit concurrent users

**Slow performance:**
- Use GPU instances for CREPE
- Enable caching
- Use faster pitch detection methods

**Build failures:**
- Check Python version compatibility
- Verify all dependencies in requirements.txt
- Check system dependencies (FFmpeg)

---

**Need help?** See main [README.md](README.md) or open an issue!
