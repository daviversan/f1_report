# F1 Race Report Generator

## Problem

Formula 1 generates large amounts of race data (timing, positions, driver info, weather) that is difficult to summarize into engaging social media content. Manual report creation is time-consuming and inconsistent. There is a need for an automated system that:

- Retrieves official F1 race data from reliable sources
- Transforms raw timing data into narrative, engaging social media posts
- Maintains a memory of past reports for consistency and reference
- Handles flexible input (race names or round numbers)
- Provides both interactive notebook and API interfaces

## Solution

A two-agent Generative AI system that automates F1 race report generation:

1. **Data Collection Agent**: Validates user input (GP name or round number), retrieves comprehensive race data from FastF1 (official F1 timing data API), and structures it for analysis.

2. **Report Generation Agent**: Uses Google's Gemini 2.5 Flash model to transform structured race data into engaging 200-250 word Instagram-style posts that highlight key moments, podium finishes, and race storylines.

3. **Memory System**: Persistent storage of all generated reports with search and retrieval capabilities, enabling the system to reference past races and maintain consistency across reports.

The system is implemented as both a Kaggle notebook (primary submission artifact) and a production-ready FastAPI service deployable to Google Cloud Run.

## Architecture

### System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Input                              │
│              (GP Name: "Monaco" or Round: "8")                  │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Agent 1: Data Collection                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Input Validation (GP name ↔ round number mapping)      │  │
│  │ • FastF1 API Integration                                  │  │
│  │ • Race Data Extraction (results, podium, grid positions)  │  │
│  │ • Data Structuring                                        │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Structured Race │
                    │      Data        │
                    └────────┬─────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Agent 2: Report Generation                      │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Gemini 2.5 Flash Model                                 │  │
│  │ • Prompt Engineering (race context + podium data)        │  │
│  │ • Content Generation (200-250 word social media post)   │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Memory Service                              │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ • Vertex AI Memory Bank (primary)                        │  │
│  │ • Local JSON Backup (f1_reports_backup.json)             │  │
│  │ • Search & Retrieval Functions                           │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │  Generated Post │
                    │  + Stored Report│
                    └─────────────────┘
```

### Component Details

**Agent 1: DataCollectionAgent**
- Validates user input against F1 2025 calendar (24 races)
- Maps GP names to round numbers and vice versa
- Retrieves session data via FastF1 library
- Extracts: final positions, podium finishers, grid positions, lap times, points
- Handles edge cases (missing data, year fallback to 2024 if needed)

**Agent 2: ReportGenerationAgent**
- Uses Vertex AI GenerativeModel (Gemini 2.5 Flash)
- Receives structured race data from Agent 1
- Generates engaging narrative posts with:
  - Race context (GP name, circuit, year)
  - Podium highlights (winners, teams, grid-to-finish stories)
  - Key race moments and storylines
- Temperature: 0.5, Max tokens: 2048

**MemoryService**
- Dual storage: Vertex AI Memory Bank (when available) + local JSON backup
- Stores complete reports: race data + generated post + timestamp
- Search functionality: query by GP name or race_id
- Retrieval: get specific reports or list all stored reports

### GenAI Capabilities Demonstrated

This project demonstrates **three** Generative AI capabilities required for the Kaggle capstone:

1. **Agents**: Two-agent orchestration where Agent 1 handles data collection and Agent 2 handles content generation, with clear separation of concerns and sequential workflow.

2. **Memory / Retrieval**: Persistent memory system using Vertex AI Memory Bank (with local JSON fallback) that stores, searches, and retrieves past race reports, enabling the system to reference historical data.

3. **MLOps with GenAI**: Production-ready containerized FastAPI service (`main.py`, `Dockerfile`, `cloudbuild.yaml`) that can be deployed to Google Cloud Run, demonstrating how GenAI applications can be operationalized at scale.

## Setup Instructions

### Prerequisites

- **For Kaggle Notebook**: Kaggle account with access to Vertex AI / Google Cloud credentials
- **For Local/Cloud Run**: 
  - Python 3.11+
  - Google Cloud Project with Vertex AI API enabled
  - `gcloud` CLI installed (for Cloud Run deployment)

### Option 1: Kaggle Notebook (Primary Submission)

1. **Upload notebook**: Upload `f1_report_notebook.ipynb` to Kaggle Notebooks
2. **Attach runtime**: Use Python 3 GPU or CPU runtime
3. **Configure credentials**: 
   - Add Google Cloud service account credentials to Kaggle Secrets
   - Key name: `GCP_SERVICE_ACCOUNT`
   - The notebook will automatically detect and use these credentials
4. **Run cells**: Execute cells in order:
   - Cell 1: Install dependencies (`%pip install ...`)
   - Cell 2: Imports and configuration
   - Cell 3: Initialize services (FastF1 cache, Vertex AI)
   - Cell 4+: Use the agent functions to generate reports

**Example usage in notebook:**
```python
# Generate report for Monaco GP
result = generate_race_report("Monaco")
print(result['social_media_post'])

