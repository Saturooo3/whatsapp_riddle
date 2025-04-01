from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

class OpenAITool:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def send_prompt(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content


    def get_structured_answer(self, riddle_type, riddle_difficulty, messages, model) -> dict:
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages= messages,         #messages muss eine Liste werden
            response_format=model,
        )

        return completion.choices[0].message.parsed
