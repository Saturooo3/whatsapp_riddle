import sys
import os

# Füge das übergeordnete Verzeichnis (das Verzeichnis, das main.py enthält) zum Python-Pfad hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Jetzt kannst du das main-Modul importieren
from main import main as app_main

import pytest
from unittest.mock import Mock, patch
from openai_tool import OpenAITool
from twilio_tool import TwilioTool

# ---------- Fixtures ----------
@pytest.fixture
def mock_openai():
    """Mock für die OpenAI API"""
    with patch('openai.OpenAI') as mock:
        mock.return_value.chat.completions.create.return_value = Mock(
            choices=[Mock(message=Mock(content="Test-Rätsel"))]
        )
        yield mock


@pytest.fixture
def mock_twilio():
    """Mock für die Twilio API"""
    with patch('twilio.rest.Client') as mock:
        mock.return_value.messages.create.return_value = Mock(sid="SM123")
        yield mock


# ---------- OpenAI Tests ----------
def test_openai_generation(mock_openai):
    """Testet die Rätselgenerierung mit OpenAI"""
    # Setup
    tool = OpenAITool("dummy-key")
    mock_openai.return_value.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content="Warum ist die Banane krumm?"))]
    )

    # Ausführung
    result = tool.generate_text("Rätsel")

    # Assertions
    assert "Banan" in result
    mock_openai.return_value.chat.completions.create.assert_called_once()


# ---------- Twilio Tests ----------
def test_twilio_message_sending(mock_twilio):
    """Testet den WhatsApp-Versand"""
    # Setup
    tool = TwilioTool(Mock(), "dummy-sid")

    # Ausführung
    result = tool.send_whatsapp_message("+491234567", "Test")

    # Assertions
    assert result == "SM123"
    mock_twilio.return_value.messages.create.assert_called_once_with(
        from_="whatsapp:+14155238886",
        body="Test",
        to="whatsapp:+491234567"
    )


def test_phone_number_formatting(mock_twilio):
    """Testet die automatische Nummernformatierung"""
    tool = TwilioTool(Mock(), "dummy-sid")
    tool.send_whatsapp_message("491234567", "Test")

    _, kwargs = mock_twilio.return_value.messages.create.call_args
    assert kwargs['to'] == "whatsapp:+491234567"


# ---------- Integrationstests ----------
def test_full_workflow(mock_openai, mock_twilio):
    """Testet den kompletten Ablauf der App"""
    with patch('builtins.input', return_value="+491234567"), \
            patch('builtins.print') as mock_print:
        app_main()

    # Überprüfe API-Aufrufe
    mock_openai.return_value.chat.completions.create.assert_called_once()
    mock_twilio.return_value.messages.create.assert_called_once()

    # Überprüfe Konsolenausgabe
    output = "\n".join(str(call) for call in mock_print.call_args_list)
    assert "Test-Rätsel" in output
    assert "SM123" in output


# ---------- Fehlertests ----------
def test_openai_error():
    """Testet Fehler bei OpenAI"""
    with patch.object(OpenAITool, 'generate_text', side_effect=Exception("API Error")):
        tool = OpenAITool("dummy-key")
        result = tool.generate_text("")
        assert result is None


def test_twilio_error():
    """Testet Fehler bei Twilio"""
    with patch.object(TwilioTool, 'send_whatsapp_message', return_value=None):
        tool = TwilioTool(Mock(), "dummy-sid")
        result = tool.send_whatsapp_message("invalid", "")
        assert result is None