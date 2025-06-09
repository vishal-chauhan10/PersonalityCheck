from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date, datetime
from numerology import get_personality_analysis
from typing import List, Optional

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # More permissive for development
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserInput(BaseModel):
    full_name: str
    birth_date: str  # Format: DD-MM-YYYY
    responses: Optional[List[dict]] = None

@app.options("/api/analyze")
async def options_analyze():
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:3000",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

@app.post("/api/analyze")
async def analyze_personality(user_input: UserInput):
    try:
        # Parse the date string
        birth_date = datetime.strptime(user_input.birth_date, "%d-%m-%Y").date()
        
        # Get personality analysis
        analysis = await get_personality_analysis(
            name=user_input.full_name,
            birth_date=birth_date,
            life_path=0,  # This will be calculated inside get_personality_analysis
            responses=user_input.responses
        )
        
        return JSONResponse(
            content=analysis,
            headers={
                "Access-Control-Allow-Origin": "http://localhost:3000",
            }
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid date format. Please use DD-MM-YYYY format.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 