import pytest
from openai_tool import OpenAITool
from twilio_tool import TwilioTool

def test_openai_tool():
    tool = OpenAITool()
    response = tool.answer("Was ist die Hauptstadt von Deutschland?")
    assert "Berlin" in response
    print(response)