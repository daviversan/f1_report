# F1 Race Report Generator

Generate social media posts for F1 races with memory storage.

## Quick Start

1. Open `f1_report_notebook.ipynb`
2. Run all cells
3. Generate reports for any 2024/2025 race

## Memory Workflow

Uses **Vertex AI Memory Bank** for persistent storage:

- **Initialize**: Creates/connects to Agent Engine on startup
- **Ingest**: `memory.add_session_to_memory()` - stores reports persistently
- **Retrieve**: `memory.search_memory()` - finds reports (survives restarts)

## Example Usage

```python
# Generate and store report
report = generate_f1_report("Bahrain")

# Search memory
search_reports("Bahrain")

# List all
list_reports()

# Get specific report
get_report("2024_R1")
```

## Requirements

- Google Cloud Project with Vertex AI enabled
- Vertex AI Agent Engine (auto-created on first run)
- FastF1 library
- Set `GCP_PROJECT_ID` and `GCP_LOCATION` in `.env`

## Setup Notes

- First run creates a Vertex AI Agent Engine instance (persistent resource)
- Reports are stored in Vertex AI Memory Bank and persist across restarts
- The system uses a local cache for quick access with Memory Bank backup

