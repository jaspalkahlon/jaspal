# Fashion Guru Bot - Google Cloud Deployment Guide

## Overview

This guide will help you deploy Fashion Guru Bot to Google Cloud Platform (GCP) using **Google Cloud Run** - a fully managed serverless platform.

## Prerequisites

1. **Google Cloud Account** - [Create one here](https://cloud.google.com/free)
2. **Google Cloud SDK (gcloud CLI)** - [Install guide](https://cloud.google.com/sdk/docs/install)
3. **Docker** - [Install guide](https://docs.docker.com/get-docker/)

## Deployment Options

We'll use **Cloud Run** (recommended for this bot):
- **Pros**: Serverless, auto-scaling, pay-per-use, easy deployment
- **Cons**: None for this use case
- **Cost**: Free tier includes 2 million requests/month

## Step-by-Step Deployment

### Step 1: Install Google Cloud SDK

**macOS/Linux:**
```bash
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
gcloud init
```

**Windows:**
Download and run the installer from: https://cloud.google.com/sdk/docs/install

### Step 2: Authenticate and Setup

```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace YOUR_PROJECT_ID)
gcloud config set project YOUR_PROJECT_ID

# If you don't have a project yet, create one:
gcloud projects create fashion-guru-bot --name="Fashion Guru Bot"
gcloud config set project fashion-guru-bot

# Enable required APIs
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### Step 3: Build and Deploy

From your project directory (`/home/user/jaspal`):

```bash
# Deploy to Cloud Run (this builds and deploys in one command)
gcloud run deploy fashion-guru-bot \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000 \
  --memory 512Mi \
  --timeout 300

# Note: The build will take 3-5 minutes on first deployment
```

**What this does:**
- Builds a container from your code
- Pushes it to Google Container Registry
- Deploys to Cloud Run
- Gives you a public URL

### Step 4: Get Your Deployment URL

After deployment completes, you'll see:
```
Service [fashion-guru-bot] revision [fashion-guru-bot-00001-xxx] has been deployed
and is serving 100 percent of traffic.
Service URL: https://fashion-guru-bot-xxxxx-uc.a.run.app
```

**Save this URL!** This is your bot's public endpoint.

### Step 5: Test Your Deployment

```bash
# Health check
curl https://YOUR-SERVICE-URL/health

# Test chat endpoint
curl -X POST https://YOUR-SERVICE-URL/chat \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test_user_001",
    "message": "What fabric should I use for a summer dress?"
  }'
```

## Environment Variables (Optional)

If you need to set environment variables:

```bash
gcloud run services update fashion-guru-bot \
  --region us-central1 \
  --set-env-vars LOG_LEVEL=INFO,API_DEBUG=false
```

## Monitoring and Logs

### View Logs
```bash
# Stream logs in real-time
gcloud run services logs tail fashion-guru-bot --region us-central1

# View logs in Cloud Console
# Go to: https://console.cloud.google.com/run
# Click on your service > Logs
```

### View Metrics
```bash
# Open in browser
gcloud run services describe fashion-guru-bot \
  --region us-central1 \
  --format="value(status.url)"
```

## Scaling Configuration

Cloud Run auto-scales, but you can configure limits:

```bash
gcloud run services update fashion-guru-bot \
  --region us-central1 \
  --min-instances 0 \
  --max-instances 10 \
  --concurrency 80
```

## Cost Estimation

**Cloud Run Free Tier (per month):**
- 2 million requests
- 360,000 GB-seconds of memory
- 180,000 vCPU-seconds

**Expected costs for Fashion Guru Bot:**
- Low traffic (<1000 requests/day): **$0/month** (within free tier)
- Medium traffic (10,000 requests/day): **~$5-10/month**
- High traffic (100,000 requests/day): **~$50-100/month**

## Updating Your Deployment

When you make code changes:

```bash
# Just redeploy - Cloud Run handles versioning
gcloud run deploy fashion-guru-bot \
  --source . \
  --platform managed \
  --region us-central1
```

## Security Best Practices

### Add Authentication (Optional)

```bash
# Require authentication
gcloud run services update fashion-guru-bot \
  --region us-central1 \
  --no-allow-unauthenticated

# Now users need to be authenticated to access
# Good for internal/team use
```

### Add API Key Protection

For production, add API key middleware to your Flask app (see security section below).

## Alternative: Deploy to Google App Engine

If you prefer App Engine over Cloud Run:

1. Create `app.yaml`:
```yaml
runtime: python39
entrypoint: gunicorn -b :$PORT src.main:app

env_variables:
  LOG_LEVEL: INFO

automatic_scaling:
  target_cpu_utilization: 0.65
  min_instances: 0
  max_instances: 10
```

2. Deploy:
```bash
gcloud app deploy
```

## Troubleshooting

### Issue: Build fails

**Solution:** Check that Dockerfile exists (we'll create it next)

### Issue: Service won't start

**Solution:** Check logs:
```bash
gcloud run services logs read fashion-guru-bot --region us-central1 --limit 50
```

### Issue: Timeout errors

**Solution:** Increase timeout:
```bash
gcloud run services update fashion-guru-bot \
  --region us-central1 \
  --timeout 300
```

### Issue: Out of memory

**Solution:** Increase memory:
```bash
gcloud run services update fashion-guru-bot \
  --region us-central1 \
  --memory 1Gi
```

## Testing Checklist

After deployment, test these endpoints:

- [ ] `GET /health` - Should return healthy status
- [ ] `POST /chat` - Should return bot response
- [ ] `GET /modules` - Should list all modules
- [ ] `GET /stats` - Should show statistics

## Local Testing Before Deployment

Before deploying to GCP, test locally with Docker:

```bash
# Build locally
docker build -t fashion-guru-bot .

# Run locally
docker run -p 5000:5000 fashion-guru-bot

# Test
curl http://localhost:5000/health
```

## CI/CD Integration (Advanced)

Set up automatic deployment with Cloud Build:

1. Create `cloudbuild.yaml`
2. Connect to GitHub repository
3. Auto-deploy on push to main branch

(See separate CI/CD guide for details)

## Support

If you encounter issues:
1. Check logs: `gcloud run services logs tail fashion-guru-bot`
2. Review Cloud Console: https://console.cloud.google.com/run
3. Check billing: https://console.cloud.google.com/billing
4. Stack Overflow: Tag questions with `google-cloud-run`

## Next Steps

After successful deployment:
1. Set up custom domain (optional)
2. Configure monitoring alerts
3. Add authentication if needed
4. Set up CI/CD pipeline
5. Monitor usage and costs

---

**Your Fashion Guru Bot is now running on Google Cloud! 🚀**
