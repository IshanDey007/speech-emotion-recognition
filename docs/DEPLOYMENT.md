# Deployment Guide

Complete guide for deploying the Speech Emotion Recognition system to production.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Frontend Deployment (Vercel)](#frontend-deployment-vercel)
- [Backend Deployment](#backend-deployment)
  - [Railway](#option-1-railway)
  - [Render](#option-2-render)
  - [AWS EC2](#option-3-aws-ec2)
- [Environment Variables](#environment-variables)
- [Production Checklist](#production-checklist)
- [Monitoring](#monitoring)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

- Git installed
- Node.js 18+ (for frontend)
- Python 3.8+ (for backend)
- Trained model files
- Domain name (optional)

---

## Frontend Deployment (Vercel)

Vercel is the recommended platform for deploying the Next.js frontend.

### Step 1: Prepare Frontend

```bash
cd frontend
npm install
npm run build  # Test build locally
```

### Step 2: Deploy to Vercel

**Option A: Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
cd frontend
vercel

# Deploy to production
vercel --prod
```

**Option B: GitHub Integration**

1. Push code to GitHub
2. Visit [vercel.com](https://vercel.com)
3. Click "New Project"
4. Import your GitHub repository
5. Configure:
   - Framework Preset: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`
6. Add environment variable:
   - `NEXT_PUBLIC_API_URL`: Your backend URL
7. Click "Deploy"

### Step 3: Configure Custom Domain (Optional)

1. Go to Project Settings → Domains
2. Add your custom domain
3. Update DNS records as instructed
4. Wait for SSL certificate provisioning

**Vercel Configuration** (`frontend/vercel.json`):

```json
{
  "buildCommand": "npm run build",
  "devCommand": "npm run dev",
  "installCommand": "npm install",
  "framework": "nextjs",
  "outputDirectory": ".next"
}
```

---

## Backend Deployment

### Option 1: Railway

Railway offers easy deployment with automatic HTTPS and scaling.

#### Step 1: Prepare Backend

Create `railway.json`:

```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

Create `Procfile`:

```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

#### Step 2: Deploy

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
cd backend
railway init

# Deploy
railway up

# Set environment variables
railway variables set PYTHON_VERSION=3.10
```

#### Step 3: Add Model Files

Since model files are large, upload them separately:

```bash
# SSH into Railway container
railway shell

# Upload model files (use SCP or cloud storage)
```

**Alternative**: Store models in cloud storage (S3, GCS) and download on startup.

---

### Option 2: Render

Render provides free tier with automatic deployments.

#### Step 1: Create `render.yaml`

```yaml
services:
  - type: web
    name: speech-emotion-api
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "uvicorn main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
```

#### Step 2: Deploy

1. Push code to GitHub
2. Visit [render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect GitHub repository
5. Configure:
   - Name: speech-emotion-api
   - Environment: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Click "Create Web Service"

#### Step 3: Upload Model Files

Use Render Disks for persistent storage:

1. Go to Dashboard → Disks
2. Create new disk
3. Mount to `/opt/render/project/src/saved_models`
4. Upload model files via SSH or cloud storage

---

### Option 3: AWS EC2

For full control and scalability.

#### Step 1: Launch EC2 Instance

```bash
# Choose Ubuntu 22.04 LTS
# Instance type: t3.medium (minimum)
# Storage: 20GB
# Security Group: Allow ports 22, 80, 443, 8000
```

#### Step 2: Connect and Setup

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python
sudo apt install python3.10 python3-pip -y

# Install dependencies
sudo apt install ffmpeg libsndfile1 -y

# Clone repository
git clone https://github.com/IshanDey007/speech-emotion-recognition.git
cd speech-emotion-recognition/backend

# Install Python packages
pip3 install -r requirements.txt

# Download model files (from S3 or transfer)
```

#### Step 3: Setup Systemd Service

Create `/etc/systemd/system/emotion-api.service`:

```ini
[Unit]
Description=Speech Emotion Recognition API
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/speech-emotion-recognition/backend
Environment="PATH=/home/ubuntu/.local/bin"
ExecStart=/usr/bin/python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable emotion-api
sudo systemctl start emotion-api
sudo systemctl status emotion-api
```

#### Step 4: Setup Nginx Reverse Proxy

```bash
sudo apt install nginx -y
```

Create `/etc/nginx/sites-available/emotion-api`:

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
    }
}
```

Enable site:

```bash
sudo ln -s /etc/nginx/sites-available/emotion-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### Step 5: Setup SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Environment Variables

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

### Backend (.env)

```bash
# Model Configuration
MODEL_PATH=saved_models/emotion_model.keras
LABEL_ENCODER_PATH=saved_models/label_encoder.pkl

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-frontend-url.com

# Optional: Cloud Storage
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET=your-bucket
```

---

## Production Checklist

### Security

- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Implement API authentication
- [ ] Sanitize file uploads
- [ ] Set up firewall rules
- [ ] Use environment variables for secrets
- [ ] Enable security headers

### Performance

- [ ] Enable gzip compression
- [ ] Configure CDN for frontend
- [ ] Optimize model loading
- [ ] Add caching layer (Redis)
- [ ] Set up load balancing
- [ ] Configure auto-scaling
- [ ] Optimize database queries
- [ ] Monitor response times

### Monitoring

- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Add health check endpoints
- [ ] Set up uptime monitoring
- [ ] Configure alerts
- [ ] Track API usage
- [ ] Monitor resource usage
- [ ] Set up analytics

### Backup

- [ ] Backup model files
- [ ] Backup database
- [ ] Configure automated backups
- [ ] Test restore procedures
- [ ] Document recovery process

---

## Monitoring

### Health Check Endpoint

```bash
curl https://your-api.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "version": "1.0.0"
}
```

### Logging

**Backend Logging** (`backend/logging_config.py`):

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

### Error Tracking with Sentry

```bash
pip install sentry-sdk
```

```python
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## Troubleshooting

### Frontend Issues

**Build Fails**
```bash
# Clear cache
rm -rf .next node_modules
npm install
npm run build
```

**API Connection Error**
- Check `NEXT_PUBLIC_API_URL` is correct
- Verify CORS settings on backend
- Check network/firewall rules

### Backend Issues

**Model Not Loading**
```bash
# Check model files exist
ls -lh saved_models/

# Check file permissions
chmod 644 saved_models/*

# Verify Python version
python3 --version  # Should be 3.8+
```

**High Memory Usage**
- Reduce batch size
- Implement model quantization
- Use model caching
- Configure swap space

**Slow Predictions**
- Use GPU if available
- Optimize feature extraction
- Implement request queuing
- Add caching layer

### Common Errors

**"Model not loaded"**
- Ensure model files are in correct location
- Check file paths in code
- Verify model compatibility

**"CORS Error"**
- Add frontend URL to CORS origins
- Check CORS middleware configuration

**"Out of Memory"**
- Increase server RAM
- Reduce concurrent requests
- Optimize model size

---

## Scaling

### Horizontal Scaling

```bash
# Use load balancer (Nginx, AWS ALB)
# Deploy multiple backend instances
# Use Redis for session management
```

### Vertical Scaling

```bash
# Increase server resources
# Optimize code performance
# Use caching extensively
```

### Database Scaling

```bash
# Use connection pooling
# Implement read replicas
# Add database indexes
# Use caching layer
```

---

## Cost Optimization

### Free Tier Options

- **Frontend**: Vercel (Free tier)
- **Backend**: Railway/Render (Free tier with limitations)
- **Storage**: AWS S3 (Free tier: 5GB)
- **Monitoring**: Sentry (Free tier: 5K events/month)

### Estimated Monthly Costs

**Small Scale** (< 1000 requests/day):
- Frontend: $0 (Vercel free tier)
- Backend: $0-5 (Railway/Render free tier)
- Storage: $0-1
- **Total**: $0-6/month

**Medium Scale** (< 10,000 requests/day):
- Frontend: $0-20
- Backend: $20-50
- Storage: $5-10
- CDN: $5-15
- **Total**: $30-95/month

**Large Scale** (> 100,000 requests/day):
- Frontend: $50-100
- Backend: $200-500
- Storage: $20-50
- CDN: $50-100
- Database: $50-100
- **Total**: $370-850/month

---

## Support

For deployment issues:
- GitHub Issues: https://github.com/IshanDey007/speech-emotion-recognition/issues
- Email: irock9431@gmail.com

---

**Last Updated**: December 2025