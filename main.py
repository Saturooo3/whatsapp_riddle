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

def display_greeting():
    text = (
    """
    Welcome to the game!
    The rules are simple:
    1. Choose the type and the difficulty of the riddle.
    2. Answer the riddle or ask for "hint".
    3. If the answer is wrong you get a hint.
    4. Enjoy the game and don't forget to invite your friends to compete with them.
    """
    )
    print(text)


def get_number_and_name():
    number = input("Enter your number: ")
    name = input("Enter your name: ")
    return number, name


def get_all_participants():
    pass


def main():
    display_greeting()
    my_number, my_name = get_number()
    my_number = PERSONAL_NUM                                                            #delete after tests
    conversation = get_my_conversation(my_number) or create_conversation()
    participant = get_participant(conversation) or create_participant(conversation)

    while True:
        send_input_to_chatgpt(prompt)
        structured_answer = get_structured_answer()
        send_riddle_to_user()
        answer = get_answer_from_user()
        check_if_answer_is_correct(answer)
        if answer == structured_answer["answer"]:
            give_user_positive_feedback()
        else:
            give_user_hint()




if __name__ == "__main__":
    main()

    # print("Rätselspiel gestartet!")
    #
    # twilio_tool = TwilioTool(twilio_client, SVC_ID)
    # openai_tool = OpenAITool(os.getenv("OPENAI_API_KEY"))
    #
    # prompt = "Erstelle ein kurzes, spannendes Rätsel."
    # raetsel = openai_tool.generate_text(prompt)
    # if not raetsel:
    #     raetsel = "Notfall-Rätsel: Was wird nasser je mehr es trocknet? Ein Handtuch!"
    # print("Rätsel:", raetsel)
    #
    # recipient = input("Gib deine WhatsApp-Nummer ein (+49...): ")
    # message_id = twilio_tool.send_whatsapp_message(recipient, rätsel)
    # print("Nachricht gesendet, ID:", message_id)