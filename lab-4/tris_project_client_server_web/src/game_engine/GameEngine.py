from player.Player import Player
from ui.AsciiUI import AsciiUI
from board.Board import Board
from time import sleep
import requests
from requests import Response

class GameEngine():

    WAIT_INTERVAL_SECONDS: float = 0.25
    DEBUG = True
    API_SERVER_BASE_URL = "http://127.0.0.1:8000"

    def __init__(self, p1: Player, p2: Player): # check if players have the same name (avoid this)
        if (p1 is p2):
            raise Exception("[GameEngine] Player one and player two must be different!")
        if (p1.name == p2.name):
            raise Exception("[GameEngine] Player one and player two mustn't have the same names!")
        self.player_one: Player = p1
        self.player_two: Player = p2

    def validate_aux(self, recv_data) -> None | dict:
        data: None | dict = None
        if recv_data.status_code == 200:
            content_type = recv_data.headers.get("Content-Type", "")

            if "application/json" in content_type:
                try:
                    data: dict = recv_data.json()
                except (ValueError, requests.exceptions.JSONDecodeError):
                    print("[GameEngine]: response does not contain a valid JSON!")
                
            else:
                print("[GameEngine]: response is not JSON")
                print("Content-Type: " + str(content_type))
        
        else:
            if type(recv_data.json().get("detail")) is list:
                print("[GameEngine]: [HTTP_ERROR] > " + str(recv_data.status_code) + ": " + str(recv_data.json().get("detail")[0].get("msg")))
            else:
                print("[GameEngine]: [HTTP_ERROR] > " + str(recv_data.status_code) + ": " + str(recv_data.json().get("detail")))

        return data

    def get_validated_data(self, url) -> None | dict:
        response: Response = requests.get(url) 
        return self.validate_aux(response)

    def post_data(self, url, payload) -> None | dict:
        response: Response = requests.post(url, json=payload) 
        return self.validate_aux(response)
    
    def find_player(self, name: str) -> Player:
        if self.player_one.name == name: return self.player_one
        else: return self.player_two
    
    def check_game_ended(self, server_data: dict) -> tuple[bool, Player | None]:
        if (server_data.get("game_ended")):
            if (server_data.get("player_win")):
                return (True, self.find_player(server_data.get("winner").get("name")))
            else:
                return (True, None)
        else:
            return (False, None)

    def send_reset_request(self) -> bool:
        req_url = self.API_SERVER_BASE_URL + "/reset"
        response = self.get_validated_data(req_url)
        if response is None:
            print("[GameEngine]: unsuccessful (reset) request to API server")
            return False
        
        if (GameEngine.DEBUG): print("[GameEngine]: successfully reset game state on API server")
        return True

    def start_game(self) -> None:
        """
        Starts and manages the main game loop.

        This method orchestrates the flow of the game, alternating turns between 
        the two players, triggering the UI to update the board visualization, 
        and checking for win or draw conditions after every move until the 
        match concludes.

        Args:
            None.

        Returns:
            None.
        """ 
        print("[GameEngine] Welcome to TRIS v-1.1 by Fabio!")
        print()

        if not (self.send_reset_request()): return

        while True:

            req_url = self.API_SERVER_BASE_URL + "/start"
            game_start_payload = {
                "players": [
                    {
                        "name": self.player_one.name
                    },
                    {
                        "name": self.player_two.name
                    }
                ]
            }

            response_data = self.post_data(req_url, payload=game_start_payload)
            if response_data is None:
                print("[GameEngine]: unsuccessful request to API server")
                break

            if (GameEngine.DEBUG): print("[GameEngine]: succesfully received data from server")

            if not (response_data.get("ok")):
                print("[GameEngine]: API server could not start the game successfully.")
                break
            
            first_player_name: str = response_data.get("first_to_play").get("name")
            if (first_player_name == self.player_one.name):
                pass

            else:
                tmp_p: Player
                tmp_p = self.player_two
                self.player_two = self.player_one
                self.player_one = tmp_p

            player_one_id: int = response_data.get("player_one_symbol")
            player_two_id: int = response_data.get("player_two_symbol")
            is_first_move: bool = True
            game_ended: bool = False

            while not game_ended:

                if is_first_move:
                    AsciiUI.display_data(board_data=Board().get_board_data())
                    is_first_move = False

                req_url = GameEngine.API_SERVER_BASE_URL + "/get_board"
                response_data = self.get_validated_data(req_url)

                if response_data is None:
                    print("[GameEngine]: unsuccessful request to API server")
                    return

                if (GameEngine.DEBUG): print("[GameEngine]: successfully retrieved game board data from API server")
                
                curr_board: list[list[int]] = response_data.get("data")

                tmp_board: Board = Board() # shadow board so that players may invoke the make_move() method on it 
                tmp_board.set_board(curr_board)

                move_data = self.player_one.make_move(game_board=tmp_board, player_id=player_one_id)
                req_url = GameEngine.API_SERVER_BASE_URL + "/make_move"
                move_payload = {
                    "player": {
                        "name": self.player_one.name
                    },
                    "move_data": [
                        move_data[0],
                        move_data[1]
                    ]
                }
                response_data = self.post_data(req_url, payload=move_payload)
                if response_data is None:
                    print("[GameEngine]: unsuccessful request to API server")
                    return
                
                if (GameEngine.DEBUG): print("[GameEngine]: successfully sent player (1) move data to API server")

                AsciiUI.display_data(board_data=tmp_board.get_board_data())

                game_state_info: tuple[bool, Player | None] = self.check_game_ended(response_data)
                if (game_state_info[0]):
                    if (game_state_info[1] is None):
                        print("[GameEngine]: match ended in a draw.")
                    else:
                        print(f"[GameEngine]: player '{game_state_info[1].name}' won the game!")

                    break # exit inner loop

                sleep(GameEngine.WAIT_INTERVAL_SECONDS)
                # second player's turn

                move_data = self.player_two.make_move(game_board=tmp_board, player_id=player_two_id)
                req_url = GameEngine.API_SERVER_BASE_URL + "/make_move"
                move_payload = {
                    "player": {
                        "name": self.player_two.name
                    },
                    "move_data": [
                        move_data[0],
                        move_data[1]
                    ]
                }
                response_data = self.post_data(req_url, payload=move_payload)
                if response_data is None:
                    print("[GameEngine]: unsuccessful request to API server")
                    return
                
                if (GameEngine.DEBUG): print("[GameEngine]: successfully sent player (2) move data to API server")

                AsciiUI.display_data(board_data=tmp_board.get_board_data())

                game_state_info: tuple[bool, Player | None] = self.check_game_ended(response_data)
                if (game_state_info[0]):
                    if (game_state_info[1] is None):
                        print("[GameEngine]: match ended in a draw.")
                    else:
                        print(f"[GameEngine]: player '{game_state_info[1].name}' won the game!")

                    break # exit inner loop
            
            # outer loop
            input_ok: bool = False
            u_choice: str = ""

            while not input_ok:
                print("[GameEngine] Do you want to play again? Y/N")
                u_choice = input("$ tris >> ").lower()
                if (u_choice == 'y' or u_choice == 'n'):
                    input_ok = True
                else:
                    print("[GameEngine] Invalid input. Please try again.")

            if u_choice == 'y':
                print("[GameEngine] Starting new match...")
                print()
                if not (self.send_reset_request()): return
                continue

            else:
                print("[GameEngine] Shutting down...")
                if not (self.send_reset_request()): return # to prevent any future crashes on initialization due to corrupt API server state
                break