from unittest import TestCase, mock
from log_parser import LogParser
import json


class TestLogParser(TestCase):
    def setUp(self) -> None:
        self.log_parser = LogParser()

    def test_parse_log_with_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            response = self.log_parser.parse_log("fake_file")

    @mock.patch("log_parser.LogParser.save_cache")
    @mock.patch("log_parser.LogParser.check_cache")
    def test_parse_log_with_valid_file(self, mock_check_cache, mock_save_cache):
        mock_check_cache.return_value = None
        mock_save_cache.return_value = json.loads("{}")

        response = self.log_parser.parse_log("../../challenge/games.log")
        self.assertEqual(dict, type(response))

    @mock.patch("log_parser.LogParser.check_cache")
    def test_parse_log_with_cache(self, mock_cache):
        mock_cache.return_value = "CACHED CONTENT"

        response = self.log_parser.parse_log("../../challenge/games.log")
        self.assertEqual("CACHED CONTENT", response)

    def test_parse_kill_line_with_invalid_input(self):
        response = self.log_parser.parse_kill_line(
            " 21:07 Kill 1022 2 22 <world> killed Isgalamido by MOD_TRIGGER_HURT")
        self.assertEqual((None, None), response)

    def test_parse_kill_line_with_valid_input(self):
        response = self.log_parser.parse_kill_line(
            " 21:07 Kill: 1022 2 22: <world> killed Isgalamido by MOD_TRIGGER_HURT")
        self.assertEqual(("<world>", "Isgalamido"), response)

    def test_parse_join_line_with_invalid_input(self):
        input = " 20:38 ClientUserinfoChanged: Isgalamido\\t\\0\\model\\uriel/zael\\hmodel\\uriel/zael\\" \
                "g_redteam\\g_blueteam\\c1\\5\\c2\\5\\hc\\100\\w\\0\\l\\0\\tt\\0\\tl\\0"
        response = self.log_parser.parse_join_line(input)
        self.assertEqual(None, response)

    def test_parse_join_line_with_valid_input(self):
        input = " 20:38 ClientUserinfoChanged: 2 n\\Isgalamido\\t\\0\\model\\uriel/zael\\hmodel\\uriel/zael\\" \
                "g_redteam\\g_blueteam\\c1\\5\\c2\\5\\hc\\100\\w\\0\\l\\0\\tt\\0\\tl\\0"
        response = self.log_parser.parse_join_line(input)
        self.assertEqual("Isgalamido", response)