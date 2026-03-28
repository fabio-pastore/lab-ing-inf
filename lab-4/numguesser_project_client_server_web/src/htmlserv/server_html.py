from fastapi import Form, Request, HTTPException, FastAPI
from fastapi.templating import Jinja2Templates
import requests
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

API_SERVER_BASE_URL: str = "http://127.0.0.1:8000/"
MIN_NUMBER = None
MAX_NUMBER = None
player_username = ''
match_ended = False

app = FastAPI()
templates = Jinja2Templates(directory=os.path.join(current_dir, "..", "..", "templates"))

def reset_globals() -> None:
    global player_username, match_ended
    player_username = ''

def post_data(req_url: str, json_payload: str) -> any:
    try:
        response = requests.post(req_url, json=json_payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print("[HTML-SERVER]: API call error >> " + str(e))
        
    return response.json()

def get_data(req_url: str) -> any:
    try:
        response = requests.get(req_url)
        response.raise_for_status()
    except requests.RequestException as e:
        print("[HTML-SERVER]: API call error >> " + str(e))

    return response.json()

@app.get("/")
def index(request: Request):
    global MIN_NUMBER, MAX_NUMBER
    req_url = API_SERVER_BASE_URL + "/get_bounds"
    data = get_data(req_url) # retrieve input number bounds from API server
    MIN_NUMBER = data.get("low_bound")
    MAX_NUMBER = data.get("high_bound")
    return templates.TemplateResponse(name="index.html", request=request, context={"request": request})

@app.post("/start")
def start(request: Request, player_name: str = Form(...)):
    global player_username, match_ended
    player_username = player_name
    req_url = API_SERVER_BASE_URL + "/start_game"
    player_info_payload = {
        "player_list": [
            {
            "name": player_username
            }
        ]
    }
    post_data(req_url, player_info_payload)
    match_ended = False
    return templates.TemplateResponse(name="game.html", request=request, context={"request": request, "lower": MIN_NUMBER, "higher": MAX_NUMBER})

@app.post("/play")
def play(request: Request, guess: int = Form(...)):
    global match_ended
    client_output = None
    if (match_ended):
        client_output = "The match has already ended. Press the following button if you wish to play again!"
        return templates.TemplateResponse(name="game.html", request=request, context={"request": request, "result": client_output, "lower": MIN_NUMBER, "higher": MAX_NUMBER})
    if not (MIN_NUMBER <= guess <= MAX_NUMBER):
        client_output = f"Please input a number in the interval ({MIN_NUMBER}-{MAX_NUMBER})"
        return templates.TemplateResponse(name="game.html", request=request, context={"request": request, "result": client_output, "lower": MIN_NUMBER, "higher": MAX_NUMBER})
    req_url = API_SERVER_BASE_URL + "/make_guess"
    guess_payload = {
        "player": player_username,
        "guess": str(guess)
    }
    guess_result = post_data(req_url, guess_payload)
    if (guess_result.get("has_won")):
        client_output = "You win!"
        reset_globals() # reset client data
        match_ended = True
        return templates.TemplateResponse(name="game.html", request=request, context={"request": request, "result": client_output, "lower": MIN_NUMBER, "higher": MAX_NUMBER})

    elif (guess_result.get("too_high")):
        client_output = "Your guess was too high! Try again!"
        return templates.TemplateResponse(name="game.html", request=request, context={"request": request, "result": client_output, "lower": MIN_NUMBER, "higher": MAX_NUMBER})
    
    client_output = "Your guess was too low! Try again!"
    return templates.TemplateResponse(name="game.html", request=request, context={"request": request, "result": client_output, "lower": MIN_NUMBER, "higher": MAX_NUMBER})

@app.get("/end")
def end_game(request: Request):
    req_url = API_SERVER_BASE_URL + "/end_game"
    get_data(req_url)
    return index(request) # go back to home page