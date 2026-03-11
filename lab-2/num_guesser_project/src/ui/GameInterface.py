from player.Player import Player
from random import randint
from datetime import datetime

class GameInterface:

    MAX_NUMBER = 1000000000000
    MIN_NUMBER = 0

    def __init__(self, players: list[Player]):
        if all(isinstance(p, Player) for p in players):
            self.players = players
        else:
            pass

    def save_data(self, player_data: dict[Player, list[int]], generated_num: int, date_time: str):
        """
        This function saves information relative to a round. It is called every time a round ends. (i.e. player names, date and time, correct number, player guesses, etc.)

        The data is stored in "results.tsv". We simply open the file in append ('a') mode and save all the required data.

        Args:
            player_data (dict[Player, list[int]]): a dictionary containing each player who participated in the round and their guesses
            generated_num (int): an integer containing the winning number for the round
            date_time (str): a string containing information about the date and time at which the round was played

        Returns:
            This function does not return any value.
        """
        with open("results.tsv", "a", encoding="UTF-8") as fout:
            fout.write(str(generated_num) + "\t")
            for item in player_data:
                fout.write(item.name + "\t")
                fout.write(str(len(player_data[item])) + "\t")
                fout.write(str(player_data[item]) + "\t")
            fout.write(date_time + "\n")

    def start_game(self, debug: bool, iterations: int) -> None: # debug = True skips next round confirmation and plays "iterations" rounds in a row
        cnt = 0
        while (True):
            print("I'm thinking about a number " + "(" + str(self.MIN_NUMBER) + "-" + str(self.MAX_NUMBER) + "). Can you guess it?")
            random_num = randint(self.MIN_NUMBER, self.MAX_NUMBER) # generate number to guess
            correct_guess = False
            player_data = {p:[] for p in self.players}

            while not correct_guess:
                for p in self.players:
                    guess_out = p.guess()
                    player_data[p].append(guess_out) # append guessed number
                    print(p.name + " guessed: " + str(guess_out))
                    if guess_out == random_num:
                        correct_guess = True
                        print(p.name + " won the game!")
                        break
                    else:
                        p.update_guess(guess_out, guess_out < random_num) # call guess update logic for each player (if applicable)
            
            print("The correct number was: " + str(random_num) + "!")

            curr_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.save_data(player_data, random_num, curr_datetime) # save data for elapsed round

            cnt += 1
            if debug and cnt == iterations:
                print("Benchmark completed successfully.")
                print("Exiting process with status code (0)")
                break

            ok_input = False
            play_again = False

            if debug:
                ok_input = True
                play_again = True

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


