import pytest
from openai_tool import OpenAITool
from pydantic import BaseModel

def test_openai_tool():
    tool = OpenAITool()
    response = tool.send_prompt("Was ist die Hauptstadt von Deutschland?")
    assert "Berlin" in response
    print(response)


class CountryStats(BaseModel):
    capital_city: str
    population: int


def test_openai_with_structure():
    tool = OpenAITool()
    messages=[
        {"role": "system", "content": "Was ist die Hauptstadt und die Einwohnerzahl von Deutschland?"}]

    response = tool.structured_answer(messages, CountryStats)
    print(response)


def test_openai_with_history():
    tool = OpenAITool()
    messages = [
        {"role": "system", "content": "Was ist die Hauptstadt von Deutschland?"},
        {"role": "user", "content": "Was ist die Hauptstadt und die Einwohnerzahl von Deutschland?"}
    ]

    response = tool.structured_answer(messages, CountryStats)
    print(response)





