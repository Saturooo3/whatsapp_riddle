import pytest
from twilio_tool import TwilioTool
from dotenv import load_dotenv
import os
"""
# Lade die .env-Datei, um die Umgebungsvariablen zu laden
load_dotenv()

# Beispielhafte Testdaten
PERSONAL_NUM = os.getenv('PERSONAL_NUM')
MASTERSHOOL_NUM = os.getenv('MASTERSHOOL_NUM')
SERVICE_SID = os.getenv('SERVICE_SID')

# Test für das Senden einer WhatsApp-Nachricht
def test_send_whatsapp_message():
    tool = TwilioTool(SERVICE_SID)
    response = tool.send_whatsapp_message(PERSONAL_NUM, "Testnachricht")
    assert response is not None
    assert isinstance(response, str)
    print(f"Message SID: {response}")

# Test für das Erstellen einer Konversation
def test_create_conversation():
    tool = TwilioTool(SERVICE_SID)
    conversation = tool.create_conversation("name")
    assert conversation is not None, "Es wurde keine Konversation gefunden"

# Test für das Abrufen einer Konversation
def test_get_my_conversation():
    tool = TwilioTool(SERVICE_SID)
    conversation = tool.get_conversation(PERSONAL_NUM)
    assert conversation is not None
    assert hasattr(conversation, "sid")
    print(f"Conversation SID: {conversation.sid}")

# Test für das Erstellen eines Teilnehmers
def test_create_participant():
    tool = TwilioTool(SERVICE_SID)
    # Zuerst eine Konversation erstellen
    conversation = tool.create_conversation("2test_partisipance")
    participant = tool.create_participant(conversation, PERSONAL_NUM)
    assert participant is not None
    assert hasattr(participant, "sid")
    print(f"Participant SID: {participant.sid}")

# Test für das Erstellen einer Nachricht
def test_create_message():
    tool = TwilioTool(SERVICE_SID)
    # Zuerst eine Konversation erstellen
    conversation = tool.create_conversation("3test_partisipance")
    message_sid = tool.create_message(conversation, "Testnachricht")
    print(f"Message SID: {message_sid}")
    assert message_sid is not None
    assert isinstance(message_sid, str)"""



