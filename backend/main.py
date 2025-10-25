from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from schemas import ProblemInput
from ai_processing.physics_parserer import extract_simulation_data

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

@app.post('/process_problem')
def process_problem(problem_input: ProblemInput):
    result = extract_simulation_data(problem_input.problem)

    return {"parameters": result}

@app.get("/")
def root():
    return {"status": "ok", "message": "Visigen backend running."}
