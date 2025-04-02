from pydantic import BaseModel, Field

class UserGuessAnalysis(BaseModel):
    is_correct: bool = Field(
        description="True if answer is correct, false otherwise")
    hint: str = Field(
        description="If the answer was incorrect, give the user a hint to solve the riddle")

class Riddle(BaseModel):
    content: str = Field(description="Riddle to solve")
