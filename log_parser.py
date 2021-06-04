import json
import re
from typing import Union
from game_control import GameControl


class LogParser:
    def __init__(self) -> None:
        self.game_control = GameControl()

    def parse_log(self, log_file: str) -> dict:
        """
        Opens and make decisions based on lines contents. Can start and end a match
        or send bigger chunck of info to be parsed elsewhere

        :param log_file: the file to be parsed
        :return: dict - containing all games info
        """
        with open(log_file, "r") as file:
            for line in file:
                if "InitGame" in line:
                    self.game_control.start_game()
                elif "ShutdownGame" in line:
                    self.game_control.finish_game()
                elif "ClientUserinfoChanged" in line:
                    parsed_join = self.parse_join_line(line)
                    self.game_control.add_player(parsed_join)
                elif "killed" in line:
                    parsed_kill = self.parse_kill_line(line)
                    self.game_control.add_kill(parsed_kill[0], parsed_kill[1])
        return self.game_control.games_list

    @staticmethod
    def parse_kill_line(line: str) -> tuple:
        """
        If it's a kill line, parse it to get the killer and the victim

        :param line: string received with the entire line to be parsed
        :return: tuple - (killer, victim)
        """
        try:
            pattern = re.compile(r"""
                                 ^\s{1,2}\d*:\d*\s\w{4}:    # " 20:54 Kill:" 
                                 \s\d*\s\d*\s\d*:\s         # " 1022 2 22:"
                                 (?P<player_from>.*?)       # Player From  
                                 \s\w{6}\s                  # " killed "
                                 (?P<player_to>.*?)         # Player To
                                 \s\w*\s\w*$                # " by ..." 
                                 """, re.VERBOSE)

            match = pattern.match(line)
            return match.group("player_from"), match.group("player_to")
        except AttributeError:
            return None, None

    @staticmethod
    def parse_join_line(line: str) -> Union[str, None]:
        """
        If it's a join line, parse it to get the player name who joined the match

        :param line: string received with the entire line to be parsed
        :return: the player name found
        """
        try:
            pattern = re.compile(r"""
                                 ^\s*\d*:\d*\s      # " 13:37 "
                                 \w{21}             # "ClientUserinfoChanged"    
                                 :\s*               # ": "               
                                 \d*\s*\w\\         # "2 n\" 
                                 (?P<player>.*?)    # Player name  
                                 \\t.*$             # Rest of the string
                                 """, re.VERBOSE)
            match = pattern.match(line)
            return match.group("player")
        except AttributeError:
            return None


if __name__ == "__main__":
    log_parser = LogParser()
    result = log_parser.parse_log("challenge/games.log")
    print(json.dumps(result))
