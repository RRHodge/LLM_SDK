"""Unit tests for Pydantic data models in vocabulary.py."""
    
import json
from pathlib import Path
import unittest
from LLM_SDK.src.vocabulary import TokenVocabulary

class TestVocabulary(unittest.TestCase):
    """Test suite for the TokenVocabulary class in vocabulary.py."""

    def setUp(self) -> None:
        """Set up a temporary vocabulary file for testing."""
        self.temp_path = Path("temp_vocab.json")
        vocab_data = {
            "hello": 1,
            "world": 2,
            "test": 3
        }
        with open(self.temp_path, "w", encoding="utf-8") as f:
            json.dump(vocab_data, f)

    def tearDown(self) -> None:
        """Clean up the temporary vocabulary file after tests."""
        if self.temp_path.exists():
            self.temp_path.unlink()

    def test_load_vocabulary_valid(self) -> None:
        """Test loading a valid vocabulary file."""
        vocab = TokenVocabulary.load_vocabulary(self.temp_path)
        self.assertEqual(vocab.token_to_id["hello"], 1)
        self.assertEqual(vocab.token_to_id["world"], 2)
        self.assertEqual(vocab.token_to_id["test"], 3)

    def test_load_vocabulary_missing_file(self) -> None:
        """Test that loading from a non-existent file raises FileNotFoundError."""
        missing_path = Path("missing_vocab.json")
        with self.assertRaises(FileNotFoundError):
            TokenVocabulary.load_vocabulary(missing_path)

    def test_load_vocabulary_malformed_json(self) -> None:
        """Test that malformed JSON content raises ValueError."""
        bad_json_path = Path("bad_vocab.json")
        with open(bad_json_path, "w", encoding="utf-8") as f:
            f.write("{ invalid json... }")

        with self.assertRaises(ValueError):
            TokenVocabulary.load_vocabulary(bad_json_path)

        # Clean up the bad JSON file
        if bad_json_path.exists():
            bad_json_path.unlink()