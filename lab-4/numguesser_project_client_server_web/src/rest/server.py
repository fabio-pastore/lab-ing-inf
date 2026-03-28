from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from random import randint

app = FastAPI()

MAX_NUMBER = 10
MIN_NUMBER = 0
game_started: bool = False
players: list[str] = []
curr_player_idx = 0
prev_winning_number = None
generated_number = None

class PlayerModel(BaseModel):
    name: str

class PlayerList(BaseModel):
    player_list: list[PlayerModel]

    @field_validator("player_list")
    @classmethod
    def check_list(cls, value: list[PlayerModel]) -> list[PlayerModel]:
        set_p_names: set[str] = set()
        for p in value:
            if p.name in set_p_names:
                raise ValueError("All player names must be different")
            else:
                set_p_names.add(p.name)
        return value
    
class PlayerGuess(BaseModel):
    player: str
    guess: str # change this to int? 

    @field_validator("guess")
    @classmethod
    def validate_guess(cls, value: str) -> str:
        int_val = None
        try:
            int_val = int(value)
        except ValueError:
            raise ValueError("Provided guess must be a number!")

        if not (MIN_NUMBER <= int_val <= MAX_NUMBER):
            raise ValueError(f"Number must be between {MIN_NUMBER} and {MAX_NUMBER}")

        return value
    
class GameStartConfirmation(BaseModel):
    game_started: bool
    player_order_list: PlayerList # order in which players shall guess in the client

class GuessResult(BaseModel):
    has_won: bool
    too_high: bool

class GameResetConfirmation(BaseModel):
    reset: bool

class WinningNumber(BaseModel):
    number: int

class GameBounds(BaseModel):
    low_bound: int
    high_bound: int

@app.post("/start_game")
def start_game(list: PlayerList) -> GameStartConfirmation:
    global players, game_started, curr_player_idx, generated_number
    players = [p.name for p in list.player_list]
    game_started = True
    curr_player_idx = 0
    generated_number = randint(MIN_NUMBER, MAX_NUMBER)
    return GameStartConfirmation(game_started=True, player_order_list=PlayerList(player_list=[PlayerModel(name=name) for name in players]))

def increment_p_index() -> None:
    global curr_player_idx
    curr_player_idx = (curr_player_idx + 1) % len(players)

@app.post("/make_guess")
def guess_number(guess: PlayerGuess) -> GuessResult:
    global prev_winning_number
    if (not game_started):
        raise HTTPException(status_code=400, detail="Game has not been started yet")
    if not (guess.player in players):
        raise HTTPException(status_code=404, detail=f"Could not find player {guess.player}")
    if (players[curr_player_idx] != guess.player):
        raise HTTPException(status_code=400, detail=f"Unexpected player guess (was expecting guess from player '{players[curr_player_idx]}').")

    player_guess = int(guess.guess)

    if (player_guess == generated_number):
        prev_winning_number = generated_number
        reset_game()
        return GuessResult(has_won=True, too_high=False)
    
    elif (player_guess > generated_number):
        increment_p_index()
        return GuessResult(has_won=False, too_high=True)

    increment_p_index()
    return GuessResult(has_won=False, too_high=False)

def reset_game() -> None:
    global game_started, players, curr_player_idx, generated_number
    game_started = False
    players = []
    curr_player_idx = 0
    generated_number = None

@app.get("/end_game")
def end_game() -> GameResetConfirmation:
    reset_game()
    return GameResetConfirmation(reset=True)

# not actually used in the HTML server (for now)
@app.get("/get_winning_number")
def get_winning_number() -> WinningNumber:
    if not game_started:
        return WinningNumber(number=prev_winning_number)
    raise HTTPException(status_code=400, detail="Unable to retrieve previous game winning number: game has not yet ended!")

@app.get("/get_bounds")
def get_game_bounds() -> GameBounds:
    return GameBounds(low_bound=MIN_NUMBER, high_bound=MAX_NUMBER)
