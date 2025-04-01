from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("API_KEY_SID")
api_secret = os.getenv("API_KEY_SECRET")
account_sid = os.getenv("ACCOUNT_SID")
SERVICE_SID = os.getenv("SERVICE_SID")
PERSONAL_NUM = os.getenv("PERSONAL_NUM")
MASTERSHOOL_NUM = os.getenv("MASTERSHOOL_NUM")

class TwilioTool:
    def __init__(self, service_sid: str):
        self.client = Client(api_key, api_secret, account_sid)
        self.service = self.client.conversations.v1.services(service_sid)



    def create_conversation(self, name):
        """
        gets name for conversation and creates a new conversation"
        """
        name_str = f"Chat with {name}"
        conversation = self.service.conversations.create(friendly_name=name_str)
        return conversation


    def create_participant(self, conversation, my_number):
        """
        gets a conversation and adds participant to the conversation
        """
        participant = (
            self.service.conversations(conversation.sid)
                .participants.create(
                messaging_binding_address=my_number,
                messaging_binding_proxy_address=MASTERSHOOL_NUM
            )
        )
        return participant


    def get_participant(self, conversation, my_number):
        """
        gets a number and returns participant if already exists,
        returns None if not
        """
        participants = (self.service.conversations(conversation.sid)
                        .participants.list())
        for participant in participants:
            if participant.messaging_binding.address == my_number:
                return participant
        return None


    def get_conversation(self, my_number):
        """
        gets number and returns conversation if exists, if not returns None
        """
        for conversation in self.service.conversations.list():
            for participant in conversation.participants.list():
                if participant.messaging_binding["address"] == my_number:
                    return conversation

        return None


    def create_message(self, conversation, message: str):
        """
        gets conversation and message as string and sends message to conversation
        """
        message=self.service.conversations(conversation.sid).messages.create(
            author=MASTERSHOOL_NUM,
            body=message
        )
        return message.sid

    def send_whatsapp_message(self, to_whatsapp: str, body: str) -> str:
        from_whatsapp = MASTERSHOOL_NUM
        if not to_whatsapp.startswith("whatsapp:"):
            to_whatsapp = "whatsapp:" + to_whatsapp
        message = self.client.messages.create(
            from_=from_whatsapp,
            body=body,
            to=to_whatsapp
        )

        return message.sid
