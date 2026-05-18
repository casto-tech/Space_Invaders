import json
import pathlib
import tempfile
import unittest
import turtle_invaders.highscore as hs


class TestHighscore(unittest.TestCase):
    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self._orig_path = hs._SCORE_PATH
        hs._SCORE_PATH = pathlib.Path(self._tmpdir.name) / "highscore.json"

    def tearDown(self):
        hs._SCORE_PATH = self._orig_path
        self._tmpdir.cleanup()

    def test_load_missing_file_returns_zero(self):
        self.assertEqual(hs.load(), 0)

    def test_save_and_load_roundtrip(self):
        hs.save(4200)
        self.assertEqual(hs.load(), 4200)

    def test_save_creates_parent_dirs(self):
        hs.save(99)
        self.assertTrue(hs._SCORE_PATH.exists())

    def test_load_corrupted_json_returns_zero(self):
        hs._SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        hs._SCORE_PATH.write_text("not valid json")
        self.assertEqual(hs.load(), 0)

    def test_load_missing_key_returns_zero(self):
        hs._SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        hs._SCORE_PATH.write_text(json.dumps({"other_key": 99}))
        self.assertEqual(hs.load(), 0)

    def test_load_non_integer_value_returns_zero(self):
        hs._SCORE_PATH.parent.mkdir(parents=True, exist_ok=True)
        hs._SCORE_PATH.write_text(json.dumps({"high_score": "not_a_number"}))
        self.assertEqual(hs.load(), 0)
