from typing import Optional
import requests
from utils.commands import Command

def get_command_from_prompt(prompt: str) -> Optional[Command]:
    commands_string = ""

    for command in Command:
        commands_string += f"{command.value}. {command.name} "

    body = {
        "model": "llama3:latest",
        "stream": "false",
        "prompt": f"Answer with only a number. Which of the given commands is the best\
                match to the given prompt? The prompt may not directly reference a command.\
                If none seem to match, resort to web search.\
                Commands: {commands_string} Example prompt: Will it rain today? Matching\
                command: {Command.WEATHER_FORECAST.value}. Example prompt: How many legs\
                do ants have? Matching command: {Command.WEB_SEARCH.value}. Example prompt:\
                Is it cold tomorrow? Matching command: {Command.WEATHER_FORECAST.value}.\
                Example prompt: what's the temperature. Matching command: {Command.WEATHER_CURRENT.value}\
                Example prompt: Nothing really matters. Resort to web search: \
                {Command.WEB_SEARCH.value}. Your turn. Prompt: {prompt}"
    }
    response = requests.get("http://localhost:11434/api/generate", json = body)

    return None
