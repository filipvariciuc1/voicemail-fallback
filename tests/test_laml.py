"""Checks for the fallback LaML. Run: python -m unittest discover tests

SignalWire only fetches these when the live bin fails, so a broken file stays
hidden until an outage. These tests catch the mistakes that would bite then.
"""
import re
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://filipvariciuc1.github.io/voicemail-fallback/"
FILES = ["vm.xml", "done.xml"]


def load(name):
    return ET.parse(ROOT / name).getroot()


class LamlTest(unittest.TestCase):
    def test_well_formed_response(self):
        for name in FILES:
            with self.subTest(name=name):
                root = load(name)
                self.assertEqual(root.tag, "Response")
                self.assertEqual(root[-1].tag, "Hangup")

    def test_record_action_is_get_on_pages(self):
        # GitHub Pages answers POST with 405, so every fetch must be GET.
        rec = load("vm.xml").find("Record")
        self.assertIsNotNone(rec)
        self.assertEqual(rec.get("method"), "GET")
        self.assertEqual(rec.get("action"), BASE + "done.xml")
        self.assertTrue((ROOT / "done.xml").is_file())

    def test_no_paid_transcription(self):
        # The live bins dropped SignalWire transcription on 10/05/2026; the
        # Voicemail app transcribes the mp3 itself for free.
        for name in FILES:
            for el in load(name).iter():
                self.assertNotEqual(el.get("transcribe", "false").lower(), "true", name)

    def test_greeting_starts_after_pause(self):
        # Matches the live bin: without it callers miss the first words.
        root = load("vm.xml")
        self.assertEqual(root[0].tag, "Pause")

    def test_record_limits(self):
        rec = load("vm.xml").find("Record")
        self.assertLessEqual(int(rec.get("maxLength")), 240)
        self.assertEqual(rec.get("finishOnKey"), "#")

    def test_no_phone_numbers(self):
        # Public repo: never publish a number.
        for path in ROOT.rglob("*"):
            if ".git" in path.parts or not path.is_file() or path.suffix == ".py":
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            self.assertIsNone(re.search(r"\+?1?[\s(.-]*\d{3}[\s).-]*\d{3}[\s.-]*\d{4}", text), path.name)


if __name__ == "__main__":
    unittest.main()
