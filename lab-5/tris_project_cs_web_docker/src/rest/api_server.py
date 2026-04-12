from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from board.Board import Board
from ui.AsciiUI import AsciiUI
import random

class Player(BaseModel):
    name: str

class PlayerList(BaseModel):
    players: list[Player] # add not same name check and other field validations

    @field_validator("players")
    @classmethod
    def validate_list(cls, value: list[Player]) -> list[Player]:
        if not (len(value) == 2):
            raise ValueError("Two players are required to play!")
        if (value[0].name == value[1].name):
            raise ValueError("Players must have different names!")
        return value

class GameStartConfirmation(BaseModel):
    ok: bool
    first_to_play: Player
    player_one_symbol: int
    player_two_symbol: int

class MoveInfo(BaseModel):
    player: Player
    move_data: tuple[int, int]

class MoveResult(BaseModel):
    game_ended: bool
    player_win: bool
    winner: Player | None

class BoardInfo(BaseModel):
    data: list[list[int]]

class GameResetConfirmation(BaseModel):
    reset_ok: bool

NUM_PLAYERS: int = 2
DEBUG: bool = True
players: list[tuple[Player, int]] = []
next_turn: Player | None = None
game_board: Board | None = None
ui: AsciiUI | None = None
game_started: bool = False

app = FastAPI()

def get_names() -> list[str]:
    out = []
    for p in players:
        out.append(p[0].name)
    return out

def find_other_player(p: Player) -> Player | None: # NOTE: this will never return None
    for pair in players:
        if pair[0].name != p.name:
            return pair[0]
    return None

def modify_player_turn() -> None:
    global next_turn
    next_turn = find_other_player(next_turn)

def reset() -> None: # resets server game data
    global players, next_turn, game_board, game_started
    players = []
    next_turn = None
    game_started = False
    if not game_board is None:
        game_board.reset()

def find_winner(player_symbol: int) -> Player | None: # NOTE: this will never return None if the present implementation is not modified 
    for pair in players:
        if (pair[1] == player_symbol):
            return pair[0] # return Player
    return None

def get_player_symbol(curr_player: Player) -> int | None: # NOTE: this will never return None
    for pair in players:
        if pair[0].name == curr_player.name:
            return pair[1]
    return None

@app.post("/start")
def start_game(player_list: PlayerList) -> GameStartConfirmation:
    global next_turn, game_board, ui, players, game_started
    if not (game_started):
        reset()
    if (game_started):
        raise HTTPException(status_code=400, detail="Game currently in progress.")
    rnd: int = random.randint(0, 1)
    rnd_symbol: int = random.randint(0, 1)
    symbol_list: list[int] = [Board.PLAYER_ONE_VAL, Board.PLAYER_TWO_VAL]
    players = [(player_list.players[0], symbol_list[rnd_symbol]), (player_list.players[1], symbol_list[1] if rnd_symbol == 0 else symbol_list[0])]
    next_turn = players[rnd][0]
    game_board = Board()
    ui = AsciiUI(board=game_board) 
    game_started = True
    return GameStartConfirmation(ok=True, first_to_play=players[rnd][0], player_one_symbol=players[rnd][1], player_two_symbol=(players[0][1] if (rnd == 1) else players[1][1])) # get first element of pair which is the Player

@app.post("/make_move")
def mark_board(move: MoveInfo) -> MoveResult:
    global game_started

    if not (game_started):
        raise HTTPException(status_code=400, detail="No game is currently being played.")
    if not (move.player.name in get_names()):
        raise HTTPException(status_code=404, detail="Specified player not found.")
    if not (move.player.name == next_turn.name):
        raise HTTPException(status_code=400, detail=f"Was not expecting move from player '{move.player.name}'.")

    row: int = move.move_data[0]
    col: int = move.move_data[1]

    try:
        if (game_board.is_written(row, col)):
            raise HTTPException(status_code=400, detail=f"Cell at coordinates {row, col} already written.")
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    game_board.write_value(row, col, get_player_symbol(curr_player=next_turn)) # NOTE: next_turn is still the player making the move, since it has not been updated yet

    winner_id: int = game_board.check_win()
    has_won_player: bool = False if (winner_id == -1) else True
    game_ended: bool = game_board.is_full() or has_won_player
    winner = None if (not has_won_player) else find_winner(player_symbol=winner_id)

    if (DEBUG):
        print("[DEBUG]:")
        ui.display_board()

    modify_player_turn()

    if (game_ended):
       game_started = False 

    return MoveResult(game_ended=game_ended, player_win=has_won_player, winner=winner)

@app.get("/get_board")
def get_board_data() -> BoardInfo:
    if game_board is None:
        raise HTTPException(status_code=404, detail="Board not yet initialized")
    return BoardInfo(data=game_board.get_board_data())

@app.get("/reset")
def reset_game() -> GameResetConfirmation:
    reset()
    return GameResetConfirmation(reset_ok=True)