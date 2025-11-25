# Deployment Guide

## Prerequisites

- Google Cloud Project with billing enabled
- Vertex AI API enabled
- Cloud Run API enabled
- Docker installed locally
- gcloud CLI installed and authenticated

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

Edit `.env` with your project details:

```
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
```

## Deployment Methods

### Method 1: Automated Deployment Script

```bash
chmod +x deploy.sh
./deploy.sh
```

### Method 2: Cloud Build

```bash
gcloud builds submit --config cloudbuild.yaml
```

### Method 3: Manual Deployment

1. Build the container:

```bash
docker build -t gcr.io/PROJECT_ID/f1-report-system .
```

2. Push to Google Container Registry:

```bash
docker push gcr.io/PROJECT_ID/f1-report-system
```

3. Deploy to Cloud Run:

```bash
gcloud run deploy f1-report-system \
  --image gcr.io/PROJECT_ID/f1-report-system \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars GCP_PROJECT_ID=PROJECT_ID,GCP_LOCATION=us-central1
```

## API Usage

After deployment, get your service URL:

```bash
gcloud run services describe f1-report-system \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)'
```

### Generate Race Report

```bash
curl -X POST https://SERVICE_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{"race_input": "Monaco"}'
```

### List All Reports

```bash
curl https://SERVICE_URL/history
```

### Search Reports

```bash
curl -X POST https://SERVICE_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Monaco"}'
```

### Get Specific Report

```bash
curl https://SERVICE_URL/report/2025_R8
```

## Local Development

Run locally with uvicorn:

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

Access the API at `http://localhost:8080`

## Resource Configuration

The default configuration uses:

- Memory: 2Gi
- CPU: 2 cores
- Timeout: 300 seconds (5 minutes)

Adjust these in `cloudbuild.yaml` or deployment script as needed.

## Troubleshooting

### Build Failures

- Ensure Docker is running
- Check that all required APIs are enabled
- Verify authentication with `gcloud auth list`

### Runtime Errors

- Check Cloud Run logs: `gcloud run logs read f1-report-system`
- Verify environment variables are set correctly
- Ensure Vertex AI Agent Engine is created

### Data Issues

- FastF1 requires internet access for race data
- Cache directory is created automatically
- Recent races may not have data available yet

