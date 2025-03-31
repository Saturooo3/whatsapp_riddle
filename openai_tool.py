import openai


class OpenAITool:
    def __init__(self):
        self.client = OpenAI()

    def generate_text(self, prompt):
        response = openai.Completion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
