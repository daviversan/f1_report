## F1 Race Report Generator

**Objective**  
Generate engaging F1 race recap posts from official timing data using a two‑agent GenAI system with persistent memory, suitable for the Kaggle Agents Intensive Capstone Project.

### Project Overview
- **Data source**: Live timing and results via `fastf1`.
- **Output**: 200–250 word, Instagram-style race recap text.
- **Interface options**:
  - Kaggle Notebook: `f1_report_notebook.ipynb`.
  - Optional FastAPI service: `main.py` (for local/API use, not required for Kaggle).

### GenAI Capabilities Demonstrated
- **Agents**: Two-agent architecture (data collection agent + report generation agent).
- **Memory / Retrieval**: Persistent store of past race reports with search and retrieval (`f1_reports_backup.json` + `MemoryService`).
- **MLOps with GenAI**: Optional containerized FastAPI service (`main.py`, `Dockerfile`) that can be deployed and monitored outside Kaggle.

### How to Run (Kaggle Notebook)
1. **Open the notebook**: Upload `f1_report_notebook.ipynb` to Kaggle and attach a Python 3 GPU/CPU runtime.  
2. **Install dependencies** (first cell already contains `%pip install ...` for `google-cloud-aiplatform`, `google-adk`, `fastf1`, `pandas`, `nest-asyncio`).  
3. **Configure credentials**: Follow the course instructions to authenticate with Google Cloud / Vertex AI in the notebook environment.  
4. **Run cells in order**:  
   - Initialize FastF1 cache and Vertex AI.  
   - Use the provided functions to request a race by round number or GP name.  
   - Inspect the generated social media post and stored history.

### How to Run Locally (Optional)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```
Then call the API (e.g. from a REST client) at `http://localhost:8080/analyze` with JSON body `{"race_input": "Monaco"}`.

### How to Test the Features

Assuming you are running locally (`http://localhost:8080`) or have a Cloud Run URL (for example, `https://YOUR_SERVICE_URL`):

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

For Cloud Run, replace `http://localhost:8080` with your service URL (for example, `https://f1-report-system-xxxx-uc.a.run.app`).

### How to Deploy on Cloud Run 
You can deploy the same FastAPI service from this repo using Google Cloud:

```bash
export PROJECT_ID=YOUR_PROJECT_ID
gcloud config set project $PROJECT_ID
gcloud services enable cloudbuild.googleapis.com run.googleapis.com containerregistry.googleapis.com aiplatform.googleapis.com

gcloud builds submit --config cloudbuild.yaml
gcloud run services describe f1-report-system --region us-central1 --format='value(status.url)'
```
Use the returned URL as the base URL (e.g. `https://.../analyze`) for the API.

**Deployed demo**  
`https://f1-report-system-178353823233.us-central1.run.app`

### Files to Know
- `f1_report_notebook.ipynb`: Main Kaggle notebook (primary artifact for evaluation).
- `main.py`: FastAPI application implementing the same two-agent system with memory.
- `requirements.txt`: Minimal dependencies for local/API use.
- `f1_cache/`: FastF1 cache (can be recreated; not required to upload to Kaggle).
- `f1_reports_backup.json`: Local JSON backup of generated reports (optional to include in Kaggle).
