from pydantic import BaseModel, Field

class UserGuessAnalysis(BaseModel):
    is_correct: bool = Field(
        description="True if answer is correct, false otherwise")
    hint: str = Field(
        description="If the answer was incorrect, give the user a hint to solve the riddle")
    is_giving_up : bool = Field(description="True if answer is to give op or new riddle")
    is_asking_for_hint: bool = Field(description="If user ask for help or hint give him a hint")
    answer: str = Field(description="only answer of the riddle")

class Riddle(BaseModel):
    content: str = Field(description="Riddle to solve")
