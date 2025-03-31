from twilio.rest import Client
import os
from dotenv import load_dotenv
from twilio_tool import TwilioTool
from openai_tool import OpenAITool
from twilio.rest import Client

# Laden der Umgebungsvariablen
load_dotenv()

# Twilio-Konfiguration
ACC_SID = os.getenv("ACCOUNT_SID")
API_KEY = os.getenv("API_KEY_SID")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
SVC_ID = os.getenv("SERVICE_SID")
MASTERSHOOL_NUM = dotenv.load_dotenv("MASTERSHOOL_NUMBER")
PERSONAL_NUM = dotenv.load_dotenv("PERSONAL_NUMBER")


api_key = API_KEY
api_secret = API_KEY_SECRET
account_sid = ACC_SID
twilio_client = Client(api_key, api_secret, account_sid)
service = twilio_client.conversations.v1.services(SVC_ID)
openai_client = OpenAI()

# Initialisierung des Twilio-Clients
twilio_client = Client(API_KEY, API_KEY_SECRET, ACC_SID)




def main():

    conversation = get_my_conversation() or create_conversation()
    participant = create_participant(conversation)
    create_message(conversation, "zweiter Test")

    print("Rätselspiel gestartet!")

    twilio_tool = TwilioTool(twilio_client, SVC_ID)
    openai_tool = OpenAITool(os.getenv("OPENAI_API_KEY"))

    prompt = "Erstelle ein kurzes, spannendes Rätsel."
    raetsel = openai_tool.generate_text(prompt)
    if not raetsel:
        raetsel = "Notfall-Rätsel: Was wird nasser je mehr es trocknet? Ein Handtuch!"
    print("Rätsel:", raetsel)

    recipient = input("Gib deine WhatsApp-Nummer ein (+49...): ")
    message_id = twilio_tool.send_whatsapp_message(recipient, rätsel)
    print("Nachricht gesendet, ID:", message_id)


if __name__ == "__main__":
    main()

