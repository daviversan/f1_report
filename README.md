# F1 Race Report Generator

Two-agent system for generating engaging F1 race social media posts with persistent memory storage.

## Architecture

**Agent 1: Data Collection**
- Validates user input (GP name or round number)
- Retrieves race data using FastF1
- Automatic fallback to previous year if data unavailable

**Agent 2: Report Generation**
- Generates engaging social media content using Gemini 2.5 Flash
- Creates 200-250 word Instagram-optimized posts
- Includes race story and key highlights

**Memory: Persistent Storage**
- Vertex AI Memory Bank for cloud storage
- Local JSON backup for quick access
- Search and retrieval capabilities

## Quick Start

### Option 1: Interactive Notebook

```bash
# Open the Jupyter notebook
jupyter notebook f1_report_notebook.ipynb

# Or use in Kaggle
# Upload f1_report_notebook.ipynb to Kaggle
```

Run all cells and use:

```python
# Generate a report
report = generate_f1_report("Monaco")

# Search reports
search_reports("Monaco")

# List all reports
list_reports()
```

### Option 2: Cloud Run API

Deploy as a REST API service:

```bash
# Quick deployment (Linux/Mac)
chmod +x deploy.sh
./deploy.sh

# Using Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Manual deployment
docker build -t gcr.io/PROJECT_ID/f1-report-system .
docker push gcr.io/PROJECT_ID/f1-report-system
gcloud run deploy f1-report-system --image gcr.io/PROJECT_ID/f1-report-system
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

## API Usage

```bash
# Generate race report
curl -X POST https://SERVICE_URL/analyze \
  -H "Content-Type: application/json" \
  -d '{"race_input": "Monaco"}'

# List all reports
curl https://SERVICE_URL/history

# Search reports
curl -X POST https://SERVICE_URL/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Monaco"}'

# Get specific report
curl https://SERVICE_URL/report/2025_R8
```

See [API.md](API.md) for complete API reference.

## Configuration

Create `.env` file:

```bash
cp .env.example .env
```

Edit with your Google Cloud configuration:

```
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
```

## Features

- Input validation for GP names and round numbers
- Comprehensive race data collection (podium, grid positions, results)
- AI-generated social media content
- Persistent memory with search capabilities
- RESTful API for integration
- Automatic data caching for performance
- Year fallback for unavailable data

## Requirements

- Google Cloud Project with Vertex AI API enabled
- Cloud Run API enabled (for deployment)
- Python 3.11+
- Docker (for deployment)

## Documentation

- [DEPLOYMENT.md](DEPLOYMENT.md) - Detailed deployment guide
- [API.md](API.md) - Complete API documentation
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) - Project architecture

## Race Coverage

Supports all 2024/2025 F1 races:
- 24 races per season
- All circuits and GPs
- Automatic data retrieval from FastF1
- Fallback to previous year if current data unavailable

## Data Sources

- **Primary**: FastF1 library (official F1 timing data)
- **Cache**: Local cache for improved performance
- **Fallback**: Automatic year fallback for recent races

## License

See project license file for details.

