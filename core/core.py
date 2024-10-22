from typing import Any, Dict, Optional
from flask import Flask, make_response, request, abort
from dotenv import load_dotenv
import datetime
import utils.errorhandler as errorhandler
from utils.commands import Command
import services.weather as weather
import services.perplexica as perplexica
import services.ollama as ollama

load_dotenv()

app = Flask(__name__)

@app.route("/")
def index():
    return "Access the API via /api"

@app.route("/health/")
def health_index():
    return "ok"

@app.route("/api/")
def api_index():
    return "API usage instructions here"

@app.route("/api/services/")
def service_index():
    return "API service usage instructions here"

@app.route("/api/services/perplexica/")
def perplexica_service_index():
    query = request.args.get("q")

    # query is validated on the service side
    status_code, data = perplexica.query_internet(query)

    if errorhandler.check_service_error(data, status_code):
        return errorhandler.get_service_error_response(data, status_code)

    if data is None:
        abort(status_code)

    return data

@app.route("/api/services/weather/")
def weather_service_index():
    city = request.args.get("city", "Helsinki")
    status_code, data = weather.get_current_weather(city)

    if errorhandler.check_service_error(data, status_code):
        return errorhandler.get_service_error_response(data, status_code)

    if data is None:
        abort(status_code)

    return data

@app.route("/api/services/music/")
def music_service_index():
    query = request.args.get("query", "")
    return f"<p>This is the music service. Try spotube?</p><p>You queried: {query}</p>"

@app.route("/api/handle-prompt")
def handle_prompt():
    prompt = request.args.get("p", None)
    print(f"prompt: {prompt}")

    if prompt is None:
        response = make_response({ "error": "Prompt missing" })
        response.status_code = 400
        return response

    command = ollama.get_command_from_prompt(prompt)

    if command is None:
        response = make_response({ "error": "Prompt didn't match a command" })
        response.status_code = 400
        return response

    print(f"command: {command.name} ({command.value})")

    data: Optional[Dict[str, Any]] = None
    status_code: int = 500

    match command:
        case Command.WEATHER_CURRENT:
            print("Handling current weather command...")
            status_code, data = weather.get_current_weather("Helsinki")

            if errorhandler.check_service_error(data, status_code):
                return errorhandler.get_service_error_response(data, status_code)

        case Command.WEATHER_FORECAST:
            print("Handling weather forecast command...")
            status_code, data = weather.get_weather_forecast("Helsinki")

            if errorhandler.check_service_error(data, status_code):
                return errorhandler.get_service_error_response(data, status_code)

        case Command.WEB_SEARCH:
            print("Handling web search command...")

    if data is None:
        abort(status_code)

    #summary_prompt = ("Give a very short summary of the following response data based on a prompt given by the user. "
    #                  "Only summarize data that is relevant to the user prompt. "
    #                  "Assume that the response data is always accurate. "
    #                  "Answer with only the summary itself. "
    #                  "Example user prompt: 'Is it hot today?', Good answer: 'No. The temperature is about "
    #                  "14 Celsius.'. Example user prompt: 'How many legs do ants have?', Good answer: "
    #                  "'Ants have 6 legs.'. "
    #                  f"Your turn. The user said: {prompt}. "
    #                  f"The response data: {data}")

    #summary_prompt = ("A user enters a prompt and expects a short answer fast. "
    #                  "The user might ask something or give a direct command."
    #                  "You must use the given data to answer as concisely as possible. "
    #                  "Assume that the given data is always accurate. Respond only with "
    #                  "the answer itself. Ignore any data that is irrelevant to the user's query. "
    #                  "Start immediately by answering the prompt without hesitation. "
    #                  "Do not reply to me. Only respond to the user prompt. "
    #                  "Example user prompt: 'Is it hot today?'. Example data: { weather: { "
    #                  "avg_temp_c: 15, min_temp_c: 11, max_temp_c: 16, chance_of_rain: 0, cloud_coverage: 35, "
    #                  "sunrise: 7am, sunset: 8pm } }. "
    #                  "You would answer: 'The temperature is about 16 degrees Celsius today.' (ignore the rest of the data like rain, cloud coverage and sun visibility times). "
    #                  "Example user prompt: 'How many legs do ants have?'. Example data: "
    #                  "'**Answer:** Ants, like all insects, have six legs.\n\nAccording to various sources [1][2][3][4], the number of legs in ants is a consistent characteristic among all ant species. Whether an ant is a worker, queen, or drone, it will always have six legs, which are attached to their thorax (the middle section of their body).\n\nThese six legs are articulated, clawed, and sensitive [5][6], allowing ants to move quickly and efficiently, forage, communicate, defend, and build nests.\n\nIn fact, the number of legs in ants is determined by their genetics, just like other insects [7]. So, if you're wondering how many legs an ant has, the answer is always six!\n\nReferences:\n[1] - Context result 1\n[2] - Context result 2\n[3] - Context result 3\n[4] - Context result 4\n[5] - Context result 6\n[6] - Context result 8\n[7] - Context result 5'. "
    #                  "You would answer: 'Ants have six legs.' (be super concise). Your turn. "
    #                  f"User prompt: '{prompt}'. Data: {data}. Answer:")

    summary_prompt = (f"Give a short one sentence answer to the user prompt '{prompt}' "
                      f"based on this data: '{data} Current time: {datetime.datetime.now()}'. "
                      "Answer with one short sentence that includes relevant details that a human might want to know.")

    return ollama.send_prompt(summary_prompt)
