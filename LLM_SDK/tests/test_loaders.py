"""Unit tests for data loaders and result exporter in loaders.py."""

import json
import tempfile
import unittest
from pathlib import Path

from src.loaders import (
    load_function_definitions,
    load_test_prompts,
    save_function_results
)

from src.models import FunctionResult, FunctionSchema, PromptSchema

class TestLoaders(unittest.TestCase):
    """Test suite for functions in loaders.py."""

    def setUp(self) -> None:
        """Set up a temporary directory and sample data files."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.temp_path = Path(self.temp_dir.name)

        # Sample valid functions definition
        self.valid_funcs_path = self.temp_path / "functions_definition.json"
        self.valid_funcs_data = [
            {
                "name": "fn_add_numbers",
                "description": "Add two numbers together",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number", "description": "First number"},
                        "b": {"type": "number", "description": "Second number"},
                    },
                    "required": ["a", "b"],
                },
                "returns": {
                    "type": "number",
                }
            }
        ]
        with open(self.valid_funcs_path, "w", encoding="utf-8") as f:
            json.dump(self.valid_funcs_data, f)

        # Sample valid test prompts
        self.valid_prompts_path = self.temp_path / "function_calling_tests.json"
        self.valid_prompts_data = [
            {"prompt": "What is 2 + 2?"},
            {"prompt": "Calculate 10 times 5"},
        ]
        with open(self.valid_prompts_path, "w", encoding="utf-8") as f:
            json.dump(self.valid_prompts_data, f)

    def tearDown(self) -> None:
        """Clean up temporary directory."""
        self.temp_dir.cleanup()

    def test_load_function_definitions_valid(self) -> None:
        """Test loading valid function definitions."""
        funcs = load_function_definitions(self.valid_funcs_path)
        self.assertEqual(len(funcs), 1)
        self.assertIsInstance(funcs[0], FunctionSchema)
        self.assertEqual(funcs[0].name, "fn_add_numbers")
        self.assertEqual(funcs[0].description, "Add two numbers together")
        self.assertEqual(funcs[0].parameters["properties"]["a"]["description"], "First number")
        self.assertEqual(funcs[0].parameters["properties"]["b"]["description"], "Second number")
        self.assertEqual(funcs[0].returns["type"], "number")


    def test_load_test_prompts_valid(self) -> None:
        """Test loading valid test prompts."""
        prompts = load_test_prompts(self.valid_prompts_path)
        self.assertEqual(len(prompts), 2)
        self.assertIsInstance(prompts[0], PromptSchema)
        self.assertEqual(prompts[0].prompt, "What is 2 + 2?")
        self.assertEqual(prompts[1].prompt, "Calculate 10 times 5")

    def test_load_missing_file_raises_file_not_found(self) -> None:
        """Test that loading from a non-existent file path raises FileNotFoundError."""
        missing = self.temp_path / "missing.json"
        with self.assertRaises(FileNotFoundError):
            load_function_definitions(missing)
        with self.assertRaises(FileNotFoundError):
            load_test_prompts(missing)

    def test_load_malformed_json_raises_value_error(self) -> None:
        """Test that malformed JSON content raises ValueError."""
        bad_json_path = self.temp_path / "bad.json"
        with open(bad_json_path, "w", encoding="utf-8") as f:
            f.write("{ invalid json... }")

        with self.assertRaises(ValueError):
            load_function_definitions(bad_json_path)
        with self.assertRaises(ValueError):
            load_test_prompts(bad_json_path)

    def test_save_function_results(self) -> None:
        """Test saving function results to a JSON file."""
        results_path = self.temp_path / "function_results.json"
        results = [
            FunctionResult(
                prompt="What is 5 + 5?",
                name="fn_add_numbers",
                parameters={"a": 5, "b": 5},
            )
        ]
        save_function_results(results, results_path)

        # Verify the file was created and contains the expected data
        self.assertTrue(results_path.is_file())
        with open(results_path, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
        self.assertEqual(len(loaded_data), 1)
        self.assertEqual(loaded_data[0]["prompt"], "What is 5 + 5?")
        self.assertEqual(loaded_data[0]["name"], "fn_add_numbers")
        self.assertEqual(loaded_data[0]["parameters"], {"a": 5, "b": 5})