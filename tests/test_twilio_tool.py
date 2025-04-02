import pytest
from twilio_tool import TwilioTool
from dotenv import load_dotenv
import os


# Lade die .env-Datei, um die Umgebungsvariablen zu laden
load_dotenv()

# Beispielhafte Testdaten
API_KEY : str = os.getenv("API_KEY")
API_KEY_SECRET: str  = os.getenv("API_KEY_SECRET")
ACC_SID: str  = os.getenv("ACC_SID")
SVC_ID: str  = os.getenv("SVC_ID")
PERSONAL_NUM: str  = os.getenv("PERSONAL_NUM")
MASTERSHOOL_NUM: str  = os.getenv("MASTERSHOOL_NUM")

# Test für das Senden einer WhatsApp-Nachricht
def test_send_whatsapp_message():
    tool = TwilioTool()
    response = tool.send_whatsapp_message(PERSONAL_NUM, "Testnachricht")
    print(f"Message SID: {response}")
    assert response is not None
    assert isinstance(response, str)

# Test für das Erstellen einer Konversation
def test_create_conversation():
    tool = TwilioTool()
    conversation = tool.create_conversation("Yusuf")
    assert conversation is not None, "Es wurde keine Konversation gefunden"

# Test für das Abrufen einer Konversation
def test_get_my_conversation():
    tool = TwilioTool()
    conversation = tool.get_conversation(PERSONAL_NUM)
    assert conversation is not None
    print(conversation)
    assert hasattr(conversation, "sid")
    print(f"Conversation SID: {conversation.sid}")

# Test für das Erstellen eines Teilnehmers
def test_create_participant():
    tool = TwilioTool()
    # Zuerst eine Konversation erstellen
    conversation = tool.create_conversation("part2")
    participant = tool.create_participant(conversation, PERSONAL_NUM)
    assert participant is not None
    assert hasattr(participant, "sid")
    print(f"Participant SID: {participant.sid}")

# Test für das Erstellen einer Nachricht
def test_create_message():
    tool = TwilioTool()
    # Zuerst eine Konversation erstellen
    conversation = tool.get_conversation(PERSONAL_NUM)
    message_sid = tool.create_message(conversation, message="Testnachricht")
    print(f"Message SID: {message_sid}")
    assert message_sid is not None
    assert isinstance(message_sid, str)

#Test für das Abrufen der Nachrichten
def test_list_messages():
    tool = TwilioTool()
    conversation = tool.get_conversation(my_number=PERSONAL_NUM)
    messages = tool.get_messages(conversation)
    for message in messages:
        print(f"From: {message.author}, Message: {message.body}")

    assert isinstance(messages, list)

#Test für das Abrufen eines Teilnehmers
def test_get_participant():
    tool = TwilioTool()
    conversation = tool.get_conversation(my_number=PERSONAL_NUM)
    participant = tool.get_participant(conversation, PERSONAL_NUM)
    assert participant is not None
    assert participant.messaging_binding.get("address") == PERSONAL_NUM



def test_last_message_from_user():
    tool = TwilioTool()
    conversation = tool.get_conversation(my_number=PERSONAL_NUM)
    last_message_from_user = tool.get_last_message_from_user(conversation)
    print(last_message_from_user)
    assert isinstance(last_message_from_user, str)
