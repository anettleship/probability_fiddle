"""FastAPI application for Warhammer 40K attack simulation."""

import sys
from pathlib import Path

# Add parent directory to path to import warhammer module
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal

from warhammer.load_unit_data_from_roster import LoadUnitDataFromRoster
from warhammer.warhammer_actions import MeleeAttack, RangedAttack
from warhammer.warhammer_actions_orchestrators import AttackOrchestrator

app = FastAPI(
    title="Warhammer 40K Probability Calculator API",
    description="API for simulating Warhammer 40K attack outcomes",
    version="1.0.0",
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Paths to test data
TEST_DATA_DIR = Path(__file__).parent.parent / "warhammer" / "test_data"


class SimulationRequest(BaseModel):
    """Request body for attack simulation."""
    attacker_roster: str
    attacker_unit: str
    defender_roster: str
    defender_unit: str
    attack_type: Literal["melee", "ranged"]
    num_simulations: int = 100


class SimulationResponse(BaseModel):
    """Response from attack simulation."""
    summary: dict
    expected_success_rate: dict
    detail: dict


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/rosters")
async def list_rosters():
    """List available roster files."""
    try:
        if not TEST_DATA_DIR.exists():
            return {"rosters": []}
        
        rosters = [f.stem for f in TEST_DATA_DIR.glob("*.json")]
        return {"rosters": sorted(rosters)}
    except Exception as e:
        return {"rosters": [], "error": str(e)}


@app.post("/simulate", response_model=dict)
async def simulate_attack(request: SimulationRequest):
    """
    Simulate an attack between two units.
    
    Parameters:
    - attacker_roster: Name of the JSON file containing the attacker unit
    - attacker_unit: Name of the unit within the attacker roster
    - defender_roster: Name of the JSON file containing the defender unit
    - defender_unit: Name of the unit within the defender roster
    - attack_type: "melee" or "ranged"
    - num_simulations: Number of simulations to run (default: 100)
    
    Returns: Simulation results with summary, probabilities, and details
    """
    try:
        # Load attacker unit
        attacker_path = TEST_DATA_DIR / f"{request.attacker_roster}.json"
        if not attacker_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Attacker roster not found: {request.attacker_roster}",
            )
        
        attacker_loader = LoadUnitDataFromRoster(datasource=attacker_path)
        attacker_unit = attacker_loader.get_unit(request.attacker_unit)
        
        if attacker_unit is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unit not found in attacker roster: {request.attacker_unit}",
            )
        
        # Load defender unit
        defender_path = TEST_DATA_DIR / f"{request.defender_roster}.json"
        if not defender_path.exists():
            raise HTTPException(
                status_code=404,
                detail=f"Defender roster not found: {request.defender_roster}",
            )
        
        defender_loader = LoadUnitDataFromRoster(datasource=defender_path)
        defender_unit = defender_loader.get_unit(request.defender_unit)
        
        if defender_unit is None:
            raise HTTPException(
                status_code=404,
                detail=f"Unit not found in defender roster: {request.defender_unit}",
            )
        
        # Select attack class based on attack type
        attack_class = MeleeAttack if request.attack_type == "melee" else RangedAttack
        
        # Run simulation
        orchestrator = AttackOrchestrator(
            attacker_unit=attacker_unit,
            target_unit=defender_unit,
            num_simulations=request.num_simulations,
            attack_class=attack_class,
        )
        
        result = orchestrator.run()
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation error: {str(e)}",
        )


@app.get("/")
async def root():
    """API documentation redirect."""
    return {
        "message": "Warhammer 40K Probability Calculator API",
        "docs_url": "/docs",
        "endpoints": {
            "health": "GET /health",
            "list_rosters": "GET /rosters",
            "simulate": "POST /simulate",
        },
    }


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "war_application.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
