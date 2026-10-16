"""Data loading and saving utilities for JSON inputs and output results.

Provides robust file reading, JSON parsing, and Pydantic validation for
function definitions, test prompts, and execution results.
Handles missing files, malformed JSON, and validation errors gracefully.
"""

import json
from pathlib import Path
from typing import List, Union

from pydantic import ValidationError

from src.models import FunctionResult, FunctionSchema, PromptSchema

def load_function_definitions(filepath: Union[str, Path]) -> List[FunctionSchema]:
    """Load and validate function definitions from a JSON file.

    Args:
        filepath: Path to the functions_definition.json file.

    Returns:
        A list of validated FunctionSchema objects.

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If the file contains invalid JSON.
        ValidationError: If any of the function definitions are invalid.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError("Function definitions file not found.")

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as err:
        raise ValueError(f"Malformed JSON in {filepath}: {err}") from err

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of function definitions in {filepath}, got {type(data).__name__}"
        )

    validated_functions: List[FunctionSchema] = []

    for index, func_data in enumerate(data):
        try:
            func = FunctionSchema.model_validate(func_data)
            validated_functions.append(func)
        except ValidationError as err:
            raise ValueError(
                f"Validation error in function definition at index {index} in {filepath}:\n{err}"
            ) from err

    return validated_functions


def load_test_prompts(filepath: Union[str, Path]) -> List[PromptSchema]:
    """Load and validate test prompts from a JSON file.

    Args:
        filepath: Path to the test_prompts.json file.

    Returns:
        A list of validated PromptSchema objects.

    Raises:
        FileNotFoundError: If the specified file is not found.
        json.JSONDecodeError: If the file contains invalid JSON.
        ValidationError: If any of the test prompts are invalid.
    """
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError("Test prompts file not found.")

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as err:
        raise ValueError(f"Malformed JSON in {filepath}: {err}") from err

    if not isinstance(data, list):
        raise ValueError(
            f"Expected a list of test prompts in {filepath}, got {type(data).__name__}"
        )

    validated_prompts: List[PromptSchema] = []

    for index, prompt_data in enumerate(data):
        try:
            prompt = PromptSchema.model_validate(prompt_data)
            validated_prompts.append(prompt)
        except ValidationError as err:
            raise ValueError(
                f"Validation error in test prompt at index {index} in {filepath}:\n{err}"
            ) from err

    return validated_prompts


def save_function_results(filepath: Union[str, Path], results: List[FunctionResult]) -> None:
    """Save function execution results to a JSON file.

    Args:
        results: List of FunctionResult objects to be saved.
        filepath: Path to the output JSON file.

    Raises:
        IOError: If there is an error writing to the file.
    """
    path = Path(filepath)
    try:
        with open(path, "w", encoding="utf-8") as file:
            json.dump([result.model_dump() for result in results], file, indent=4)
    except IOError as err:
        raise IOError(f"Error writing function results to {filepath}: {err}") from err