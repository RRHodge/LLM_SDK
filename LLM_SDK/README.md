_This project has been created as partof the 42 curriculum by rarabeto._

# Description

## Data Schema &amp; Validation (`src/models.py`)
The `src/models.py` module defines the data contract for the function calling pipeline, enforcing strict type safety and schema validation using **Pydantic v2** as mandated by the project requirement. All models inherit from `pydantic.Basemodel` and utilize `typing.Annotated` with `pydantic.Field` for modern, idiomatic type declarations.

To ensure resilience during parsing and peer evaluation, every model configures `ConfigDict(extra="ignore")`

---
### Core Data Models 

| Model Class | Source / Role | Description &amp; Validated Fields |
| :--- | :--- | :--- |
| **`ParameterProperty`** | `functions_definition.json` | Represents an individual function parameter's schema, validating its data `type` (e.g., `string`, `number`, `boolean`) and optional `description`. |
| **`FunctionParameters`** | `functions_definition.json` | Container for parameter schemas, validating the container `type` (defaults to `"object"`), the `properties` dictionary, and the `required` arguments list. |
| **`FunctionReturns`** | `functions_definition.json` | Container for value returns of schema, validating the container `type` (e.g., `string`, `number`, `boolean`) and optional `description` |
 **`FunctionSchema`**| `functions_definition.json` | Validates the complete tool function definition schema, including its unique `name`, human-readable `description`, and accepted `parameters` |
| **`FunctionResult`**| `functions_definition.json` | Enforce the strict 3-field output contract (`prompt`, `name`, `parameters`) required for the final evaluation results. |

---

### Key Design Decisions &amp; Features

1. **Mandatory Pydantic Validation**:
    > In strict compliance with project specifications, all input and output structures are validated through Pydantic models to guarantee 100% schema integrity without relying on unvalidated dictionaries.

2. **Compliznt Output Formatting**:

    > The `FunctionResult` model strictly restricts exported fields to `prompt` (string), `name` (string), and `parameters` (object). Calling `.model_dump()` on a `FunctionResult` instance produces a clean Python dictionary matching the required JSON structure.
---

### Validating &amp; Unit Testing (`tests/test_models.py`)

The integrity of `src\models.py` is verified via automated unit tests in `test/test_models.py`:

* **Nested Schema Parsing**: `test_function_schema_validation` verifies that raw dictionary definitions are correctly validated into nested `FunctionSchema` and `ParameterProperty` instances using `.model_validate()`.

* **Output Contract Verification**: `test_function_result_dump` ensures that `model_dump` yields exactly the three required keys (`prompt`, `name`, `parameters`).

* **Error Handling**: `test_invalid_prompt_schema_raises` confirms that missing required fields trigger a `pydantic.ValidationError`.


```python
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
```

## (`src/loaders.py`)


```python

```


# Instruction


# Resources