# Search past reports
search_results = search_reports("Monaco")
print(search_results)
```

### Option 2: Local Development

1. **Clone repository**:
   ```bash
   git clone <repository-url>
   cd f1_report
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set environment variables** (create `.env` file or export):
   ```bash
   export GCP_PROJECT_ID=your-project-id
   export GCP_LOCATION=us-central1
   ```

5. **Run FastAPI service**:
   ```bash
   uvicorn main:app --reload --port 8080
   ```

6. **Test the API** (see Testing section below)

### Option 3: Deploy to Cloud Run

You can deploy the FastAPI service to Google Cloud Run for a production-ready API:

**PowerShell (Windows):**
```powershell
# Set your project ID
$PROJECT_ID = "YOUR_PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com aiplatform.googleapis.com

# Deploy using Cloud Build
gcloud builds submit --config cloudbuild.yaml

# Get service URL
gcloud run services describe f1-report-system --region us-central1 --format 'value(status.url)'
```

**Bash (Linux/Mac/Cloud Shell):**
```bash
export PROJECT_ID=YOUR_PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com aiplatform.googleapis.com

gcloud builds submit --config cloudbuild.yaml
gcloud run services describe f1-report-system --region us-central1 --format 'value(status.url)'
```

**Deployed demo**  
`https://f1-report-system-178353823233.us-central1.run.app`

## Testing the Features

### Testing Locally

If running locally at `http://localhost:8080`:

```bash
# 1. Health check
curl http://localhost:8080/

# 2. Generate a race report (by GP name or round number)
curl -X POST http://localhost:8080/analyze \
  -H "Content-Type: application/json" \
  -d '{"race_input": "Monaco"}'

# 3. List all stored reports
curl http://localhost:8080/history

# 4. Search reports (by GP name or race_id)
curl -X POST http://localhost:8080/search \
  -H "Content-Type: application/json" \
  -d '{"query": "Monaco"}'

# 5. Get a specific report (replace 2025_R8 with an ID from history/search)
curl http://localhost:8080/report/2025_R8
```

### Testing Cloud Run Deployment

Replace `http://localhost:8080` with your Cloud Run service URL:

**PowerShell:**
```powershell
$SERVICE_URL = "https://f1-report-system-178353823233.us-central1.run.app"

# Health check
curl "$SERVICE_URL/"

# Generate report
curl -Method POST "$SERVICE_URL/analyze" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"race_input": "Monaco"}'

# List reports
curl "$SERVICE_URL/history"

# Search reports
curl -Method POST "$SERVICE_URL/search" `
  -Headers @{ "Content-Type" = "application/json" } `
  -Body '{"query": "Monaco"}'

# Get specific report
curl "$SERVICE_URL/report/2025_R8"
```

**Bash:**
```bash
SERVICE_URL="https://f1-report-system-178353823233.us-central1.run.app"

curl "$SERVICE_URL/"
curl -X POST "$SERVICE_URL/analyze" -H "Content-Type: application/json" -d '{"race_input": "Monaco"}'
curl "$SERVICE_URL/history"
curl -X POST "$SERVICE_URL/search" -H "Content-Type: application/json" -d '{"query": "Monaco"}'
curl "$SERVICE_URL/report/2025_R8"
```

## Project Files

- **`f1_report_notebook.ipynb`**: Main Kaggle notebook (primary artifact for evaluation)
  - Complete two-agent system implementation
  - Memory service with search/retrieval
  - Example usage cells
  - Ready to run end-to-end on Kaggle

- **`main.py`**: FastAPI application
  - Same agent architecture as notebook
  - REST API endpoints (`/analyze`, `/history`, `/search`, `/report/{race_id}`)
  - Production-ready with error handling

- **`requirements.txt`**: Python dependencies
  - `google-cloud-aiplatform`: Vertex AI integration
  - `fastf1`: F1 data retrieval
  - `fastapi`, `uvicorn`: Web framework
  - `pandas`: Data processing

- **`Dockerfile`**: Container configuration for Cloud Run deployment

- **`cloudbuild.yaml`**: Google Cloud Build configuration for automated deployment

- **`f1_cache/`**: FastF1 data cache (can be recreated; not required for Kaggle submission)

- **`f1_reports_backup.json`**: Local JSON backup of generated reports (optional for Kaggle)

## License

This project is submitted for the Kaggle Agents Intensive Capstone Project evaluation.
