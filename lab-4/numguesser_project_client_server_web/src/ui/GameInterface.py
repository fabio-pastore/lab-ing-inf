from player.Player import Player
import requests

class GameInterface:

    SERVER_BASE_URL: str = "http://127.0.0.1:8000/"
    MIN_NUMBER = None
    MAX_NUMBER = None

    def __init__(self, players: list[Player]):
        if all(isinstance(p, Player) for p in players):
            self.players = players
        else:
            raise ValueError("All players must be instances of class 'Player'")

    def validate_aux(self, recv_data) -> None | dict:
        data: None | dict = None
        if recv_data.status_code == 200:
            content_type = recv_data.headers.get("Content-Type", "")

            if "application/json" in content_type:
                try:
                    data: dict = recv_data.json()
                except (ValueError, requests.exceptions.JSONDecodeError):
                    print("$ num-guesser: response does not contain a valid JSON!")
                
            else:
                print("$ num-guesser : response is not JSON")
                print("Content-Type: " + str(content_type))
        
        else:
            if type(recv_data.json().get("detail")) is list: # aggiungi fix anche all'ex 1)
                print("$ num-guesser: [HTTP_ERROR] > " + str(recv_data.status_code) + ": " + str(recv_data.json().get("detail")[0].get("msg")))
            else:
                print("$ num-guesser: [HTTP_ERROR] > " + str(recv_data.status_code) + ": " + str(recv_data.json().get("detail")))

        return data
    
    def find_player(self, name: str) -> None | Player:
        for p in self.players:
            if p.name == name:
                return p
        return None

    def get_validated_data(self, url) -> None | dict:
        response: requests.Response = requests.get(url) 
        return self.validate_aux(response)

    def post_data(self, url, payload) -> None | dict:
        response: requests.Response = requests.post(url, json=payload) 
        return self.validate_aux(response)

    def start_game(self) -> None:

        req_url = self.SERVER_BASE_URL + "/get_bounds"
        response_data = self.get_validated_data(req_url)

        if response_data is None:
                print("$ num-guesser: could not fetch game bounds from server")
                return

        GameInterface.MIN_NUMBER = response_data.get("low_bound")
        GameInterface.MAX_NUMBER = response_data.get("high_bound")

        for player in self.players:
            player.update_bounds(GameInterface.MAX_NUMBER, GameInterface.MIN_NUMBER)

        while (True):
            correct_guess = False
            req_url = self.SERVER_BASE_URL + "/start_game"
            game_start_payload: str = {"player_list" : [{"name": p.name} for p in self.players]}
            # print(game_start_payload)
            response_data: None | dict = self.post_data(req_url, game_start_payload)
            
            if response_data is None:
                print("$ num-guesser: /game_start POST failed")
                break

            if not (response_data.get("game_started")):
                print("$ num-guesser: server was unable to start the game")
                break
            
            name_order: list[dict] = response_data.get("player_order_list").get("player_list")
            player_order = []
            for player in name_order:
                player_order.append(self.find_player(player.get("name")))
            
            print("I'm thinking about a number " + "(" + str(GameInterface.MIN_NUMBER) + "-" + str(GameInterface.MAX_NUMBER) + "). Can you guess it?")

            while not correct_guess:
                for p in self.players:
                    player_guess = p.guess()
                    print(p.name + " guessed: " + str(player_guess))
                    req_url = self.SERVER_BASE_URL + "/make_guess"

                    guess_payload = {
                        "player" : p.name,
                        "guess" : str(player_guess)
                        }

                    response_data = self.post_data(req_url, guess_payload)

                    if response_data is None:
                        print("$ num-guesser: /make_guess failed!")
                        return

                    if response_data.get("has_won"):
                        correct_guess = True
                        print(p.name + " won the game!")
                        break
                    else:
                        was_guess_low = not(response_data.get("too_high"))
                        p.update_guess(player_guess, was_prev_guess_low=was_guess_low) # call guess update logic for each player (if applicable)

            req_url = self.SERVER_BASE_URL + "/get_winning_number" 
            response_data = self.get_validated_data(req_url)

            if response_data is None:
                print("$ num-guesser: /get_winning_number failed!")
                break

            print("The correct number was: " + str(response_data.get("number")) + "!")

            ok_input = False
            play_again = False

            while not ok_input:
                print("Do you want to play again? Y/N")
                user_choice = input("$ num-guesser ")
                if user_choice.strip().lower() == 'y':
                    play_again = True
                    ok_input = True
                elif user_choice.strip().lower() == 'n':
                    ok_input = True
                else:
                    print("Invalid input. Please try again.")
                    print()
                    continue

            if play_again:
                for p in self.players:
                    p.reset()
                continue

            else:
                print("Exiting process with status code (0)")
                break