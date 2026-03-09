# 🚀 Deployment Guide

Guide for deploying PlotlyVizPro applications to various platforms.

---

## Table of Contents

- [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Docker Deployment](#docker-deployment)
- [AWS Deployment](#aws-deployment)
- [Google Cloud Platform](#google-cloud-platform)
- [Traditional Server Deployment](#traditional-server-deployment)

---

## Streamlit Cloud Deployment

The easiest way to deploy your Streamlit app for free.

### Prerequisites
- GitHub account
- Repository pushed to GitHub

### Steps

1. **Prepare Your Repository**

```bash
# Ensure you have requirements.txt in root
# Streamlit Cloud will automatically detect it
git add requirements.txt app.py pages/
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

2. **Deploy to Streamlit Cloud**

- Visit [share.streamlit.io](https://share.streamlit.io)
- Sign in with GitHub
- Click "New app"
- Select your repository
- Set main file path: `app.py`
- Click "Deploy"

3. **Configuration**

Create `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#56B4E9"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#262730"
textColor = "#FAFAFA"

[server]
headless = true
port = 8501

[browser]
gatherUsageStats = false
```

### Environment Variables

If using Mapbox or other API keys:

```bash
# In Streamlit Cloud dashboard:
# Settings > Secrets

# Add to secrets.toml:
MAPBOX_TOKEN = "your_token_here"
```

---

## Heroku Deployment

Deploy full-stack Python applications.

### Prerequisites
- Heroku account
- Heroku CLI installed

### For Streamlit Apps

1. **Create Heroku-specific files**

`Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

`setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml
```

`runtime.txt`:
```
python-3.10.12
```

2. **Deploy**

```bash
# Login to Heroku
heroku login

# Create app
heroku create plotlyvizpro

# Deploy
git push heroku main

# Open app
heroku open
```

3. **Add Config Vars**

```bash
heroku config:set MAPBOX_TOKEN=your_token_here
```

---

## Docker Deployment

Container-based deployment for any platform.

### Build and Run Locally

```bash
# Build image
docker build -t plotlyvizpro .

# Run container
docker run -p 8888:8888 plotlyvizpro

# Access at http://localhost:8888
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jupyter:
    build: .
    ports:
      - "8888:8888"
    volumes:
      - ./notebooks:/app/notebooks
      - ./datasets:/app/datasets
      - ./exports:/app/exports
    environment:
      - JUPYTER_ENABLE_LAB=yes

  streamlit:
    build:
      context: .
      dockerfile: Dockerfile.streamlit
    ports:
      - "8501:8501"
    volumes:
      - ./exports:/app/exports
    command: streamlit run app.py
```

### Deploy to Docker Hub

```bash
# Tag image
docker tag plotlyvizpro yourusername/plotlyvizpro:v1.0

# Push to Docker Hub
docker push yourusername/plotlyvizpro:v1.0
```

---

## AWS Deployment

### AWS Elastic Beanstalk

1. **Install EB CLI**

```bash
pip install awsebcli
```

2. **Initialize EB**

```bash
eb init -p python-3.10 plotlyvizpro
```

3. **Create Environment**

```bash
eb create plotlyvizpro-env
```

4. **Deploy**

```bash
eb deploy
```

5. **Open App**

```bash
eb open
```

### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 22.04 LTS
   - t2.micro (free tier eligible)
   - Open ports: 22 (SSH), 8501 (Streamlit), 8888 (Jupyter)

2. **SSH into Instance**

```bash
ssh -i your-key.pem ubuntu@your-ec2-ip
```

3. **Install Dependencies**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3-pip python3-venv -y

# Clone repository
git clone https://github.com/SatvikPraveen/PlotlyVizPro.git
cd PlotlyVizPro

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

4. **Run with systemd**

Create `/etc/systemd/system/streamlit.service`:

```ini
[Unit]
Description=Streamlit App
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/PlotlyVizPro
Environment="PATH=/home/ubuntu/PlotlyVizPro/venv/bin"
ExecStart=/home/ubuntu/PlotlyVizPro/venv/bin/streamlit run app.py

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable streamlit
sudo systemctl start streamlit
```

5. **Set Up Nginx Reverse Proxy**

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
    }
}
```

---

## Google Cloud Platform

### Google Cloud Run (Serverless)

1. **Create Dockerfile for Cloud Run**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

2. **Deploy**

```bash
# Build and deploy
gcloud run deploy plotlyvizpro \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Google Compute Engine

Similar to AWS EC2 - follow EC2 instructions with GCE-specific commands.

---

## Traditional Server Deployment

### Using Gunicorn (for production)

While Streamlit has its own server, you can use Gunicorn for better production deployment:

1. **Install Gunicorn**

```bash
pip install gunicorn
```

2. **Create wsgi.py** (if needed for non-Streamlit apps)

3. **Run with Gunicorn**

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:server
```

### Using Apache/Nginx

Set up reverse proxy as shown in EC2 nginx example above.

---

## Environment Variables

### Best Practices

1. **Never commit secrets to Git**

Add to `.gitignore`:
```
.env
secrets.toml
*.key
*.pem
```

2. **Use .env files locally**

Create `.env`:
```bash
MAPBOX_TOKEN=your_token
DATABASE_URL=postgresql://...
```

Load in Python:
```python
import os
from dotenv import load_dotenv

load_dotenv()
MAPBOX_TOKEN = os.getenv('MAPBOX_TOKEN')
```

3. **Use platform-specific secret managers**
   - Streamlit Cloud: Secrets management
   - Heroku: Config vars
   - AWS: Secrets Manager or Parameter Store
   - GCP: Secret Manager

---

## Performance Optimization

### 1. Caching in Streamlit

```python
import streamlit as st

@st.cache_data
def load_data():
    return pd.read_csv('datasets/superstore.csv')

df = load_data()  # Only loads once
```

### 2. Optimize Images

```python
# Use lower DPI for web
fig.write_image('plot.png', width=800, height=600, scale=1)
```

### 3. Lazy Loading

```python
# Only load data when needed
if st.button('Show Analysis'):
    df = load_heavy_dataset()
    fig = create_complex_plot(df)
    st.plotly_chart(fig)
```

---

## Monitoring and Maintenance

### Health Checks

```python
# Add to app.py for monitoring
import streamlit as st

def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Expose health endpoint
if st.experimental_get_query_params().get('health'):
    st.json(health_check())
```

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
logger.info('App started')
```

---

## Scaling Considerations

1. **Horizontal Scaling**: Use load balancer with multiple instances
2. **Caching**: Implement Redis for shared cache
3. **CDN**: Use CloudFlare or AWS CloudFront for static assets
4. **Database**: Use PostgreSQL/MySQL for persistent data
5. **Message Queue**: Use Celery for background tasks

---

## Security Checklist

- [ ] HTTPS enabled (use Let's Encrypt for free SSL)
- [ ] Environment variables for secrets
- [ ] Input validation on user data
- [ ] Rate limiting enabled
- [ ] CORS properly configured
- [ ] Regular dependency updates
- [ ] Security headers configured
- [ ] Database queries parameterized

---

## Troubleshooting Deployment

### Common Issues

**Port conflicts:**
```bash
# Check what's using port 8501
lsof -i :8501

# Use different port
streamlit run app.py --server.port 8502
```

**Memory issues:**
```python
# Optimize memory usage
import gc

@st.cache_data
def process_data():
    # ... processing ...
    gc.collect()  # Force garbage collection
    return result
```

**Slow loading:**
- Enable caching
- Reduce initial data load
- Use lazy loading
- Optimize images

---

For more help, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md) or open an issue on GitHub.
