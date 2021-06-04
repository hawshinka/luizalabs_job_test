import json
import re
import hashlib
from typing import Union
from game_control import GameControl


class LogParser:
    def __init__(self) -> None:
        self.game_control = GameControl()

    def parse_log(self, log_file: str) -> dict:
        """
        Opens and make decisions based on lines contents. Can start and end a match
        or send bigger chunck of info to be parsed elsewhere

        :param log_file: str (the file to be parsed)
        :return: dict (containing all games info)
        """
        hash = self.get_file_hash(log_file)
        cache = self.check_cache(hash)
        if cache:
            return cache

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

        output = self.game_control.games_list
        return self.save_cache(hash, output)

    @staticmethod
    def get_file_hash(file: str) -> str:  # pragma: no cover
        """
        Returns the SHA1 hash of a given file
        :param file: str (filename to hash)
        :return: str (SHA1 hash)
        """
        buf_size = 65536
        sha1 = hashlib.sha1()
        with open(file, "rb") as file:
            while True:
                data = file.read(buf_size)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()

    @staticmethod
    def check_cache(hash: str) -> Union[str, None]:  # pragma: no cover
        """
        Check if there's a cache for a given hash
        :param hash: str (SHA1 hash)
        :return: str|None (file's content or None)
        """
        try:
            with open(f"cache/{hash}") as cache_file:
                return json.load(cache_file)
        except FileNotFoundError:
            return

    @staticmethod
    def save_cache(hash: str, content: str) -> str:  # pragma: no cover
        """
        Save cache to a file with hashe's name
        :param hash: str (SHA1 hash)
        :param content: str (file content)
        :return: str (file content)
        """
        with open(f"cache/{hash}", "w+") as cache_file:
            json.dump(content, cache_file)
        return content

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
