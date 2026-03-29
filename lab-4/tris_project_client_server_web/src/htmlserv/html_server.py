from fastapi import Form, Request, HTTPException, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from player.CpuPlayer import CpuPlayer
from player.CpuPlayerGood import CpuPlayerGood
from ui.AsciiUI import AsciiUI
from board.Board import Board
import requests
import os

current_dir = os.path.dirname(os.path.realpath(__file__))

API_SERVER_BASE_URL: str = "http://127.0.0.1:8000"
DEBUG: bool = True # set to True for debug messages
p_name: str | None = None
cpu_p : CpuPlayer | None = None
first_to_play: str | None = None
p_1_s: str | None = None # player symbols
p_cpu_s : str | None = None 
is_player_turn: bool = True
game_ended: bool = False

app = FastAPI()
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "..", "..", "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(current_dir, "..", "..", "templates"))

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

def get_shadow_board() -> Board:
    req_url = API_SERVER_BASE_URL + "/get_board"
    b_data = get_data(req_url)
    b_matrix: list[list[int]] = b_data.get("data")
    shadow_board: Board = Board()
    shadow_board.set_board(b_matrix)
    return shadow_board

def request_reset():
    req_url = API_SERVER_BASE_URL + "/reset"
    response = get_data(req_url)
    if not (response.get("reset_ok")):
        raise HTTPException(status_code=503, detail="API server could not successfully reset game status")
    
def reset_vars():
    global p_name, first_to_play, p_1_s, p_cpu_s, is_player_turn, game_ended, cpu_p
    p_name = None
    first_to_play = None
    p_1_s = None
    p_cpu_s = None
    is_player_turn = True
    game_ended = False
    cpu_p = None
    CpuPlayer.reset_id_counter()

def send_move_data(coords: tuple[int, int] | None, cpu_move: bool) -> dict:
    req_url = API_SERVER_BASE_URL + "/make_move"
    if (cpu_move): 
        tmp_b: Board = get_shadow_board()
        coords: tuple[int, int] = cpu_p.make_move(tmp_b, p_cpu_s)

    move_d_payload = {
        "player": {
            "name": cpu_p.name if (cpu_move) else p_name
        },
        "move_data": [
            coords[0],
            coords[1]
        ]
    }
    ret = post_data(req_url, json_payload=move_d_payload)
    return ret

def get_context_dict() -> dict:
    tmp : Board = get_shadow_board()
    b_data: list[list[int]] = tmp.get_board_data()
    out: dict = {}
    for i in range(Board.NUM_BOARD_RC):
        for j in range (Board.NUM_BOARD_RC):
            out['c' + str(i) + str(j)] = AsciiUI.PLAYER_ONE_CHAR if (b_data[i][j] == Board.PLAYER_ONE_VAL) \
                else (AsciiUI.PLAYER_TWO_CHAR if (b_data[i][j] == Board.PLAYER_TWO_VAL) else '')
    return out

@app.get("/")
def index(request: Request):
    return templates.TemplateResponse(name="index.html", request=request, context={"request": request})

@app.post("/play") # switch to post later
def play(request: Request, player: str = Form(...), hard_mode: bool = Form(False)):
    global p_name, cpu_p, first_to_play, p_1_s, p_cpu_s, game_ended, is_player_turn
    request_reset() # reset game status on API server in case of previous crashes
    p_name = player
    is_player_turn = True
    game_ended = False
    if (cpu_p is None):
        if (hard_mode):
            cpu_p = CpuPlayerGood()
        else:
            cpu_p = CpuPlayer()
    req_url = API_SERVER_BASE_URL + "/start"
    game_start_payload = {
        "players": [
            {
                "name": p_name
            },
            {
                "name": cpu_p.name
            }
        ]
    }
    data = post_data(req_url, json_payload=game_start_payload) # send start req to API server
    if not (data.get("ok")): raise HTTPException(status_code=503, detail="API server could not start the game")
    first_to_play = data.get("first_to_play")
    p_1_s = data.get("player_one_symbol")
    p_cpu_s = data.get("player_two_symbol")

    complete_context = {"request": request}

    if (first_to_play.get("name") == cpu_p.name):
        send_move_data(None, cpu_move=True)

    curr_turn: str = "It's your turn!"
    complete_context.update({"turn": curr_turn})
    complete_context.update(get_context_dict())
    if (DEBUG): print("[DEBUG]\n" + str(complete_context))

    return templates.TemplateResponse(name="tris.html", request=request, context=complete_context)

@app.post("/mark_board")
def mark(request: Request, row: int = Form(...), col: int = Form(...)):
    global is_player_turn, game_ended
    if (game_ended): raise HTTPException(status_code=400, detail="Game has already ended!")
    data = None
    curr_turn : str = ''

    if (is_player_turn):
        data = send_move_data((row, col), False) # player move
        is_player_turn = False
        curr_turn = "It's the computer's turn!"
    else:
        data = send_move_data(None, True) # CPU move
        is_player_turn = True
        curr_turn = "It's your turn!"

    complete_context = {"request": request} # default context content
    complete_context.update(get_context_dict())
    move_result_out: str = ''

    if (data.get("game_ended")):
        game_ended = True
        curr_turn = ''
        if (data.get("player_win")):
            winner_name: str = data.get("winner").get("name")
            move_result_out = f"{winner_name} has won the match!"
        else:
            move_result_out = "The match ended in a draw!"
        reset_vars()

    complete_context.update({"result": move_result_out, "turn": curr_turn}) 
    if (DEBUG): print("[DEBUG]\n" + str(complete_context))

    return templates.TemplateResponse(name='tris.html', request=request, context=complete_context)

@app.get("/reset")
def reset(request: Request):
    if (game_ended):
        reset_vars()
        request_reset()