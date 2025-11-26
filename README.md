# F1 Race Report Generator

Two-agent system for generating F1 race social media posts with persistent memory storage.

## Architecture

**Agent 1: Data Collection** - Validates input, retrieves race data using FastF1  
**Agent 2: Report Generation** - Generates social media content using Gemini 2.5 Flash  
**Memory: Persistent Storage** - Local JSON backup with search capabilities

## Quick Start

### Deploy to Cloud Run

```bash
# 1. Setup (one-time)
gcloud config set project gen-lang-client-0467867580
gcloud services enable cloudbuild.googleapis.com containerregistry.googleapis.com run.googleapis.com aiplatform.googleapis.com

# 2. Deploy
gcloud builds submit --config cloudbuild.yaml

# 3. Get URL
gcloud run services describe f1-report-system --region us-central1 --format 'value(status.url)'
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete setup.

### Interactive Notebook

```bash
jupyter notebook f1_report_notebook.ipynb
# Or upload to Kaggle Notebooks
```

### Local Development

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

## API Usage

```bash
# Generate report
curl -X POST https://SERVICE_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{"race_input": "Monaco"}'

# List reports
curl https://SERVICE_URL/history

# Search
curl -X POST https://SERVICE_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Monaco"}'
```

See [API.md](API.md) for complete API reference.

## Kaggle Submission

- **Notebook**: `f1_report_notebook.ipynb` - Interactive execution
- **Cloud Run**: Deploy for live API demo
- **Local Docker**: Test without GCP setup

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- [API.md](API.md) - API documentation
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Architecture

## Requirements

- Google Cloud Project (Vertex AI, Cloud Run APIs enabled)
- Python 3.11+
- Docker (for deployment)
