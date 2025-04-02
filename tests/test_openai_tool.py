import pytest
from openai_tool import OpenAITool
from pydantic import BaseModel, Field

def test_openai_tool():
    tool = OpenAITool()
    response = tool.send_prompt("Was ist die Hauptstadt von Deutschland?")
    assert "Berlin" in response
    print(response)


class CountryStats(BaseModel):
    capital_city: str
    population: int
    def dump(self)->str:
        return f"Capital city is {self.capital_city}, population is {self.population}"



def test_openai_with_structure():
    tool = OpenAITool()
    messages=[
        {"role": "system", "content": "Was ist die Hauptstadt und die Einwohnerzahl von Deutschland?"}]

    response = tool.structured_answer(messages, CountryStats)
    print(response)

class PopulationStats(BaseModel):
    average_age: float = Field(description="The average age of the people in the city")
    languages_spoken: list[str] = Field(description="The languages spoken in the city, ordered by most speakers")
    def dump(self)->str:
        return f"Average age is {self.average_age}, languages spoken are {', '.join(self.languages_spoken)}"


def test_openai_with_history():
    # Run with: uv run pytest -k test_openai_with_history --capture no
    tool = OpenAITool()
    messages = [
        {"role": "system", "content": "Du bist ein hilfreicher Assistant der mir strukturierte Antworten auf Geographie und Landesstatistiken gibt."},
        {"role": "user", "content": "Was ist die Hauptstadt und die Einwohnerzahl von Deutschland?"}
    ]

    first_response : CountryStats = tool.structured_answer(messages, CountryStats)
    print(first_response.dump())
    messages.append({"role": "assistant", "content": first_response.dump()})
    messages.append({"role" : "user", "content": "What is the average age of people in the city, and what are the most spoken languages?"})

    second_response : PopulationStats = tool.structured_answer(messages, PopulationStats)
    print(second_response.dump())
    messages.append({"role": "assistant", "content": second_response.dump()})

    print(f"Messages were: {'\n'.join([str(message) for message in messages])}")
