from unittest import TestCase
from game_control import GameControl


class TestGameControl(TestCase):
    def setUp(self) -> None:
        self.game_control = GameControl()

    def test_game_index_attribute(self):
        self.assertEqual("game_0", self.game_control.game_index)

    def test_start_game(self):
        self.game_control.start_game()

        expected_games_list = {
            self.game_control.game_index: {
                "total_kills": 0,
                "players": [],
                "kills": {}
            }
        }

        self.assertEqual(1, self.game_control.game_count)
        self.assertEqual(True, self.game_control.started)
        self.assertEqual(False, self.game_control.finished)
        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_start_game_without_finishing_previous(self):
        expected_games_list = {
            "game_1": {
                "total_kills": 0,
                "players": [],
                "kills": {}
            }
        }

        self.game_control.start_game()
        self.assertEqual("game_1", self.game_control.game_index)
        self.assertEqual(True, self.game_control.started)
        self.assertEqual(False, self.game_control.finished)
        self.assertEqual(expected_games_list, self.game_control.games_list)

        expected_games_list = {
            "game_1": {
                "total_kills": 0,
                "players": [],
                "kills": {}
            },
            "game_2": {
                "total_kills": 0,
                "players": [],
                "kills": {}
            }
        }

        self.game_control.start_game()
        self.assertEqual("game_2", self.game_control.game_index)
        self.assertEqual(True, self.game_control.started)
        self.assertEqual(False, self.game_control.finished)
        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_finish_game(self):
        self.game_control.start_game()
        self.game_control.finish_game()

        expected_games_list = {
            self.game_control.game_index: {
                "total_kills": 0,
                "players": [],
                "kills": {}
            }
        }

        self.assertEqual(1, self.game_control.game_count)
        self.assertEqual(False, self.game_control.started)
        self.assertEqual(True, self.game_control.finished)
        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_finish_game_with_repeated_players(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")
        self.game_control.add_player("Yauari")
        self.game_control.finish_game()

        expected_games_list = {
            "game_1": {
                "total_kills": 0,
                "players": ["Yauari"],
                "kills": {
                    "Yauari": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_add_one_player(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")

        expected_games_list = {
            "game_1": {
                "total_kills": 0,
                "players": ["Yauari"],
                "kills": {
                    "Yauari": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_add_repeated_player(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")
        self.game_control.add_player("Yauari")

        expected_games_list = {
            "game_1": {
                "total_kills": 0,
                "players": ["Yauari", "Yauari"],
                "kills": {
                    "Yauari": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_add_different_players(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")
        self.game_control.add_player("Vieira")

        expected_games_list = {
            "game_1": {
                "total_kills": 0,
                "players": ["Yauari", "Vieira"],
                "kills": {
                    "Yauari": 0,
                    "Vieira": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_add_suicide_kill(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")
        self.game_control.add_player("Vieira")
        self.game_control.add_kill("Yauari", "Yauari")

        expected_games_list = {
            "game_1": {
                "total_kills": 1,
                "players": ["Yauari", "Vieira"],
                "kills": {
                    "Yauari": 0,
                    "Vieira": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_add_world_kill(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")
        self.game_control.add_player("Vieira")
        self.game_control.add_kill("<world>", "Yauari")

        expected_games_list = {
            "game_1": {
                "total_kills": 1,
                "players": ["Yauari", "Vieira"],
                "kills": {
                    "Yauari": -1,
                    "Vieira": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)

    def test_add_valid_kill(self):
        self.game_control.start_game()
        self.game_control.add_player("Yauari")
        self.game_control.add_player("Vieira")
        self.game_control.add_kill("Yauari", "Vieira")

        expected_games_list = {
            "game_1": {
                "total_kills": 1,
                "players": ["Yauari", "Vieira"],
                "kills": {
                    "Yauari": 1,
                    "Vieira": 0
                }
            }
        }

        self.assertEqual(expected_games_list, self.game_control.games_list)
