#!/bin/bash

# F1 Report System - Cloud Run Deployment Script

set -e

# Configuration
PROJECT_ID=${GCP_PROJECT_ID:-"gen-lang-client-0467867580"}
REGION=${GCP_LOCATION:-"us-central1"}
SERVICE_NAME="f1-report-system"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "Deploying F1 Report System to Cloud Run"
echo "Project: ${PROJECT_ID}"
echo "Region: ${REGION}"
echo ""

# Build container image
echo "Building container image..."
docker build -t ${IMAGE_NAME}:latest .

# Push to Google Container Registry
echo "Pushing image to GCR..."
docker push ${IMAGE_NAME}:latest

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy ${SERVICE_NAME} \
  --image ${IMAGE_NAME}:latest \
  --platform managed \
  --region ${REGION} \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --set-env-vars GCP_PROJECT_ID=${PROJECT_ID},GCP_LOCATION=${REGION} \
  --project ${PROJECT_ID}

echo ""
echo "Deployment complete!"
echo "Service URL:"
gcloud run services describe ${SERVICE_NAME} \
  --platform managed \
  --region ${REGION} \
  --format 'value(status.url)' \
  --project ${PROJECT_ID}

