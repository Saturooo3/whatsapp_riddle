from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os

class UserGuessAnalysis(BaseModel):
    is_correct: bool = Field(
        description="True if answer is correct, false otherwise")
    hint: str = Field(
        description="If the answer was incorrect, give the use a hin to solve the riddle")

class Riddle(BaseModel):
    content: str = Field(description="Riddle to solve")


class OpenAITool:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)

    def send_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


    def structured_answer(self, messages, model):
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages= messages,
            response_format=model,
        )

        return completion.choices[0].message.parsed
