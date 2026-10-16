"""Unit tests for Pydantic data models in models.py."""

import unittest
from pydantic import ValidationError
from src.models import (
    FunctionParameters,
    FunctionResult,
    FunctionReturns,
    FunctionSchema,
    ParameterProperty,
    PromptSchema,
)


class TestModels(unittest.TestCase):
    """Test suite for data models in models.py."""

    def test_parameter_property_valid(self) -> None:
        """Test valid ParameterProperty instantiation."""
        property = ParameterProperty(
            type="number",
            description="A test number"
        )
        self.assertEqual(property.type, "number")
        self.assertEqual(property.description, "A test number")

    def test_function_parameters_defaults(self) -> None:
        """Test FunctionParameters default values."""
        params = FunctionParameters()
        self.assertEqual(params.type, "object")
        self.assertEqual(params.properties, {})
        self.assertEqual(params.required, [])

    def test_function_returns_valid(self) -> None:
        """Test FunctionReturns with valid input."""
        returns = FunctionReturns(type="number")
        self.assertEqual(returns.type, "number")

    def test_function_schema_validation(self) -> None:
        """Test FunctionSchema validation and nested model creation."""
        schema_data = {
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
        schema = FunctionSchema.model_validate(schema_data)
        self.assertEqual(schema.name, "fn_add_numbers")
        self.assertIn("a", schema.parameters.properties)
        self.assertEqual(schema.parameters.properties["a"].type, "number")
        self.assertEqual(schema.parameters.required, ["a", "b"])
        self.assertEqual(schema.returns.type, "number")

    def test_prompt_schema_valid(self) -> None:
        """Test PromptSchema with valid input."""
        prompt = PromptSchema(prompt="Calculate 2 + 2")
        self.assertEqual(prompt.prompt, "Calculate 2 + 2")

    def test_function_result_dumped(self) -> None:
        """Test FunctionResult with valid input."""
        result = FunctionResult(
            prompt="What is 5 + 5?",
            name="fn_add_numbers",
            parameters={"a": 5, "b": 5},
        )
        dumped = result.model_dump()
        self.assertEqual(dumped["prompt"], "What is 5 + 5?")
        self.assertEqual(dumped["name"], "fn_add_numbers")
        self.assertEqual(dumped["parameters"], {"a": 5, "b": 5})

    def test_invalid_prompt_schema_raises(self) -> None:
        """Test that PromptSchema raises ValidationError for missing required fields."""
        with self.assertRaises(ValidationError):
            PromptSchema({})

    def test_function_result_schema_raises(self) -> None:
        """Test that FunctionResult raises ValidationError for missing required fields."""
        with self.assertRaises(ValidationError):
            FunctionResult(
                prompt="What is 5 + 5?",
                name="fn_add_numbers",
                # Missing 'parameters' field
            )


if __name__ == "__main__":
    unittest.main()