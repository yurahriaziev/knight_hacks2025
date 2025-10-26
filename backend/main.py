from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ProblemInput
from ai_processing.physics_parserer import extract_simulation_data
from utils.logger import log
from agents.a2a_manager import run_a2a_simulation

app = FastAPI(
    title='Visigen API',
    version='1.0.0'
)

origins = {"http://localhost:5173"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

# @app.post('/process_problem')
# def process_problem(problem_input: ProblemInput):
#     result = extract_simulation_data(problem_input.problem)

#     return {"parameters": result}

@app.post('/simulate')
async def simulate_physics_problem(req: ProblemInput):
    """
    Receives a physics word problem and returns a generated 3D simulation JSON.
    """
    log("SimulationAPI", f"Received simulation request: {req.problem}", "info")

    try:
        result = run_a2a_simulation(req.problem)
        return {
            'status':'success',
            'message':'Simulation generated successfully',
            **result
        }
    except Exception as e:
        log("SimulationAPI", f"Error running simulation: {e}", "error")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def root():
    return {"status": "ok", "message": "Visigen backend running."}
