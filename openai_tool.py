from openai import OpenAI
from dotenv import load_dotenv
import os


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
