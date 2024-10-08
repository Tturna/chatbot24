from flask import Flask, make_response, request, abort
from dotenv import load_dotenv
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

@app.route("/api/handle-voiceline")
def handle_voiceline():
    voice_line = request.args.get("v", None)

    if voice_line is None:
        response = make_response("Voice line missing.")
        response.status_code = 400
        return response

    command = ollama.get_command_from_prompt(voice_line)

    if command is None:
        response = make_response("Voice line didn't match a command")
        response.status_code = 400
        return response

    match command:
        case Command.WEATHER_CURRENT:
            pass
        case Command.WEATHER_FORECAST:
            pass
        case Command.WEB_SEARCH:
            pass

    return f"Command: {command.name}"
