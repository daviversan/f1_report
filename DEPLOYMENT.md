# Deployment Guide

## Prerequisites

**PowerShell:**
```powershell
# 1. Set project
gcloud config set project gen-lang-client-0467867580

# 2. Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable aiplatform.googleapis.com

# 3. Grant Cloud Build permissions
$PROJECT_NUMBER = gcloud projects describe gen-lang-client-0467867580 --format="value(projectNumber)"
gcloud projects add-iam-policy-binding gen-lang-client-0467867580 --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding gen-lang-client-0467867580 --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding gen-lang-client-0467867580 --member="serviceAccount:$PROJECT_NUMBER@cloudbuild.gserviceaccount.com" --role="roles/storage.admin"
```

**Bash/Linux/Mac:**
```bash
# 1. Set project
gcloud config set project gen-lang-client-0467867580

# 2. Enable APIs
gcloud services enable cloudbuild.googleapis.com containerregistry.googleapis.com run.googleapis.com aiplatform.googleapis.com

# 3. Grant Cloud Build permissions
PROJECT_NUMBER=$(gcloud projects describe gen-lang-client-0467867580 --format="value(projectNumber)")
gcloud projects add-iam-policy-binding gen-lang-client-0467867580 --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" --role="roles/run.admin"
gcloud projects add-iam-policy-binding gen-lang-client-0467867580 --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" --role="roles/iam.serviceAccountUser"
gcloud projects add-iam-policy-binding gen-lang-client-0467867580 --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" --role="roles/storage.admin"
```

## Deploy

```bash
gcloud builds submit --config cloudbuild.yaml
```

Get service URL:
```bash
gcloud run services describe f1-report-system --region us-central1 --format 'value(status.url)'
```

## Test API

```bash
# Health check
curl https://YOUR_SERVICE_URL/

# Generate report
curl -X POST https://YOUR_SERVICE_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{"race_input": "Monaco"}'

# List reports
curl https://YOUR_SERVICE_URL/history
```

## Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

## Troubleshooting

- **API not enabled**: Run prerequisite commands above
- **Permission denied**: Grant Cloud Build service account roles
- **Build fails**: Check logs with `gcloud builds log [BUILD_ID]`
- **Service errors**: Check logs with `gcloud run logs read f1-report-system`
