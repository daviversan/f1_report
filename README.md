# F1 Report System

AI-powered F1 race report generator using Vertex AI Gemini 1.5 Flash and FastF1.

## Overview

Two-agent system that:
1. **Agent 1 (Data Collection)**: Validates user input and retrieves F1 race data
2. **Agent 2 (Report Generation)**: Creates structured social media content

## Quick Start

Run these cells in order:
1. Cell 1: Install dependencies (1-2 minutes)
2. Cell 2: Import libraries
3. Cell 3: Configure Vertex AI and FastF1
4. Cell 4: Initialize session memory
5. Cell 5: Load F1 2025 calendar
6. Cell 6: Initialize F1 data tools
7. Cell 7: Run tests (validates setup)

Total time: 3-5 minutes on first run

## Technology Stack

- **AI Model**: Vertex AI Gemini 1.5 Flash
- **Data Source**: FastF1 (official F1 Python library)
- **Platform**: Jupyter Notebook / Kaggle
- **Language**: Python 3.8+

## Requirements

### Python Packages
- google-cloud-aiplatform
- fastf1
- pandas
- python-dotenv

### Google Cloud
- GCP Project with Vertex AI API enabled
- Authentication configured

## Features

### Data Retrieval
- Event information (GP names, dates, circuits)
- Race results (positions, times, points)
- Qualifying results
- Driver information
- Historical data (2018-present)

### Session Management
- In-memory report storage
- Query history tracking

### F1 Calendar
- Complete 2025 season (24 races)
- Circuit information
- Input validation

## Data Coverage

FastF1 provides:
- Official F1 timing data
- Real-time race information
- Historical archives
- Driver statistics
- Team data

## Troubleshooting

**Import errors**: Restart kernel and rerun Cell 1

**Slow first run**: FastF1 downloads ~50MB on first use (cached thereafter)

**Test failures**: Check internet connection, wait 30 seconds, retry

## Project Structure

```
f1_report_notebook.ipynb  - Main notebook (15 cells)
README.md                 - This file
f1_cache/                 - FastF1 data cache (created automatically)
```

## Next Steps

After successful setup:
1. Build Agent 1 (Data Collection)
2. Build Agent 2 (Report Generation)
3. Deploy to production

## Documentation

- FastF1: https://docs.fastf1.dev/
- Vertex AI: https://cloud.google.com/vertex-ai/docs

## Status

Ready for agent development. All data retrieval tested and working.
