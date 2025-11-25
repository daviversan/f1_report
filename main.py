"""F1 Report System - FastAPI Application

Cloud Run service for F1 race report generation with memory storage.
"""

import os
import json
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any
from contextlib import asynccontextmanager

import pandas as pd
import fastf1
import vertexai
import nest_asyncio
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from vertexai.generative_models import GenerativeModel
from google.adk.memory import VertexAiMemoryBankService


# Configuration
PROJECT_ID = os.getenv('GCP_PROJECT_ID', 'gen-lang-client-0467867580')
LOCATION = os.getenv('GCP_LOCATION', 'us-central1')
MODEL_NAME = 'gemini-2.5-flash'

# Global variables
agent_engine_id = None
memory = None
agent1 = None
agent2 = None


# F1 Calendar
F1_2025_CALENDAR = {
    1: {"name": "Bahrain Grand Prix", "circuit": "Bahrain International Circuit"},
    2: {"name": "Saudi Arabian Grand Prix", "circuit": "Jeddah Corniche Circuit"},
    3: {"name": "Australian Grand Prix", "circuit": "Albert Park Circuit"},
    4: {"name": "Japanese Grand Prix", "circuit": "Suzuka International Racing Course"},
    5: {"name": "Chinese Grand Prix", "circuit": "Shanghai International Circuit"},
    6: {"name": "Miami Grand Prix", "circuit": "Miami International Autodrome"},
    7: {"name": "Emilia Romagna Grand Prix", "circuit": "Autodromo Enzo e Dino Ferrari"},
    8: {"name": "Monaco Grand Prix", "circuit": "Circuit de Monaco"},
    9: {"name": "Spanish Grand Prix", "circuit": "Circuit de Barcelona-Catalunya"},
    10: {"name": "Canadian Grand Prix", "circuit": "Circuit Gilles Villeneuve"},
    11: {"name": "Austrian Grand Prix", "circuit": "Red Bull Ring"},
    12: {"name": "British Grand Prix", "circuit": "Silverstone Circuit"},
    13: {"name": "Belgian Grand Prix", "circuit": "Circuit de Spa-Francorchamps"},
    14: {"name": "Hungarian Grand Prix", "circuit": "Hungaroring"},
    15: {"name": "Dutch Grand Prix", "circuit": "Circuit Zandvoort"},
    16: {"name": "Italian Grand Prix", "circuit": "Autodromo Nazionale di Monza"},
    17: {"name": "Azerbaijan Grand Prix", "circuit": "Baku City Circuit"},
    18: {"name": "Singapore Grand Prix", "circuit": "Marina Bay Street Circuit"},
    19: {"name": "United States Grand Prix", "circuit": "Circuit of the Americas"},
    20: {"name": "Mexico City Grand Prix", "circuit": "Autódromo Hermanos Rodríguez"},
    21: {"name": "São Paulo Grand Prix", "circuit": "Autódromo José Carlos Pace"},
    22: {"name": "Las Vegas Grand Prix", "circuit": "Las Vegas Street Circuit"},
    23: {"name": "Qatar Grand Prix", "circuit": "Lusail International Circuit"},
    24: {"name": "Abu Dhabi Grand Prix", "circuit": "Yas Marina Circuit"}
}


