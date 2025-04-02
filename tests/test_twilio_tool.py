from twilio_tool import TwilioTool



# Test für das Senden einer WhatsApp-Nachricht
def test_send_whatsapp_message():
    tool = TwilioTool()
    response = tool.send_whatsapp_message("Testnachricht")
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
    conversation = tool.get_conversation()
    assert conversation is not None
    print(conversation)
    assert hasattr(conversation, "sid")
    print(f"Conversation SID: {conversation.sid}")

# Test für das Erstellen eines Teilnehmers
def test_create_participant():
    tool = TwilioTool()
    # Zuerst eine Konversation erstellen
    conversation = tool.create_conversation("part2")
    participant = tool.create_participant(conversation)
    assert participant is not None
    assert hasattr(participant, "sid")
    print(f"Participant SID: {participant.sid}")

# Test für das Erstellen einer Nachricht
def test_create_message():
    tool = TwilioTool()
    # Zuerst eine Konversation erstellen
    conversation = tool.get_conversation()
    message_sid = tool.create_message(conversation, message="Testnachricht")
    print(f"Message SID: {message_sid}")
    assert message_sid is not None
    assert isinstance(message_sid, str)

#Test für das Abrufen der Nachrichten
def test_list_messages():
    tool = TwilioTool()
    conversation = tool.get_conversation()
    messages = tool.get_messages(conversation)
    for message in messages:
        print(f"From: {message.author}, Message: {message.body}")

    assert isinstance(messages, list)

#Test für das Abrufen eines Teilnehmers
def test_get_participant():
    tool = TwilioTool()
    conversation = tool.get_conversation()
    participant = tool.get_participant(conversation)
    assert participant is not None
    assert participant.messaging_binding.get("address") == tool.my_number



def test_last_message_from_user():
    tool = TwilioTool()
    conversation = tool.get_conversation(my_number=PERSONAL_NUM)
    last_message_from_user = tool.get_last_message_from_user(conversation, my_number=PERSONAL_NUM)
    print(last_message_from_user)
    assert isinstance(last_message_from_user, str)
