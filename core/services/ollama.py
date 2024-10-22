from typing import Optional
import requests
from utils.commands import Command

PROMPT_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "llama3:latest"

def send_prompt(prompt: str) -> str:
    body = {
        "model": DEFAULT_MODEL,
        "stream": False,
        "prompt": prompt
    }

    response = requests.post(PROMPT_URL, json = body)
    response_json = response.json()
    return response_json["response"]

def get_command_from_prompt(prompt: str) -> Optional[Command]:
    commands_string = ""

    for command in Command:
        commands_string += f"{command.value}. {command.name} "

    prompt_string = (f"Answer with only a number. Which of the given commands is the best"
                     f"match to the given prompt? The prompt might not directly reference a command."
                     f"If none seem to match, resort to web search."
                     f"Commands: {commands_string} Example prompt: Will it rain today? Matching"
                     f"command: {Command.WEATHER_FORECAST.value}. Example prompt: How many legs"
                     f"do ants have? Matching command: {Command.WEB_SEARCH.value}. Example prompt:"
                     f"Is it cold tomorrow? Matching command: {Command.WEATHER_FORECAST.value}."
                     f"Example prompt: what's the temperature. Matching command: {Command.WEATHER_CURRENT.value}"
                     f"Example prompt: Nothing really matters. Resort to web search: "
                     f"{Command.WEB_SEARCH.value}. Your turn. Prompt: {prompt}")

    command_number_string: str = send_prompt(prompt_string)
    command_number = int(command_number_string.split()[0])

    if command_number == 0 or command_number > len(Command):
        return None
    
    for command in Command:
        if command.value == command_number:
            return command

    return None
