# Cloud Deployment Guide

This guide walks you through deploying the Dance Pose Analyzer to production cloud environments.

## Table of Contents
- [Railway Deployment (Recommended)](#railway-deployment-recommended)
- [Render Deployment](#render-deployment)
- [AWS EC2 Deployment](#aws-ec2-deployment)
- [Post-Deployment Testing](#post-deployment-testing)

---

## Railway Deployment (Recommended)

Why Railway? Free tier includes 500 hours/month, automatic HTTPS, GitHub integration, zero config needed.

### Prerequisites
- GitHub account
- Railway account (free tier available)

### Steps

#### 1. Push to GitHub

```bash
# Create a new repository on GitHub first at https://github.com/new
# Then push your code:

cd /path/to/dance-pose-analyzer
git remote add origin https://github.com/YOUR_USERNAME/dance-pose-analyzer.git
git branch -M main
git push -u origin main
```

#### 2. Deploy via Railway Dashboard

1. Go to [railway.app](https://railway.app/) and sign in with GitHub
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your `dance-pose-analyzer` repository
4. Railway will auto-detect the Dockerfile and deploy

#### 3. Configure Environment

Railway auto-configures most settings, but verify:
- **Port**: Should auto-detect `8000` from Dockerfile
- **Start Command**: Uses `CMD` from Dockerfile (already configured)

#### 4. Get Your URL

Once deployed (takes 2-3 minutes):
- Railway provides a URL like: `https://dance-pose-analyzer-production-XXXX.up.railway.app`
- Click **"Generate Domain"** if not auto-generated
- Test: `curl https://your-app.railway.app/health`

#### 5. Verify Deployment

```bash
# Test health endpoint
curl https://your-app.railway.app/health

# Test API docs
open https://your-app.railway.app/docs
```

---

## Render Deployment

Why Render? Free tier includes 750 hours/month, similar to Railway but with more manual config.

### Steps

#### 1. Create `render.yaml` (already done)

This file should be in your project root:

```yaml
services:
  - type: web
    name: dance-pose-analyzer
    env: docker
    plan: free
    healthCheckPath: /health
```

#### 2. Connect GitHub to Render

1. Go to [render.com](https://render.com/) and sign in
2. Click **"New"** → **"Web Service"**
3. Connect your GitHub repository
4. Render auto-detects Dockerfile

#### 3. Configure Settings

- **Name**: `dance-pose-analyzer`
- **Environment**: Docker
- **Region**: Choose closest to your users
- **Instance Type**: Free
- **Health Check Path**: `/health`

#### 4. Deploy

- Click **"Create Web Service"**
- Render builds and deploys (3-5 minutes)
- URL provided: `https://dance-pose-analyzer.onrender.com`

**Note**: Free tier spins down after 15 mins of inactivity. First request after idle takes ~30 seconds.

---

## AWS EC2 Deployment

Why AWS? Full control, production-grade, but requires more setup.

### Prerequisites
- AWS account
- SSH key pair

### Steps

#### 1. Launch EC2 Instance

```bash
# Using AWS CLI (or use AWS Console)
aws ec2 run-instances \
  --image-id ami-0c55b159cbfafe1f0 \  # Amazon Linux 2
  --instance-type t2.medium \
  --key-name your-key-pair \
  --security-groups launch-wizard-1
```

#### 2. Configure Security Group

Allow inbound traffic:
- **Port 80** (HTTP): 0.0.0.0/0
- **Port 22** (SSH): Your IP only

#### 3. SSH into Instance

```bash
ssh -i your-key.pem ec2-user@your-instance-ip
```

#### 4. Install Docker

```bash
sudo yum update -y
sudo yum install docker git -y
sudo service docker start
sudo usermod -a -G docker ec2-user
exit  # Log out and back in for group changes to take effect
```

#### 5. Clone and Deploy

```bash
git clone https://github.com/YOUR_USERNAME/dance-pose-analyzer.git
cd dance-pose-analyzer

docker build -t pose-analyzer .
docker run -d -p 80:8000 --name pose-api pose-analyzer
```

#### 6. Test Deployment

```bash
curl http://your-ec2-public-ip/health
```

#### 7. Setup HTTPS (Optional but Recommended)

```bash
# Install Caddy (automatic HTTPS)
sudo yum install caddy -y

# Create Caddyfile
cat > Caddyfile <<EOF
your-domain.com {
    reverse_proxy localhost:8000
}
EOF

sudo caddy start
```

---

## Post-Deployment Testing

### 1. Health Check

```bash
curl https://your-deployment-url/health
```

Expected response:
```json
{"status": "healthy", "service": "dance-pose-analyzer"}
```

### 2. API Documentation

Open in browser:
```
https://your-deployment-url/docs
```

You should see the Swagger UI.

### 3. Upload Test Video

```bash
# Using curl
curl -X POST "https://your-deployment-url/api/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "video=@test_video.mp4"
```

Expected response:
```json
{
  "success": true,
  "video_id": "some-uuid",
  "status": "completed",
  "download": {
    "url": "/api/download/some-uuid",
    "direct_link": "https://your-deployment-url/api/download/some-uuid"
  }
}
```

### 4. Download Processed Video

```bash
curl -O "https://your-deployment-url/api/download/some-uuid"
```

### 5. Load Testing (Optional)

```bash
# Install hey (HTTP load testing tool)
brew install hey  # macOS
# or: go install github.com/rakyll/hey@latest

# Test with 100 requests, 10 concurrent
hey -n 100 -c 10 https://your-deployment-url/health
```

---

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
# Railway
railway logs

# Render
# View logs in dashboard

# AWS EC2
docker logs pose-api
```

**Common issues:**
- **Port mismatch**: Ensure Dockerfile `EXPOSE 8000` and code uses port 8000
- **Missing dependencies**: Check `requirements.txt` includes all packages
- **Memory limit**: Upgrade to larger instance if OOM errors

### Slow Video Processing

**Solution**: Upgrade instance type
- Railway: Upgrade to Pro plan ($5/month for 8GB RAM)
- Render: Upgrade to Starter ($7/month for 512MB RAM)
- AWS: Use t2.large (2 vCPUs, 8GB RAM)

### Upload Fails

**Check file size limits:**
```python
# Add to api.py
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
```

**Increase timeout** (for large videos):
```dockerfile
# In Dockerfile, add:
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--timeout-keep-alive", "300"]
```

---

## Deployment URLs

After deploying, update this section in the main README.md:

```markdown
## Live Demo

- **API Endpoint**: https://your-app.railway.app
- **API Documentation**: https://your-app.railway.app/docs
- **Health Check**: https://your-app.railway.app/health
```

---

## Cost Estimates

| Platform | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| **Railway** | 500 hrs/mo | $5/mo (8GB RAM) | Quick demos, hobby projects |
| **Render** | 750 hrs/mo | $7/mo (512MB RAM) | Persistent free apps |
| **AWS EC2** | 750 hrs/mo (1st year) | $0.046/hr (t2.medium) | Production, full control |

**Recommendation for Assignment**: Use Railway for fastest deployment and demo purposes.

---

## Security Checklist

Before going to production:

- [ ] Enable HTTPS (automatic on Railway/Render)
- [ ] Add rate limiting (see README Security section)
- [ ] Set file size limits
- [ ] Configure CORS properly (whitelist domains)
- [ ] Add authentication (JWT tokens)
- [ ] Setup monitoring (Sentry, LogDNA)
- [ ] Configure auto-cleanup for old videos
- [ ] Add health check alerts

---

## Next Steps

1. Deploy to your chosen platform
2. Test all endpoints with real videos
3. Update main README.md with deployment URL
4. Record demo video showing deployed API
5. Submit assignment with GitHub link + live URL
