import os
from dotenv import load_dotenv
from twilio_tool import TwilioTool
from openai_tool import (OpenAITool, Riddle, UserGuessAnalysis)

# Laden der Umgebungsvariablen
load_dotenv()

# Twilio-Konfiguration
API_KEY : str = os.getenv("API_KEY_SID")
API_KEY_SECRET: str  = os.getenv("API_KEY_SECRET")
ACC_SID: str  = os.getenv("ACC_SID")
SVC_ID: str  = os.getenv("SVC_ID")
PERSONAL_NUM: str  = os.getenv("PERSONAL_NUM")
MASTERSHOOL_NUM: str  = os.getenv("MASTERSHOOL_NUM")

twilio_client = TwilioTool()
openai_client = OpenAITool()


def display_greeting():
    text = (
    """
    Welcome to the game!
    The rules are simple:
    1. Choose the type of the riddle.
    2. Answer the riddle or ask for "hint".
    3. If the answer is wrong you get a hint.
    4. Enjoy the game and don't forget to invite your friends to compete with them.
    """
    )
    return text


def get_number_and_name():
    number = "whatsapp:",input("Enter your number(+49....): ")
    name = input("Enter your name: ")
    return number, name


def get_riddle_type(conversation, my_number):
    ask_riddle_type = "Choose riddle type (e.g., logic, math, word): "
    twilio_client.create_message(conversation, message=ask_riddle_type)
    riddle_type = twilio_client.get_last_message_from_user(conversation, my_number)
    return riddle_type


def check_answer_and_give_feedback(answer, riddle_data, conversation, my_number):
    if answer == riddle_data["answer"].strip().lower():
        twilio_client.create_message(conversation, "Correct!")
    else:
        response_for_first_wrong_answer =(f"Wrong! Here's a hint: "
                                          f"{riddle_data["hint"]}\nTry again!")

        twilio_client.create_message(conversation=conversation, message=response_for_first_wrong_answer)
        answer = twilio_client.get_last_message_from_user(conversation, my_number)                  #muss den letzten Eintrag vom participant raussuchen

        if answer == riddle_data["answer"].strip().lower():
            twilio_client.create_message(conversation, "Correct!")
        else:
            twilio_client.create_message(conversation,
                                    f"Wrong! The correct answer was: "
                                    f"{riddle_data["answer"]}")


def main():

    #my_number, my_name = get_number_and_name()
    my_number = PERSONAL_NUM
    my_name = "Yusuf"

    conversation = twilio_client.get_conversation(my_number)
    if not conversation:
        conversation = twilio_client.create_conversation(my_name)
        twilio_client.create_participant(conversation, my_number)

    greeting = display_greeting()
    twilio_client.create_message(conversation=conversation, message=greeting)

    continue_game = True
    while continue_game:
        riddle_type = get_riddle_type(conversation, my_number)

        messages = [
            {"role": "system",
             "content": "You are my assistant to help me solve riddle."},
            {"role": "user",
             "content": f"Create a riddle for me to solve with the type {riddle_type}"}
        ]

        riddle_response: Riddle = openai_client.structured_answer(messages=messages, model=Riddle)
        twilio_client.create_message(conversation,riddle_response.content)
        messages.append(
            {"role": "assistant", "content": riddle_response.content})

        while True:
            user_response = "What is the answer of the riddle? "
            twilio_client.create_message(conversation, user_response)
            messages.append({"role": "user", "content": user_response})
            user_guess_analysis: UserGuessAnalysis = openai_client.structured_answer(
                messages, UserGuessAnalysis)
            if user_guess_analysis.is_correct:
                print("You did it!")
                break
            else:
                print(
                    f"Wrong answer, but here you get a hint: "
                    f"{user_guess_analysis.hint}")
                messages.append(
                    {"role": "assistant", "content": user_guess_analysis.hint})

        # riddle_data = OpenAITool.structured_answer()
        # riddle_text = riddle_data["riddle"],"Your answer: "
        # TwilioTool.create_message(conversation, riddle_text)
        # user_answer = TwilioTool.get_last_message_from_user(conversation, my_number)         #muss den letzten Eintrag vom participant raussuchen
        # check_answer_and_give_feedback(user_answer, riddle_data, conversation)
        #
        # ask_to_continue_str ="Do you want another riddle? (yes/no): "
        # TwilioTool.create_message(conversation, ask_to_continue_str)
        #
        # ask_to_continue = TwilioTool.get_last_message_from_user(conversation, my_number)     #muss den letzten Eintrag vom participant raussuchen
        #
        # if ask_to_continue != "yes":
        #     continue_game = False
        #     TwilioTool.create_message(conversation, "See you next time!")


if __name__ == "__main__":
    main()
