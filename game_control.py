class GameControl:
    def __init__(self) -> None:
        self.started = False
        self.finished = True
        self.game_count = 0
        self.games_list = {}

    @property
    def game_index(self):
        return f"game_{self.game_count}"

    def start_game(self) -> None:
        """
        Starts a new match and its definitions to a list

        :return:
        """
        if self.started and not self.finished:
            self.finish_game()

        self.started = True
        self.finished = False

        self.game_count += 1
        self.games_list[self.game_index] = {
            "total_kills": 0,
            "players": [],
            "kills": {}
        }

        return

    def finish_game(self) -> bool:
        """
        Finishes a game and remove it's duplicated players from players list

        :return: bool - whether the game was finished or not
        """
        if not self.started and self.finished:
            return

        self.started = False
        self.finished = True

        players_list = self.games_list[self.game_index]["players"]
        self.games_list[self.game_index]["players"] = \
            list(dict.fromkeys(players_list))

        return

    def add_player(self, player: str) -> None:
        """
        Adds a player to the current match. Can't add the world (there's no dict big enough)
        It's kills starts with zero

        :param player: player name being added
        :return:
        """
        if player and player != "<world>":
            self.games_list[self.game_index]["players"].append(player)
            if not self.games_list[self.game_index]["kills"].get(player):
                self.games_list[self.game_index]["kills"][player] = 0
        return

    def add_kill(self, player_from: str, player_to: str) -> None:
        """
        Adds a kill to the score board. If a player is killed by the world, a score is deducted from him
        If a player kills himself, no score is given (or taken)

        :param player_from: the player who killed
        :param player_to: the player who was killed
        :return:
        """
        self.games_list[self.game_index]["total_kills"] += 1

        if player_from == player_to:
            return

        player_from_kills = self.games_list[self.game_index]["kills"].get(player_from, 0)
        player_to_kills = self.games_list[self.game_index]["kills"].get(player_to, 0)

        if player_from == "<world>":
            self.games_list[self.game_index]["kills"][player_to] = player_to_kills - 1
        else:
            self.games_list[self.game_index]["kills"][player_from] = player_from_kills + 1

        return
