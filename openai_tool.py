from openai import OpenAI
from dotenv import load_dotenv

class OpenAITool:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def answer(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
