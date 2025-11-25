# Project Structure

## Overview

F1 Report System: Two-agent system for generating F1 race reports with memory storage.

## Directory Structure

```
f1_report/
├── main.py                      # FastAPI Cloud Run application
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Container configuration
├── deploy.sh                    # Automated deployment script
├── cloudbuild.yaml             # Cloud Build configuration
├── .dockerignore               # Docker build exclusions
├── .gcloudignore              # gcloud deployment exclusions
├── .gitignore                 # Git exclusions
├── .env.example               # Environment variables template
├── README.md                  # Project overview
├── DEPLOYMENT.md             # Deployment instructions
├── API.md                    # API documentation
├── f1_report_notebook.ipynb # Jupyter notebook implementation
├── f1_reports_backup.json   # Local memory backup
└── f1_cache/                # FastF1 data cache
    ├── 2024/
    └── 2025/
```

## Core Components

### Cloud Run Deployment Files

- **main.py**: FastAPI application with agent orchestration
  - DataCollectionAgent: Validates input and retrieves race data
  - ReportGenerationAgent: Generates social media posts using Gemini
  - MemoryService: Manages persistent storage with Vertex AI Memory Bank
  - REST API endpoints for analysis, search, and retrieval

- **requirements.txt**: Production dependencies
  - FastAPI, uvicorn for web service
  - google-cloud-aiplatform, google-adk for Vertex AI
  - fastf1 for race data
  - pandas for data processing

- **Dockerfile**: Multi-stage build for Cloud Run
  - Python 3.11 slim base
  - System dependencies (gcc, g++)
  - Application code and cache directory

- **deploy.sh**: Automated deployment script
  - Builds Docker image
  - Pushes to GCR
  - Deploys to Cloud Run with configuration

- **cloudbuild.yaml**: Cloud Build pipeline
  - Build, push, and deploy steps
  - Environment variable configuration
  - Resource allocation (2Gi RAM, 2 CPU)

### Configuration Files

- **.dockerignore**: Excludes from Docker build
  - Python cache, virtual environments
  - Jupyter notebooks and checkpoints
  - Cache files, backups
  - Documentation and IDE files

- **.gcloudignore**: Excludes from gcloud deployment
  - Similar to dockerignore but for Cloud SDK

- **.gitignore**: Excludes from version control
  - Python artifacts, cache files
  - Environment variables
  - IDE files, logs

- **.env.example**: Environment variables template
  - GCP_PROJECT_ID
  - GCP_LOCATION

### Documentation

- **README.md**: Project overview and quick start
  - Architecture description
  - Deployment options
  - API usage examples

- **DEPLOYMENT.md**: Detailed deployment guide
  - Prerequisites and setup
  - Three deployment methods
  - Troubleshooting tips

- **API.md**: Complete API reference
  - Endpoint documentation
  - Request/response examples
  - Error handling

### Implementation

- **f1_report_notebook.ipynb**: Jupyter notebook implementation
  - Interactive development environment
  - Complete agent system
  - Memory management functions
  - Example usage cells

### Data Files

- **f1_reports_backup.json**: Local memory backup
  - Stores generated reports
  - JSON format for portability
  - Synced with Vertex AI Memory Bank

- **f1_cache/**: FastF1 data cache
  - Stores race session data
  - Organized by year and GP
  - SQLite database for HTTP cache
  - Improves performance and reduces API calls

## Deployment Targets

### Option 1: Cloud Run (Production)

RESTful API service with:
- Automatic scaling
- Managed infrastructure
- HTTPS endpoints
- Memory persistence

### Option 2: Kaggle Notebook (Development)

Interactive environment with:
- Vertex AI integration
- Real-time testing
- Memory Bank connectivity
- Manual execution

## Key Features

1. **Two-Agent Architecture**
   - Agent 1: Data collection and validation
   - Agent 2: Report generation with Gemini

2. **Persistent Memory**
   - Vertex AI Memory Bank
   - Local JSON backup
   - Search and retrieval

3. **Robust Data Retrieval**
   - FastF1 primary source
   - Automatic year fallback
   - Comprehensive race data

4. **REST API**
   - Generate reports
   - Search history
   - Retrieve specific reports

5. **Production Ready**
   - Containerized deployment
   - Health checks
   - Error handling
   - Resource optimization

## Dependencies

- Python 3.11+
- Google Cloud Platform
- Vertex AI API
- Cloud Run API
- Docker (for local builds)

