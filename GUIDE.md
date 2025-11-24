# Execution Guide

## Setup

Run cells in this order:

### Cell 1-2: Install Dependencies
Install required Python packages. Takes 1-2 minutes.

### Cell 3-4: Import Libraries  
Import all required modules.

### Cell 5-6: Configuration
Initialize Vertex AI and FastF1 cache.

### Cell 7-8: Session Memory
Create in-memory storage for reports.

### Cell 9-10: F1 Calendar
Load 2025 F1 season calendar (24 races).

### Cell 11-12: Data Tools
Initialize F1 data retrieval tools using FastF1.

### Cell 13-14: Test
Validate setup with 2024 Bahrain GP data.

## Expected Output

After Cell 14, you should see:
- Event info for Bahrain Grand Prix
- Top 3 race results
- Max Verstappen's driver information

## Troubleshooting

**Import errors**: Restart kernel, rerun Cell 1-2

**Slow first run**: Normal - FastF1 downloads data (cached for future use)

**Test failures**: Check internet connection, wait and retry

## Next Steps

After successful setup:
1. Build Data Collection Agent
2. Build Report Generation Agent
3. Integrate both agents
4. Deploy to production

## Data Available

F1DataTools provides three methods:
- `get_event_info(year, round)` - Race event details
- `get_session_results(year, round, session_type)` - Race/qualifying results
- `get_driver_info(driver, year)` - Driver information

## Example Usage

```python
# Get 2024 Monaco GP info
event = f1_tools.get_event_info(2024, 8)

# Get race results
results = f1_tools.get_session_results(2024, 8, "R")

# Get Lewis Hamilton's info
driver = f1_tools.get_driver_info("HAM", 2024)
```

## Total Time

First run: 3-5 minutes
Subsequent runs: 30 seconds (data is cached)

