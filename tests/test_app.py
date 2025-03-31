import pytest
from openai_tool import OpenAITool
from pydantic import BaseModel

def test_openai_tool():
    tool = OpenAITool()
    response = tool.answer("Was ist die Hauptstadt von Deutschland?")
    assert "Berlin" in response
    print(response)
    ### test für structured output with pydantic model

class CountryStats(BaseModel):
    capital_city: str
    population: int


def test_openai_with_structure():
    tool = OpenAITool()
    response = tool.structured_answer("Was ist die Hauptstadt und die Einwohnerzahl von Deutschland?", CountryStats)
    print(response)
