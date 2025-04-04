from twilio_tool import TwilioTool
from openai_tool import OpenAITool
from whatsapp_riddle_executers import (Riddle, UserGuessAnalysis)
from rich import console
import json
import Ascii

twilio_client = TwilioTool()
openai_client = OpenAITool()

console = console.Console()

def display_greeting():
    text = Ascii.print_ascii_greeting()
    return text


def get_number_and_name():
    number = "whatsapp:",input("Enter your number(+49....): ")
    name = input("Enter your name: ")
    return number, name


def get_riddle_type(conversation):
    ask_riddle_type = Ascii.print_choose_riddle()
    twilio_client.create_message(conversation, message=ask_riddle_type)
    riddle_type = twilio_client.get_last_message_from_user(conversation)
    return riddle_type


def check_answer_and_give_feedback(conversation, messages):
    while True:
        new_message = twilio_client.get_last_message_from_user(conversation)
        messages.append({"role": "user", "content": new_message})
        user_guess_analysis: UserGuessAnalysis = openai_client.structured_answer(
            messages, UserGuessAnalysis)

        if user_guess_analysis.is_correct:
            twilio_client.create_message(conversation, Ascii.print_win())
            break
        elif user_guess_analysis.is_giving_up:
            twilio_client.create_message(conversation, Ascii.print_give_up(user_guess_analysis))
            break
        elif user_guess_analysis.is_asking_for_hint:
            twilio_client.create_message(conversation, user_guess_analysis.hint)
        else:
            respond_wrong_answer = Ascii.print_hint(user_guess_analysis)

            twilio_client.create_message(conversation, respond_wrong_answer)

            messages.append(
                {"role": "assistant", "content": user_guess_analysis.hint})

def load_or_create_conversation():
    conversation = twilio_client.get_conversation()
    if not conversation:
        console.print("No conversation found, creating new one",
                      style="bold blue")
        conversation = twilio_client.create_conversation()
        twilio_client.create_participant(conversation)
        console.print("Created new conversation and participant",
                      style="bold blue")

    return conversation

def initialize_messages(riddle_type, asked_riddles):
    initialization_message = (f"Create a new riddle for me, that is not in the list "
                              f"{asked_riddles}. It should be riddle from type {riddle_type}")
    messages = [
            {"role": "system",
             "content": "You are my assistant to give me riddles to solve, and give me hints, when I'm stuck."},
            {"role": "user",
             "content": initialization_message }
        ]

    return messages

def read_asked_riddles_from_json():
    try:
        with open("asked_riddles.json", "r") as f:
            data = json.loads(f.read())
        return data
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_asked_riddles_to_json(asked_riddles):
    with open("asked_riddles.json", "w") as f:
        f.write(json.dumps(asked_riddles))


def main():
    console.print("Starting game!", style="bold green")

    console.print(f"Getting conversation for {twilio_client.my_number}", style="bold blue")
    conversation = load_or_create_conversation()
    console.print("Got conversation from twilio", style="bold blue")

    greeting = display_greeting()
    twilio_client.create_message(conversation=conversation, message=greeting)
    console.print("Displayed greeting", style="bold blue")

    continue_game = True
    console.print("Entering main loop", style="bold blue")
    while continue_game:
        riddle_type = get_riddle_type(conversation)

        asked_riddles : list = read_asked_riddles_from_json()
        messages = initialize_messages(riddle_type, asked_riddles)

        riddle_response: Riddle = openai_client.structured_answer(messages=messages, model=Riddle)
        twilio_client.create_message(conversation, riddle_response.content)
        console.print(f"Riddle send to player", style="bold blue")
        asked_riddles.append(riddle_response.content)
        write_asked_riddles_to_json(asked_riddles)

        messages.append({"role": "assistant", "content": riddle_response.content})

        check_answer_and_give_feedback(conversation, messages)
        console.print(f"Answer checked", style="bold blue")

if __name__ == "__main__":
    main()
