from twilio.rest import Client
from dotenv import load_dotenv
import os
from time import sleep

from rich import console


console = console.Console()
class TwilioTool:
    def __init__(self):
        load_dotenv()

        self.account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        assert self.account_sid is not None, "TWILIO_ACCOUNT_SID is not set"
        self.api_key = os.getenv("TWILIO_API_KEY_SID")
        assert self.api_key is not None, "TWILIO_API_KEY_SID is not set"
        self.api_key_secret = os.getenv("TWILIO_API_KEY_SECRET")
        assert self.api_key_secret is not None, "TWILIO_API_KEY_SECRET is not set"
        self.service_sid = os.getenv("TWILIO_SERVICE_SID")
        assert self.service_sid is not None, "TWILIO_SERVICE_SID is not set"
        self.twilio_number = os.getenv("TWILIO_MASTERSCHOOL_NUM")
        assert self.twilio_number is not None, "TWILIO_MASTERSCHOOL_NUM is not set"
        self.my_number = os.getenv("MY_NUM")
        assert self.my_number is not None, "MY_NUM is not set"

        self.client = Client(self.api_key, self.api_key_secret, self.account_sid)
        self.service = self.client.conversations.v1.services(self.service_sid)



    def create_conversation(self, name):
        """
        gets name for conversation and creates a new conversation
        """
        name_str = f"Chat with {name}"
        conversation = self.service.conversations.create(friendly_name=name_str)
        return conversation


    def create_participant(self, conversation):
        """
        gets a conversation and adds participant to the conversation
        """
        console.print(f"Creating participants for conversation {conversation.sid}, my number {self.my_number}, twilio number {self.twilio_number}", style="bold blue")
        participant = (
                conversation
                .participants.create(
                    messaging_binding_address=self.my_number,
                    messaging_binding_proxy_address=self.twilio_number
            )
        )
        return participant


    def get_participant(self, conversation):
        """
        gets a number and returns participant if already exists,
        returns None if not
        """
        participants = (self.service.conversations(conversation.sid)
                        .participants.list())
        for participant in participants:
            if participant.messaging_binding.get("address") == self.my_number:
                return participant
        return None


    def get_conversation(self):
        """
        gets number and returns conversation if exists, if not returns None
        """
        for conversation in self.service.conversations.list():
            console.print(f"Checking conversation {conversation.sid}", style="bold blue")
            for participant in conversation.participants.list():
                console.print(f"Checking participant {participant.sid}", style="bold blue")
                if participant.messaging_binding is None:
                    continue
                if participant.messaging_binding.get("address") == self.my_number:
                    return conversation
        console.print(f"No conversation found for {self.my_number}", style="bold red")
        return None


    def create_message(self, conversation, message: str):
        """
        gets conversation and message as string and sends message to conversation
        """
        message=self.service.conversations(conversation.sid).messages.create(
            author=self.twilio_number,
            body=message
        )
        return message.sid

    def send_whatsapp_message(self, to_whatsapp: str, body: str) -> str:
        if not to_whatsapp.startswith("whatsapp:"):
            to_whatsapp = "whatsapp:" + to_whatsapp
        message = self.client.messages.create(
            from_=self.twilio_number,
            body=body,
            to=to_whatsapp
        )

        return message.sid

    def get_messages(self, conversation):

        messages = (
        self.service.conversations(conversation.sid).messages.list()
        )
        return messages


    def get_last_message_from_user(self, conversation):
        while True:
            messages = self.get_messages(conversation)
            if not messages:
                sleep(1)
                continue
            last_message = messages[-1]
            if last_message.author != self.my_number:
                sleep(1)
                continue
            else:
                return last_message.body