# Memory Service
class MemoryService:
    """Persistent storage for race reports using Vertex AI Memory Bank."""
    
    def __init__(self, project: str, location: str, agent_engine_id: str, backup_file: str = "f1_reports_backup.json"):
        self._service = VertexAiMemoryBankService(
            project=project,
            location=location,
            agent_engine_id=agent_engine_id
        )
        self._cache = {}
        self._backup_file = backup_file
        self._load_from_backup()
    
    def _load_from_backup(self):
        """Load reports from local JSON backup."""
        try:
            if os.path.exists(self._backup_file):
                with open(self._backup_file, 'r', encoding='utf-8') as f:
                    self._cache = json.load(f)
        except Exception:
            pass
    
    def _save_to_backup(self):
        """Save reports to local JSON backup."""
        try:
            with open(self._backup_file, 'w', encoding='utf-8') as f:
                json.dump(self._cache, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def add_session_to_memory(self, race_id: str, report_data: Dict[str, Any]) -> None:
        """Store a race report."""
        timestamp = datetime.now().isoformat()
        entry = {"data": report_data, "timestamp": timestamp}
        self._cache[race_id] = entry
        self._save_to_backup()
        
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(self._async_add_session(race_id, entry))
            else:
                loop.run_until_complete(self._async_add_session(race_id, entry))
        except Exception:
            pass
    
    async def _async_add_session(self, race_id: str, entry: Dict[str, Any]):
        """Async helper to add session to Memory Bank."""
        from google.adk.sessions import Session
        session = Session(
            session_id=race_id,
            user_id="f1_report_system",
            metadata=entry
        )
        await self._service.add_session_to_memory(session)
    
    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        """Search stored reports."""
        results = []
        query_lower = query.lower()
        
        for race_id, entry in self._cache.items():
            gp_name = entry['data'].get('race_data', {}).get('gp_info', {}).get('name', '')
            if query_lower in race_id.lower() or query_lower in gp_name.lower():
                results.append({
                    "race_id": race_id,
                    "gp_name": gp_name,
                    "timestamp": entry['timestamp']
                })
        return results
    
    def get_report(self, race_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve specific report."""
        return self._cache.get(race_id)
    
    def list_all(self) -> List[Dict[str, Any]]:
        """List all stored reports."""
        return [{
            "race_id": race_id,
            "gp_name": entry['data'].get('race_data', {}).get('gp_info', {}).get('name', 'Unknown'),
            "timestamp": entry['timestamp']
        } for race_id, entry in self._cache.items()]


# Data Collection Agent
class DataCollectionAgent:
    """Validates input and collects F1 race data."""
    
    def __init__(self, calendar: Dict[int, Dict[str, str]], year: int = 2025):
        self.calendar = calendar
        self.year = year
    
    def validate_input(self, user_input: str) -> Optional[int]:
        """Validate and convert user input to round number."""
        user_input = user_input.strip()
        
        try:
            round_num = int(user_input)
            return round_num if round_num in self.calendar else None
        except ValueError:
            pass
        
        user_lower = user_input.lower()
        for round_num, info in self.calendar.items():
            if user_lower in info['name'].lower():
                return round_num
        return None
    
    def collect_race_data(self, round_num: int, year: Optional[int] = None) -> Optional[Dict[str, Any]]:
        """Collect comprehensive race data."""
        if year is None:
            year = self.year
            
        try:
            event = fastf1.get_event(year, round_num)
            session = fastf1.get_session(year, round_num, "R")
            session.load()
            
            results = session.results
            drivers_results = []
            
            for idx, row in results.iterrows():
                position = None
                try:
                    if pd.notna(row.get('Position')) and str(row.get('Position', '')).strip():
                        position = int(row['Position'])
                except (ValueError, TypeError):
                    pass
                
                if position is None:
                    try:
                        if pd.notna(row.get('ClassifiedPosition')) and str(row.get('ClassifiedPosition', '')).strip():
                            position = int(row['ClassifiedPosition'])
                    except (ValueError, TypeError):
                        pass
                
                if position is None and 'Status' in row and str(row['Status']) == 'Finished':
                    position = len([d for d in drivers_results if d['position'] is not None]) + 1
                
                grid_pos = None
                try:
                    if pd.notna(row['GridPosition']) and str(row['GridPosition']).strip():
                        grid_pos = int(row['GridPosition'])
                except (ValueError, TypeError):
                    pass
                
                drivers_results.append({
                    "position": position,
                    "full_name": str(row['FullName']) if pd.notna(row['FullName']) else None,
                    "team": str(row['TeamName']) if pd.notna(row['TeamName']) else None,
                    "grid_position": grid_pos,
                    "time": str(row['Time']) if pd.notna(row['Time']) else None,
                    "points": float(row['Points']) if pd.notna(row['Points']) else 0.0,
                })
            
            if all(r['position'] is None for r in drivers_results):
                for idx, driver in enumerate(drivers_results):
                    driver['position'] = idx + 1
            
            podium = sorted([r for r in drivers_results if r['position'] in [1, 2, 3]], key=lambda x: x['position'])
            
            race_data = {
                "race_id": f"{year}_R{round_num}",
                "year": year,
                "round": round_num,
                "gp_info": {
                    "name": event.EventName,
                    "country": event.Country,
                    "circuit": self.calendar[round_num]['circuit'],
                },
                "podium": podium,
                "final_results": [r for r in drivers_results if r['position'] is not None]
            }
            
            return race_data
            
        except Exception:
            if year >= 2024 and year == self.year:
                return self.collect_race_data(round_num, year=year-1)
            return None
    
    def run(self, user_input: str) -> Optional[Dict[str, Any]]:
        """Main execution."""
        round_num = self.validate_input(user_input)
        if not round_num:
            return None
        return self.collect_race_data(round_num)


# Report Generation Agent
class ReportGenerationAgent:
    """Generates social media reports from race data."""
    
    def __init__(self, model_name: str = 'gemini-2.5-flash'):
        self.model = GenerativeModel(model_name)
    
    def generate_report(self, race_data: Dict[str, Any]) -> Optional[str]:
        """Generate social media post."""
        try:
            gp_info = race_data['gp_info']
            podium = race_data['podium']
            
            if len(podium) < 3:
                return None
            
            prompt = f"""Create an Instagram post for this F1 race:

RACE: {gp_info['name']} ({race_data['year']})
CIRCUIT: {gp_info['circuit']}

PODIUM:
1st: {podium[0]['full_name']} ({podium[0]['team']}) - Started P{podium[0]['grid_position']}
2nd: {podium[1]['full_name']} ({podium[1]['team']}) - Started P{podium[1]['grid_position']}
3rd: {podium[2]['full_name']} ({podium[2]['team']}) - Started P{podium[2]['grid_position']}

Write an engaging 200-250 word post that tells the race story and highlights the key moments. Don't generate images, just text."""

            response = self.model.generate_content(
                prompt,
                generation_config={"max_output_tokens": 2048, "temperature": 0.5}
            )
            
            return response.text.strip()
            
        except Exception:
            return None
    
    def run(self, race_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Main execution."""
        if not race_data:
            return None
        
        social_media_post = self.generate_report(race_data)
        if not social_media_post:
            return None
        
        return {
            "race_id": race_data['race_id'],
            "race_data": race_data,
            "social_media_post": social_media_post,
            "timestamp": datetime.now().isoformat()
        }


# Pydantic Models
class AnalyzeRequest(BaseModel):
    race_input: str


class AnalyzeResponse(BaseModel):
    race_id: str
    gp_name: str
    social_media_post: str
    timestamp: str


class HistoryItem(BaseModel):
    race_id: str
    gp_name: str
    timestamp: str


class SearchRequest(BaseModel):
    query: str


# Lifecycle Management
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize services on startup."""
    global agent_engine_id, memory, agent1, agent2
    
    # Initialize Vertex AI
    vertexai.init(project=PROJECT_ID, location=LOCATION)
    nest_asyncio.apply()
    fastf1.Cache.enable_cache('f1_cache')
    
    # Initialize Agent Engine
    client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
    agent_engines = list(client.agent_engines.list())
    if agent_engines:
        agent_engine = agent_engines[0]
    else:
        agent_engine = client.agent_engines.create()
    
    agent_engine_id = agent_engine.api_resource.name.split("/")[-1]
    
    # Initialize services
    memory = MemoryService(PROJECT_ID, LOCATION, agent_engine_id)
    agent1 = DataCollectionAgent(F1_2025_CALENDAR)
    agent2 = ReportGenerationAgent(MODEL_NAME)
    
    yield


# FastAPI Application
app = FastAPI(
    title="F1 Report System",
    description="Generate F1 race reports with memory storage",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "healthy", "service": "F1 Report System"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_race(request: AnalyzeRequest):
    """Generate report for specified race."""
    race_data = agent1.run(request.race_input)
    if not race_data:
        raise HTTPException(status_code=400, detail="Invalid race input or data unavailable")
    
    full_report = agent2.run(race_data)
    if not full_report:
        raise HTTPException(status_code=500, detail="Failed to generate report")
    
    memory.add_session_to_memory(full_report['race_id'], full_report)
    
    return AnalyzeResponse(
        race_id=full_report['race_id'],
        gp_name=race_data['gp_info']['name'],
        social_media_post=full_report['social_media_post'],
        timestamp=full_report['timestamp']
    )


@app.get("/history", response_model=List[HistoryItem])
async def get_history():
    """List all stored reports."""
    reports = memory.list_all()
    return [HistoryItem(**r) for r in reports]


@app.post("/search", response_model=List[HistoryItem])
async def search_reports(request: SearchRequest):
    """Search stored reports."""
    results = memory.search_memory(request.query)
    return [HistoryItem(**r) for r in results]


@app.get("/report/{race_id}")
async def get_report(race_id: str):
    """Retrieve specific report."""
    report = memory.get_report(race_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

