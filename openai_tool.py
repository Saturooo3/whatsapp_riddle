from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

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


    def structured_answer(self, prompt, model):
        completion = self.client.beta.chat.completions.parse(
            model="gpt-4o-mini",
            messages=[
#                {"role": "system", "content": "Extract the event information."},
                {"role": "user",
                 "content": prompt},
            ],
            response_format=model,
        )

        return completion.choices[0].message.parsed
