# Deployment Guide

This document provides detailed instructions for deploying the Dance Pose Analyzer to various cloud platforms.

## Prerequisites

- Docker installed locally
- Git repository set up
- Cloud platform account (AWS, GCP, or Railway)

## Option 1: Railway (Easiest)

Railway provides the simplest deployment with automatic Docker support.

### Steps:

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize project**
   ```bash
   cd dance-pose-analyzer
   railway init
   ```

4. **Deploy**
   ```bash
   railway up
   ```

5. **Get your URL**
   ```bash
   railway domain
   ```

### Cost: Free tier available, then $5/month

## Option 2: AWS EC2

Best for full control and customization.

### Steps:

1. **Launch EC2 Instance**
   - Instance type: t2.medium (minimum)
   - AMI: Amazon Linux 2
   - Security group: Allow ports 22 (SSH) and 80 (HTTP)

2. **Connect to instance**
   ```bash
   ssh -i your-key.pem ec2-user@your-instance-ip
   ```

3. **Install Docker**
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   sudo usermod -a -G docker ec2-user
   ```

4. **Install Git**
   ```bash
   sudo yum install git -y
   ```

5. **Clone and deploy**
   ```bash
   git clone your-repo-url
   cd dance-pose-analyzer
   sudo docker build -t pose-analyzer .
   sudo docker run -d -p 80:8000 --restart unless-stopped pose-analyzer
   ```

6. **Access your API**
   - URL: `http://your-instance-ip`

### Cost: ~$20-30/month for t2.medium

## Option 3: Google Cloud Run

Serverless option that scales to zero.

### Steps:

1. **Install gcloud CLI**
   Follow: https://cloud.google.com/sdk/docs/install

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Build and push image**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/pose-analyzer
   ```

4. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy pose-analyzer \
     --image gcr.io/YOUR_PROJECT_ID/pose-analyzer \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --memory 2Gi \
     --timeout 300
   ```

5. **Get your URL**
   The deployment will output your service URL.

### Cost: Pay per use, free tier available

## Option 4: Render

Similar to Railway, easy deployment.

### Steps:

1. **Push code to GitHub**

2. **Go to Render Dashboard**
   - Create new Web Service
   - Connect your GitHub repo
   - Select "Docker" as environment
   - Click "Create Web Service"

3. **Configure**
   - Name: dance-pose-analyzer
   - Region: Choose nearest
   - Instance type: Starter ($7/month)

4. **Deploy**
   Render will automatically build and deploy.

### Cost: $7/month for starter plan

## Testing Deployment

After deploying to any platform, test with:

```bash
# Health check
curl https://your-url/health

# Upload test video
curl -X POST "https://your-url/api/analyze" \
  -F "video=@test_dance.mp4" \
  -o response.json

# Download result
video_id=$(cat response.json | grep -o '"video_id":"[^"]*' | cut -d'"' -f4)
curl "https://your-url/api/download/$video_id" -o processed.mp4
```

## Monitoring

### Check Docker Logs (EC2)
```bash
sudo docker logs -f pose-analyzer
```

### Railway Logs
```bash
railway logs
```

### Cloud Run Logs
```bash
gcloud run services logs read pose-analyzer --limit=50
```

## Troubleshooting

### Issue: Out of memory
**Solution**: Increase instance memory or upgrade plan

### Issue: Video processing timeout
**Solution**: Increase timeout settings in your cloud platform

### Issue: Container won't start
**Solution**: Check logs for dependency issues, ensure all packages install correctly

## Security Considerations

1. **HTTPS**: Use cloud platform's built-in SSL/TLS
2. **API Keys**: Add authentication if needed
3. **File Size Limits**: Configure in FastAPI
4. **Rate Limiting**: Add rate limiting for production

## Performance Optimization

1. **Use GPU instances** for faster processing (if available)
2. **Add Redis caching** for repeated requests
3. **Implement queue system** for async processing
4. **Enable CDN** for faster downloads

## Recommended: Railway or Render

For this assignment, I recommend **Railway** or **Render** because:
- Fastest to deploy
- Automatic HTTPS
- Easy to demonstrate in video
- Free or low cost
- No server management needed
