from pydantic import BaseModel, Field

class ProblemInput(BaseModel):
    problem: str = Field(..., min_length=5, max_length=1000, description='User provided word problem text')